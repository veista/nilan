"""Nilan CTS700 Compact P Køl Polar/Nordic/Arctic (XL) hybrid device.

Hardware: CTS700 LC Board (e.g. v4.0 / NCS-700), product family
Compact P Køl Polar/Nordic/Arctic (XL), varenr 75124xx.

Fan writes use holding 4747 with values 101-104. Do not mix with CTS700 2018+
(21771 percent) or CTS700 2015 legacy (4747 percent).
"""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components.modbus import modbus
from homeassistant.core import HomeAssistant

from .capabilities import (
    capabilities_for_cts700_nordic,
    filter_attributes_by_capabilities,
)
from .device_map_cts700_nordic import CTS700_NORDIC_ENTITY_MAP
from .modbus_hub_util import build_modbus_hub_name, wait_for_modbus_connected
from .register_probe import (
    PROBE_SPECS,
    deserialize_dead_registers,
    run_register_probe,
)
from .registers import CTS700NordicRegisters as Reg

_LOGGER = logging.getLogger(__name__)

_TEMP_SCALE = 10

# Nordic holding 5432: 0 off, 1 cool, 2 heat, 3 dehum, 4 DHW
# Climate layer: 1 heat, 2 cool, 3 auto
_NORDIC_TO_CLIMATE = {1: 2, 2: 1, 3: 3, 4: 3}
_CLIMATE_TO_NORDIC = {1: 2, 2: 1, 3: 3}


class DeviceCTS700Nordic:
    """CTS700 Nordic XL hybrid map device."""

    def __init__(
        self,
        hass: HomeAssistant,
        name,
        com_type,
        host_ip: str | None,
        host_port,
        unit_id,
        hub_name: str | None = None,
        stored_dead_registers: list | None = None,
    ) -> None:
        """Create Nordic hybrid device."""
        self.hass = hass
        self._device_name = name
        self._device_type = "Compact P Køl Polar/Nordic/Arctic XL CTS700"
        self._device_sw_ver = "CTS700 Nordic/Polar/Arctic hybrid map"
        self._device_hw_ver = "CTS700"
        self._host_ip = host_ip
        self._host_port = host_port
        self._unit_id = int(unit_id)
        self._com_type = com_type
        self._hub_name = hub_name or build_modbus_hub_name(
            name, board_type="CTS700_NORDIC", unit_id=self._unit_id
        )
        self._client_config = {
            "name": self._hub_name,
            "type": self._com_type,
            "method": "rtu",
            "delay": 0,
            "port": self._host_port,
            "timeout": 3,
            "host": self._host_ip,
            "parity": "E",
            "baudrate": 19200,
            "bytesize": 8,
            "stopbits": 1,
        }
        self._modbus = modbus.ModbusHub(self.hass, self._client_config)
        # Serialize hub calls: many HA entities poll in parallel; CTS Ethernet
        # drops overlapping requests (state "unknown" / glance spinners / NaN).
        self._modbus_lock = asyncio.Lock()
        self._attributes = {}
        self._board_type = "CTS700_NORDIC"
        self._capabilities: frozenset[str] = frozenset()
        self._dead_registers: set[tuple[str, int]] = set()
        self._unsupported_attributes: set[str] = set()
        self._stored_dead_registers = stored_dead_registers
        self._probe_ran = False

    async def async_close(self):
        """Close modbus connection."""
        await self._modbus.async_close()

    async def setup(self):
        """Modbus and attribute map setup."""
        _LOGGER.debug("CTS700 Nordic setup started")
        success = await self._modbus.async_setup()
        if success:
            await wait_for_modbus_connected(self._modbus)
        else:
            await self._modbus.async_close()
            raise ValueError("Modbus setup was unsuccessful")

        probe = await self._read_input(Reg.t3_extract)
        if probe is None:
            await self._modbus.async_close()
            raise ValueError("CTS700 Nordic probe read failed")

        for entity, value in CTS700_NORDIC_ENTITY_MAP.items():
            self._attributes[entity] = value["entity_type"]

        caps = capabilities_for_cts700_nordic()
        self._capabilities = caps
        self._attributes = filter_attributes_by_capabilities(
            self._attributes, CTS700_NORDIC_ENTITY_MAP, caps
        )

        outdoor = await self.get_t1_intake_temperature()
        if outdoor is not None:
            _LOGGER.debug("CTS700 Nordic outdoor probe %.1f C", outdoor)
        if self._stored_dead_registers is not None:
            try:
                self._dead_registers = deserialize_dead_registers(
                    self._stored_dead_registers
                )
            except (TypeError, ValueError):
                _LOGGER.warning(
                    "Stored dead-register data invalid; re-probing"
                )
                self._stored_dead_registers = None
            if self._stored_dead_registers is not None:
                self._unsupported_attributes = {
                    attr
                    for attr, regs in PROBE_SPECS["CTS700_NORDIC"].items()
                    if all(
                        (kind, address) in self._dead_registers
                        for kind, address in regs
                    )
                }
                _LOGGER.debug(
                    "Loaded %d dead registers from stored config",
                    len(self._dead_registers),
                )
        if self._stored_dead_registers is None:
            try:
                await run_register_probe(self, PROBE_SPECS["CTS700_NORDIC"])
                self._probe_ran = True
            except Exception:  # noqa: BLE001 — probe must never fail setup
                _LOGGER.warning(
                    "CTS700 Nordic register probe failed; continuing with core-only setup"
                )
        self._device_sw_ver = "CTS700 Nordic/Polar/Arctic hybrid map"
        _LOGGER.debug(
            "CTS700 Nordic attributes=%s capabilities=%s",
            list(self._attributes.keys()),
            sorted(caps),
        )

    def get_assigned(self, platform: str):
        """Get platform assignment."""
        return [key for key, value in self._attributes.items() if value == platform]

    @property
    def get_device_name(self):
        """Device name."""
        return self._device_name

    @property
    def get_hub_name(self):
        """Stable entry-derived modbus hub name."""
        return self._hub_name

    @property
    def get_device_type(self):
        """Device type."""
        return self._device_type

    @property
    def get_device_hw_version(self):
        """Hardware version."""
        return self._device_hw_ver

    @property
    def get_device_sw_version(self):
        """Software version string."""
        return self._device_sw_ver

    @property
    def get_attributes(self):
        """Return device attributes."""
        return self._attributes

    def supports_attribute(self, name: str) -> bool:
        """True when the probed registers for this attribute are alive."""
        return name not in self._unsupported_attributes

    async def _pb_call(self, address: int, value, call_type: str):
        """Single-flight Modbus call on this hub."""
        async with self._modbus_lock:
            return await self._modbus.async_pb_call(
                self._unit_id, address, value, call_type
            )

    async def _read_holding(self, address: int) -> int | None:
        """Read one holding register as signed int."""
        if ("holding", address) in self._dead_registers:
            return None
        result = await self._pb_call(address, 1, "holding")
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        return None

    async def _read_holding_unsigned(self, address: int) -> int | None:
        """Read one holding register as unsigned int."""
        if ("holding", address) in self._dead_registers:
            return None
        result = await self._pb_call(address, 1, "holding")
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        return None

    async def _read_input(self, address: int) -> int | None:
        """Read one input register as signed int."""
        if ("input", address) in self._dead_registers:
            return None
        result = await self._pb_call(address, 1, "input")
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        return None

    async def _read_input_unsigned(self, address: int) -> int | None:
        """Read one input register as unsigned int."""
        if ("input", address) in self._dead_registers:
            return None
        result = await self._pb_call(address, 1, "input")
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        return None

    async def _write_holding(self, address: int, value: int) -> bool:
        """Write one holding register.

        Prefer FC6 write_register (HA Modbus climate default for setpoints).
        Fall back to FC16 write_registers (fan step 4747 accepts FC16).
        """
        result = await self._pb_call(address, value, "write_register")
        if result is not None:
            return True
        result = await self._pb_call(address, [value], "write_registers")
        if result is None:
            _LOGGER.error(
                "CTS700 Nordic write failed address=%s value=%s (FC6 and FC16)",
                address,
                value,
            )
            return False
        return True

    async def _read_temp_input(self, address: int) -> float | None:
        """Read input temperature with 0.1 scale."""
        value = await self._read_input(address)
        if value is None:
            return None
        return float(value) / _TEMP_SCALE

    async def _read_temp_holding(self, address: int) -> float | None:
        """Read holding temperature with 0.1 scale."""
        value = await self._read_holding(address)
        if value is None:
            return None
        return float(value) / _TEMP_SCALE

    async def _temp_matches(self, address: int, celsius: float) -> bool:
        """True if holding temp readback matches wanted Celsius."""
        verify = await self._read_temp_holding(address)
        if verify is None:
            return False
        return abs(verify - celsius) <= 0.15

    async def _write_temp(
        self, address: int, celsius: float, min_v: float, max_v: float
    ) -> bool:
        """Write temperature with 0.1 scale; verify readback.

        Room/DHW setpoints on Compact P Nordic match HA YAML climate: FC6 first.
        Some firmwares reject FC16 on 4746/20460 while still accepting FC16 on 4747.
        """
        try:
            celsius_f = float(celsius)
        except (TypeError, ValueError):
            _LOGGER.error("CTS700 Nordic temp write invalid value %r", celsius)
            return False
        if celsius_f < min_v or celsius_f > max_v:
            _LOGGER.error(
                "CTS700 Nordic temp %s out of range %s..%s (address %s)",
                celsius_f,
                min_v,
                max_v,
                address,
            )
            return False
        raw = int(round(celsius_f * _TEMP_SCALE))
        output = int.from_bytes(
            raw.to_bytes(2, "little", signed=True), "little", signed=False
        )

        # FC6 (write single). HA may return None even when the unit accepted the write.
        await self._modbus.async_pb_call(
            self._unit_id, address, output, "write_register"
        )
        if await self._temp_matches(address, celsius_f):
            return True

        # FC16 fallback
        await self._modbus.async_pb_call(
            self._unit_id, address, [output], "write_registers"
        )
        if await self._temp_matches(address, celsius_f):
            return True

        _LOGGER.warning(
            "CTS700 Nordic temp write address=%s wanted=%.1f did not stick",
            address,
            celsius_f,
        )
        return False

    async def _raw_operation_mode(self) -> int | None:
        """Raw Nordic operation mode from 5432."""
        return await self._read_holding_unsigned(Reg.operation_mode)

    def get_climate_fan_modes(self) -> list[str]:
        """Nordic fan steps are 1-4 only (4747 = 101-104). No off via fan 0."""
        return ["1", "2", "3", "4"]

    def get_climate_hvac_modes(self) -> list[str]:
        """Selectable climate modes.

        Holding 5432 reports active cool/heat/dehum/DHW as status on Compact P
        Nordic; heat/cool writes do not stick as user setpoints. Keep Auto + Off.
        """
        return ["auto", "off"]

    def supports_water_heater_off(self) -> bool:
        """Compact P Nordic shared DHW setpoint does not reliably accept 0 as Off."""
        return False

    async def get_run_state(self) -> bool | None:
        """True when unit is not in off mode."""
        mode = await self._raw_operation_mode()
        if mode is None:
            _LOGGER.error("Could not read get_run_state")
            return None
        return mode != 0

    async def set_run_state(self, state: bool) -> None:
        """Turn off (mode 0) or restore auto/dehum (3) when starting from off."""
        if not state:
            await self._write_holding(Reg.operation_mode, 0)
            return
        current = await self._raw_operation_mode()
        if current in (None, 0):
            # 3 = dehum/auto path; controller then picks heat/cool itself
            await self._write_holding(Reg.operation_mode, 3)

    async def get_operation_mode(self) -> int | None:
        """Climate mode for HA mode selector (always auto when running).

        Active heat/cool from 5432 is exposed via get_control_state / hvac_action.
        """
        raw = await self._raw_operation_mode()
        if raw is None:
            _LOGGER.error("Could not read get_operation_mode")
            return None
        return 3

    async def set_operation_mode(self, mode: int) -> bool:
        """Accept Auto only; heat/cool are not user-writable setpoints on Nordic."""
        if mode != 3:
            _LOGGER.debug(
                "Ignoring Nordic HVAC mode %s (selectable modes are auto/off only)",
                mode,
            )
            return False
        # Auto means leave controller strategy alone; do not force 5432 writes
        return True

    async def get_ventilation_step(self) -> int | None:
        """Fan step 1-4 from holding 4747 values 101-104."""
        value = await self._read_holding_unsigned(Reg.user_fan_step)
        if value is None:
            _LOGGER.error("Could not read get_ventilation_step")
            return None
        if 101 <= value <= 104:
            return value - 100
        if value in (1, 2, 3, 4):
            return value
        # Step 0 / unknown: Nordic units do not expose fan-off on 4747
        return 1

    async def set_ventilation_step(self, mode: int) -> bool:
        """Write fan step as 101-104 (levels 1-4 only)."""
        if mode not in (1, 2, 3, 4):
            _LOGGER.debug("Ignoring Nordic fan step %s (valid 1-4)", mode)
            return False
        return await self._write_holding(Reg.user_fan_step, 100 + mode)

    async def get_control_state(self) -> int | None:
        """Approximate control state for climate action UI from raw 5432."""
        running = await self.get_run_state()
        if running is None:
            return None
        if not running:
            return 0
        raw = await self._raw_operation_mode()
        if raw is None:
            return None
        # Nordic 5432: 1 cool, 2 heat, 3 dehum, 4 DHW
        if raw == 2:
            return 7
        if raw == 1:
            return 8
        return 6

    async def get_control_temperature(self) -> float | None:
        """Room / extract air temperature (T3 input)."""
        value = await self._read_temp_input(Reg.t3_extract)
        if value is None:
            _LOGGER.error("Could not read get_control_temperature")
        return value

    async def get_user_temperature_setpoint(self) -> float | None:
        """Room temperature setpoint (4746)."""
        value = await self._read_temp_holding(Reg.user_temperature)
        if value is None:
            _LOGGER.error("Could not read get_user_temperature_setpoint")
        return value

    async def set_user_temperature_setpoint(self, value: float) -> bool:
        """Set room temperature setpoint (holding 4746)."""
        return await self._write_temp(Reg.user_temperature, value, 5, 30)

    async def get_t1_intake_temperature(self) -> float | None:
        """Outdoor air temperature."""
        return await self._read_temp_input(Reg.t1_outdoor)

    async def get_t2_inlet_temperature(self) -> float | None:
        """Supply air temperature."""
        return await self._read_temp_input(Reg.t2_supply)

    async def get_t3_exhaust_temperature(self) -> float | None:
        """Extract air temperature."""
        return await self._read_temp_input(Reg.t3_extract)

    async def get_t4_outlet(self) -> float | None:
        """Exhaust / after heat exchanger."""
        return await self._read_temp_holding(Reg.t4_exhaust)

    async def get_t5_condenser_temperature(self) -> float | None:
        """Condenser / after heat pump."""
        return await self._read_temp_holding(Reg.t5_condenser)

    async def get_t6_evaporator_temperature(self) -> float | None:
        """Evaporator temperature (T6)."""
        return await self._read_temp_holding(Reg.t6_evaporator)

    async def get_t7_inlet_temperature_after_heater(self) -> float | None:
        """Supply after after-heater (T7). None when register unused (~0 C)."""
        value = await self._read_temp_holding(Reg.t7_after_heater)
        if value is None:
            return None
        # Many Compact P Nordic/Polar units have no T7 sensor; bus returns 0.0
        if abs(value) < 0.05:
            return None
        return value

    async def get_t8_outdoor_temperature(self) -> float | None:
        """T8 outdoor / preheater path.

        Primary: input 5159 (wiring T8). Some Compact P firmwares also expose
        holding 20296. When 5159 tracks T1 exactly, try 20296 so HA is not
        showing a duplicated outdoor reading by mistake.
        """
        t1 = await self.get_t1_intake_temperature()
        t8_input = await self._read_temp_input(Reg.t8_preheater)
        t8_hold = await self._read_temp_holding(Reg.t8_before_preheater_holding)

        if t8_input is not None and t1 is not None and abs(t8_input - t1) < 0.15:
            if t8_hold is not None and abs(t8_hold - t1) >= 0.15:
                _LOGGER.debug(
                    "CTS700 Nordic T8: input 5159 mirrors T1 (%.1f); using holding 20296 (%.1f)",
                    t1,
                    t8_hold,
                )
                return t8_hold
            _LOGGER.debug(
                "CTS700 Nordic T8 equals T1 (%.1f C); expected when both are outdoor "
                "NTCs and preheater is idle",
                t1,
            )
            return t8_input

        if t8_input is not None:
            return t8_input
        return t8_hold

    async def get_t9_heater_temperature(self) -> float | None:
        """Water surface / after heater (T9, holding 20298)."""
        return await self._read_temp_holding(Reg.t9_water_surface)

    async def get_humidity(self) -> float | None:
        """Live extract humidity (4716)."""
        value = await self._read_input_unsigned(Reg.humidity_live)
        if value is None:
            _LOGGER.error("Could not read get_humidity")
            return None
        return float(value)

    async def get_average_humidity(self) -> float | None:
        """Long-average humidity (20164)."""
        value = await self._read_holding_unsigned(Reg.average_humidity)
        if value is None:
            return None
        return float(value)

    async def get_days_to_inlet_filter_change(self) -> int | None:
        """Days until inlet filter change (holding 1328 remaining; 20103 fallback)."""
        remaining = await self._read_holding_unsigned(Reg.filter_remaining_inlet)
        if remaining is not None:
            return remaining
        return await self._read_holding_unsigned(Reg.filter_days)

    async def get_days_since_inlet_filter_change(self) -> int | None:
        """Days since last inlet filter change (interval - remaining)."""
        interval = await self._read_holding_unsigned(Reg.filter_interval_inlet)
        remaining = await self._read_holding_unsigned(Reg.filter_remaining_inlet)
        if interval is None or remaining is None:
            return None
        return max(0, interval - remaining)

    async def get_days_to_exhaust_filter_change(self) -> int | None:
        """Days until exhaust filter change (holding 1329 remaining)."""
        return await self._read_holding_unsigned(Reg.filter_remaining_exhaust)

    async def get_days_since_exhaust_filter_change(self) -> int | None:
        """Days since last exhaust filter change (interval - remaining)."""
        interval = await self._read_holding_unsigned(Reg.filter_interval_exhaust)
        remaining = await self._read_holding_unsigned(Reg.filter_remaining_exhaust)
        if interval is None or remaining is None:
            return None
        return max(0, interval - remaining)

    async def get_filter_interval_inlet(self) -> int | None:
        """Inlet filter interval in days (holding 1326)."""
        return await self._read_holding_unsigned(Reg.filter_interval_inlet)

    async def get_filter_interval_exhaust(self) -> int | None:
        """Exhaust filter interval in days (holding 1327)."""
        return await self._read_holding_unsigned(Reg.filter_interval_exhaust)

    async def get_filter_alarm_state(self) -> bool | None:
        """Filter alarm active (input 5168)."""
        value = await self._read_input_unsigned(Reg.filter_alarm)
        if value is None:
            _LOGGER.warning(
                "Filter alarm read failed (input %s). Keeping previous HA state; "
                "check Ethernet Modbus load / overlapping YAML hub.",
                Reg.filter_alarm,
            )
            return None
        active = bool(value)
        prev = self._attributes.get("filter_alarm_state")
        if prev is not None and bool(prev) != active:
            _LOGGER.info(
                "Filter alarm changed: %s -> %s (raw=%s, input %s)",
                "ON" if prev else "OFF",
                "ON" if active else "OFF",
                value,
                Reg.filter_alarm,
            )
        elif active:
            _LOGGER.debug(
                "Filter alarm still ON (raw=%s, input %s)",
                value,
                Reg.filter_alarm,
            )
        self._attributes["filter_alarm_state"] = active
        return active

    async def get_fan_speed_percent(self) -> int | None:
        """Fan power / max percent (21771)."""
        return await self._read_holding_unsigned(Reg.fan_power_percent)

    async def get_bypass_damper_percent(self) -> int | None:
        """Bypass damper readout percent (holding 21773). Status only."""
        return await self._read_holding_unsigned(Reg.bypass_damper_percent)

    async def get_main_compressor_effort(self) -> int | None:
        """Main compressor / heat-pump effort percent (holding 4706).

        Community maps and mark007 YAML treat this as 0 when the heat pump is
        off and a positive percent (often up to 100) when the compressor runs.
        Useful as a live "is the heat pump on" signal on Compact P Nordic.
        """
        return await self._read_holding_unsigned(Reg.main_compressor_effort)

    async def get_heat_pump_state(self) -> bool | None:
        """Heat pump running derived from main compressor effort (4706 > 0)."""
        effort = await self.get_main_compressor_effort()
        if effort is None:
            return None
        return effort > 0

    async def get_bypass_flap_state(self) -> bool | None:
        """Bypass open/closed status (read-only).

        Prefer discrete holding 4704 (bypass 1). Fall back to 21773 percent.
        Do not expose a writable switch: Ethernet writes to 21773 often fail
        to stick on Compact P Nordic (see docs/cts700/ethernet-limits.md).
        """
        state = await self._read_holding_unsigned(Reg.bypass_1_state)
        if state is not None:
            return bool(state)
        pct = await self._read_holding_unsigned(Reg.bypass_damper_percent)
        if pct is None:
            _LOGGER.debug(
                "CTS700 Nordic bypass status unavailable (4704/21773). "
                "YAML Modbus coils stay unavailable while that hub is disabled."
            )
            return None
        return pct > 0

    async def get_supply_fan_speed(self) -> int | None:
        """Supply fan actual percent."""
        return await self._read_holding_unsigned(Reg.supply_fan_speed)

    async def get_return_fan_speed(self) -> int | None:
        """Extract fan actual percent."""
        return await self._read_holding_unsigned(Reg.extract_fan_speed)

    async def get_anode_state(self) -> int | None:
        """Anode status raw (0/1/2)."""
        return await self._read_holding_unsigned(Reg.anode_status)

    async def get_electric_water_heater_setpoint(self) -> float | None:
        """DHW setpoint."""
        return await self._read_temp_holding(Reg.hot_water_set_point)

    async def set_electric_water_heater_setpoint(self, value: float) -> bool:
        """Set DHW setpoint (holding 20460)."""
        if value == 0:
            return await self._write_holding(Reg.hot_water_set_point, 0)
        return await self._write_temp(Reg.hot_water_set_point, value, 5, 85)

    async def get_compressor_water_heater_setpoint(self) -> float | None:
        """Shared DHW setpoint."""
        return await self.get_electric_water_heater_setpoint()

    async def set_compressor_water_heater_setpoint(self, value: float) -> bool:
        """Set shared DHW setpoint."""
        return await self.set_electric_water_heater_setpoint(value)

    async def get_t11_electric_water_heater_temperature(self) -> float | None:
        """DHW top temperature."""
        return await self._read_temp_input(Reg.t11_dhw_top)

    async def get_t12_compressor_water_heater_temperature(self) -> float | None:
        """DHW bottom temperature."""
        return await self._read_temp_input(Reg.t12_dhw_bottom)

    async def get_electric_water_heater_state(self) -> bool | None:
        """No dedicated el-supplement bit in community map; always False."""
        return False

    async def set_electric_water_heater_state(self, value: bool | int) -> bool:
        """Do not write Compact P 2018 holding 20464 on the Nordic hybrid map."""
        _LOGGER.warning(
            "Electrical supplement heater write is not mapped on CTS700 Nordic "
            "(holding 20464 is Compact P 2018 only)"
        )
        return False
