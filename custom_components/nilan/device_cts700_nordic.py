"""Nilan CTS700 Compact P Køl Polar/Nordic/Arctic (XL) hybrid device.

Hardware: CTS700 LC Board (e.g. v4.0 / NCS-700), product family
Compact P Køl Polar/Nordic/Arctic (XL), varenr 75124xx.

Fan: holding 4747 may be classic steps 101-104 or percent 0-100 (map via
20140/42/44/46 or 21771). Optional controls live in
device_cts700_nordic_controls.py.
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
from .device_cts700_nordic_controls import CTS700NordicControlsMixin
from .device_cts700_nordic_sensors import CTS700NordicSensorsMixin
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


class DeviceCTS700Nordic(CTS700NordicControlsMixin, CTS700NordicSensorsMixin):
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
        """Nordic fan steps are 1-4 only. No off via fan 0."""
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

    # get_ventilation_step / set_ventilation_step / get_control_state /
    # get_actively_heating / get_electric_water_heater_state live on the mixin.

    # Sensor / DHW getters: CTS700NordicSensorsMixin
    # Fan / pauses / HVAC activity: CTS700NordicControlsMixin
