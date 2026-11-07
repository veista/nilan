"""Nilan CTS700 2015 legacy device (older Modbus map under 10000).

Fan on holding 4747 is percent 0-100 (mapped to climate 0-4). Never write
Nordic step values 101-104 here; that encoding belongs to CTS700_NORDIC.
"""

from __future__ import annotations

import logging

from homeassistant.components.modbus import modbus
from homeassistant.core import HomeAssistant

from .capabilities import (
    capabilities_for_cts700_legacy,
    filter_attributes_by_capabilities,
)
from .device_map_cts700_legacy import CTS700_LEGACY_ENTITY_MAP
from .modbus_hub_util import build_modbus_hub_name, wait_for_modbus_connected
from .register_probe import (
    PROBE_SPECS,
    deserialize_dead_registers,
    run_register_probe,
)
from .registers import CTS700LegacyHoldingRegisters as Reg

_LOGGER = logging.getLogger(__name__)

_TEMP_SCALE = 10

# Climate layer expects 1 heat / 2 cool / 3 auto.
# 2015 PDF prmOperationType: 0 auto / 1 cooling / 2 heating.
_PDF_TO_CLIMATE = {0: 3, 1: 2, 2: 1}
_CLIMATE_TO_PDF = {3: 0, 2: 1, 1: 2}


class DeviceCTS700Legacy:
    """Nilan CTS700 device using 2015 Modbus register map."""

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
        """Create CTS700 legacy device."""
        self.hass = hass
        self._device_name = name
        self._device_type = "CTS700 (2015 map)"
        self._device_sw_ver = "CTS700 2015 map"
        self._device_hw_ver = "CTS700"
        self._host_ip = host_ip
        self._host_port = host_port
        self._unit_id = int(unit_id)
        self._com_type = com_type
        self._hub_name = hub_name or build_modbus_hub_name(
            name, board_type="CTS700_LEGACY", unit_id=self._unit_id
        )
        self._client_config = {
            "name": self._hub_name,
            "type": self._com_type,
            "method": "rtu",
            "delay": 0,
            "port": self._host_port,
            "timeout": 1,
            "host": self._host_ip,
            "parity": "E",
            "baudrate": 19200,
            "bytesize": 8,
            "stopbits": 1,
        }
        self._modbus = modbus.ModbusHub(self.hass, self._client_config)
        self._attributes = {}
        self._board_type = "CTS700_LEGACY"
        self._capabilities = frozenset()
        self._dead_registers: set[tuple[str, int]] = set()
        self._unsupported_attributes: set[str] = set()
        self._stored_dead_registers = stored_dead_registers
        self._probe_ran = False

    async def async_close(self):
        """Close modbus connection."""
        await self._modbus.async_close()

    async def setup(self):
        """Modbus and attribute map setup for CTS700 2015 map."""
        _LOGGER.debug("CTS700 legacy setup started")
        success = await self._modbus.async_setup()
        if success:
            await wait_for_modbus_connected(self._modbus)
            _LOGGER.debug("CTS700 legacy Modbus has been setup")
        else:
            await self._modbus.async_close()
            _LOGGER.error("CTS700 legacy Modbus setup was unsuccessful")
            raise ValueError("Modbus setup was unsuccessful")

        probe = await self._read_holding(Reg.tsens1)
        if probe is None:
            await self._modbus.async_close()
            _LOGGER.error("CTS700 legacy probe read failed")
            raise ValueError("CTS700 legacy probe read failed")

        for entity, value in CTS700_LEGACY_ENTITY_MAP.items():
            self._attributes[entity] = value["entity_type"]

        caps = capabilities_for_cts700_legacy()
        self._capabilities = caps
        self._attributes = filter_attributes_by_capabilities(
            self._attributes, CTS700_LEGACY_ENTITY_MAP, caps
        )

        outdoor = await self.get_t1_intake_temperature()
        if outdoor is not None:
            _LOGGER.debug("CTS700 legacy outdoor probe %.1f C", outdoor)
        self._device_sw_ver = "CTS700 2015 map"
        _LOGGER.debug(
            "CTS700 legacy attributes loaded: %s", list(self._attributes.keys())
        )
        _LOGGER.debug("CTS700 legacy capabilities=%s", sorted(caps))

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
                    for attr, regs in PROBE_SPECS["CTS700_LEGACY"].items()
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
                await run_register_probe(self, PROBE_SPECS["CTS700_LEGACY"])
                self._probe_ran = True
            except Exception:  # noqa: BLE001 — probe must never fail setup
                _LOGGER.warning(
                    "CTS700 legacy register probe failed; continuing with core-only setup"
                )

    def get_assigned(self, platform: str):
        """Get platform assignment."""
        slots = self._attributes
        return [key for key, value in slots.items() if value == platform]

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
        """Device hardware version."""
        return self._device_hw_ver

    @property
    def get_device_sw_version(self):
        """Device software version string."""
        return self._device_sw_ver

    @property
    def get_attributes(self):
        """Return device attributes."""
        return self._attributes

    def supports_attribute(self, name: str) -> bool:
        """True when the probed registers for this attribute are alive."""
        return name not in self._unsupported_attributes

    async def _read_holding(self, address: int) -> int | None:
        """Read one holding register as signed int."""
        if ("holding", address) in self._dead_registers:
            return None
        result = await self._modbus.async_pb_call(
            self._unit_id, address, 1, "holding"
        )
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
        result = await self._modbus.async_pb_call(
            self._unit_id, address, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        return None

    async def _write_holding(self, address: int, value: int) -> None:
        """Write one holding register."""
        await self._modbus.async_pb_call(
            self._unit_id, address, [value], "write_registers"
        )

    async def _read_temp(self, address: int) -> float | None:
        """Read temperature with 0.1 scale."""
        value = await self._read_holding(address)
        if value is None:
            return None
        return float(value) / _TEMP_SCALE

    async def _write_temp(
        self, address: int, celsius: float, min_v: float, max_v: float
    ) -> bool:
        """Write temperature with 0.1 scale."""
        if celsius < min_v or celsius > max_v:
            return False
        raw = int(round(celsius * _TEMP_SCALE))
        output = int.from_bytes(
            raw.to_bytes(2, "little", signed=True), "little", signed=False
        )
        await self._write_holding(address, output)
        return True

    async def get_run_state(self) -> bool | None:
        """True when pause mode is inactive."""
        value = await self._read_holding_unsigned(Reg.pause_mode)
        if value is None:
            _LOGGER.error("Could not read get_run_state")
            return None
        return value == 0

    async def set_run_state(self, state: bool) -> None:
        """Clear pause (True) or pause ventilation (False)."""
        await self._write_holding(Reg.pause_mode, 0 if state else 1)

    async def get_operation_mode(self) -> int | None:
        """Return climate-compatible mode (1 heat / 2 cool / 3 auto)."""
        value = await self._read_holding_unsigned(Reg.operation_type)
        if value is None:
            _LOGGER.error("Could not read get_operation_mode")
            return None
        return _PDF_TO_CLIMATE.get(value, 3)

    async def set_operation_mode(self, mode: int) -> bool:
        """Set operating mode from climate codes 1/2/3."""
        if mode not in _CLIMATE_TO_PDF:
            return False
        await self._write_holding(Reg.operation_type, _CLIMATE_TO_PDF[mode])
        return True

    async def get_ventilation_step(self) -> int | None:
        """Get fan speed as climate levels 0-4 from percent 0-100 on 4747."""
        value = await self._read_holding_unsigned(Reg.user_fan_speed)
        if value is None:
            _LOGGER.error("Could not read get_ventilation_step")
            return None
        if value in (101, 102, 103, 104):
            _LOGGER.error(
                "Holding 4747=%s looks like Nordic step encoding; "
                "use board CTS700 Compact P Nordic XL",
                value,
            )
            return None
        if value > 4:
            return min(4, max(0, int(round(value / 25.0))))
        return value

    async def set_ventilation_step(self, mode: int) -> bool:
        """Set fan speed level 0-4 as percent 0/25/50/75/100 on 4747."""
        if mode in (0, 1, 2, 3, 4):
            await self._write_holding(Reg.user_fan_speed, mode * 25)
            return True
        return False

    async def get_control_state(self) -> int | None:
        """Approximate control state from run + operating mode."""
        running = await self.get_run_state()
        if running is None:
            return None
        if not running:
            return 0
        mode = await self.get_operation_mode()
        if mode == 1:
            return 7
        if mode == 2:
            return 8
        return 6

    async def get_control_temperature(self) -> float | None:
        """Prefer master sensor, else T3 extract."""
        value = await self._read_temp(Reg.master_sensor_temperature)
        if value is not None:
            return value
        value = await self._read_temp(Reg.tsens3)
        if value is None:
            _LOGGER.error("Could not read get_control_temperature")
        return value

    async def get_user_temperature_setpoint(self) -> float | None:
        """User room temperature setpoint (4746)."""
        value = await self._read_temp(Reg.user_temperature)
        if value is None:
            _LOGGER.error("Could not read get_user_temperature_setpoint")
        return value

    async def set_user_temperature_setpoint(self, value: float) -> None:
        """Set user room temperature setpoint."""
        await self._write_temp(Reg.user_temperature, value, 5, 50)

    async def get_t1_intake_temperature(self) -> float | None:
        """Temperature sensor 1 (typically outdoor)."""
        return await self._read_temp(Reg.tsens1)

    async def get_t2_inlet_temperature(self) -> float | None:
        """Temperature sensor 2 (typically supply)."""
        return await self._read_temp(Reg.tsens2)

    async def get_t3_exhaust_temperature(self) -> float | None:
        """Temperature sensor 3 (typically extract)."""
        return await self._read_temp(Reg.tsens3)

    async def get_t4_outlet(self) -> float | None:
        """Temperature sensor 4 (often after heat exchanger)."""
        return await self._read_temp(Reg.tsens4)

    async def get_t5_condenser_temperature(self) -> float | None:
        """Temperature sensor 5 (often after heat pump)."""
        return await self._read_temp(Reg.tsens5)

    async def get_t6_evaporator_temperature(self) -> float | None:
        """Temperature sensor 6 (often evaporator)."""
        return await self._read_temp(Reg.tsens6)

    async def get_humidity(self) -> float | None:
        """Humidity sensor (0-100, no 0.1 scale)."""
        value = await self._read_holding_unsigned(Reg.humidity)
        if value is None:
            _LOGGER.error("Could not read get_humidity")
            return None
        return float(value)

    async def get_days_to_air_filter_change(self) -> int | None:
        """Approximate remaining inlet filter days (threshold - passed)."""
        threshold = await self._read_holding_unsigned(Reg.filter_inlet_time_threshold)
        passed = await self._read_holding_unsigned(Reg.filter_inlet_pass_days)
        if threshold is None or passed is None:
            _LOGGER.error("Could not read get_days_to_air_filter_change")
            return None
        return max(0, int(threshold) - int(passed))

    async def get_electric_water_heater_setpoint(self) -> float | None:
        """DHW user setpoint (5548)."""
        return await self._read_temp(Reg.user_temp_dhw)

    async def set_electric_water_heater_setpoint(self, value: float) -> None:
        """Set DHW user setpoint."""
        if value == 0:
            await self._write_holding(Reg.user_temp_dhw, 0)
            return
        await self._write_temp(Reg.user_temp_dhw, value, 10, 65)

    async def get_t11_electric_water_heater_temperature(self) -> float | None:
        """Tank top not uniquely named in 2015 PDF; unavailable."""
        return None

    async def get_electric_water_heater_state(self) -> bool | None:
        """True when heater control output is active."""
        value = await self._read_holding_unsigned(Reg.heater_control)
        if value is None:
            return None
        return bool(value)

    async def get_compressor_water_heater_setpoint(self) -> float | None:
        """Same DHW setpoint register as electric path."""
        return await self.get_electric_water_heater_setpoint()

    async def set_compressor_water_heater_setpoint(self, value: float) -> None:
        """Set shared DHW setpoint."""
        await self.set_electric_water_heater_setpoint(value)

    async def get_t12_compressor_water_heater_temperature(self) -> float | None:
        """Tank bottom not uniquely named in 2015 PDF; unavailable."""
        return None
