"""Nilan CTS700 Compact P 2018+ device (Ethernet Modbus TCP MVP).

Fan writes use holding 21771 as percent. Room setpoint 20102, room current
20286. Do not use Nordic 4747 step values 101-104 on this class.
"""

from __future__ import annotations

import logging

from homeassistant.components.modbus import modbus
from homeassistant.core import HomeAssistant

from .capabilities import (
    capabilities_for_cts700,
    filter_attributes_by_capabilities,
)
from .device_map_cts700 import CTS700_ENTITY_MAP
from .modbus_hub_util import build_modbus_hub_name, wait_for_modbus_connected
from .register_probe import (
    PROBE_SPECS,
    deserialize_dead_registers,
    run_register_probe,
)
from .registers import CTS700NewHoldingRegisters

_LOGGER = logging.getLogger(__name__)

# CTS700 temperatures use scale 0.1 (divide by 10).
_TEMP_SCALE = 10


class DeviceCTS700:
    """Nilan CTS700 Compact P device."""

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
        """Create CTS700 device."""
        self.hass = hass
        self._device_name = name
        self._device_type = "Compact P CTS700"
        self._device_sw_ver = "CTS700 Compact P 2018+ map"
        self._device_hw_ver = "CTS700"
        self._host_ip = host_ip
        self._host_port = host_port
        self._unit_id = int(unit_id)
        self._com_type = com_type
        self._hub_name = hub_name or build_modbus_hub_name(
            name, board_type="CTS700", unit_id=self._unit_id
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
        self._board_type = "CTS700"
        self._capabilities = frozenset()
        self._dead_registers: set[tuple[str, int]] = set()
        self._unsupported_attributes: set[str] = set()
        self._stored_dead_registers = stored_dead_registers
        self._probe_ran = False

    async def async_close(self):
        """Close modbus connection."""
        await self._modbus.async_close()

    async def setup(self):
        """Modbus and attribute map setup for CTS700."""
        _LOGGER.debug("CTS700 setup started")
        success = await self._modbus.async_setup()
        if success:
            await wait_for_modbus_connected(self._modbus)
            _LOGGER.debug("CTS700 Modbus has been setup")
        else:
            await self._modbus.async_close()
            _LOGGER.error("CTS700 Modbus setup was unsuccessful")
            raise ValueError("Modbus setup was unsuccessful")

        probe = await self._read_holding(
            CTS700NewHoldingRegisters.t1_outdoor_air_temperature
        )
        if probe is None:
            await self._modbus.async_close()
            _LOGGER.error("CTS700 probe read failed")
            raise ValueError("CTS700 probe read failed")

        for entity, value in CTS700_ENTITY_MAP.items():
            self._attributes[entity] = value["entity_type"]

        caps = capabilities_for_cts700()
        self._capabilities = caps
        self._attributes = filter_attributes_by_capabilities(
            self._attributes, CTS700_ENTITY_MAP, caps
        )

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
                    for attr, regs in PROBE_SPECS["CTS700"].items()
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
                await run_register_probe(self, PROBE_SPECS["CTS700"])
                self._probe_ran = True
            except Exception:  # noqa: BLE001 — probe must never fail setup
                _LOGGER.warning(
                    "CTS700 register probe failed; continuing with core-only setup"
                )

        outdoor = await self.get_t1_intake_temperature()
        if outdoor is not None:
            _LOGGER.debug("CTS700 outdoor probe %.1f C", outdoor)
        self._device_sw_ver = "CTS700 Compact P 2018+ map"
        _LOGGER.debug("CTS700 attributes loaded: %s", list(self._attributes.keys()))
        _LOGGER.debug("CTS700 capabilities=%s", sorted(caps))

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
        """True when ventilation is not paused."""
        value = await self._read_holding_unsigned(
            CTS700NewHoldingRegisters.set_ventilation_on_pause
        )
        if value is None:
            _LOGGER.error("Could not read get_run_state")
            return None
        return value == 0

    async def set_run_state(self, state: bool) -> None:
        """Pause (False) or resume (True) ventilation."""
        await self._write_holding(
            CTS700NewHoldingRegisters.set_ventilation_on_pause, 0 if state else 1
        )

    async def get_operation_mode(self) -> int | None:
        """Get operating mode (1 heat / 2 cool / 3 auto when mapped)."""
        value = await self._read_holding_unsigned(
            CTS700NewHoldingRegisters.operating_mode
        )
        if value is None:
            _LOGGER.error("Could not read get_operation_mode")
        return value

    async def set_operation_mode(self, mode: int) -> bool:
        """Set operating mode."""
        if mode in (0, 1, 2, 3):
            await self._write_holding(CTS700NewHoldingRegisters.operating_mode, mode)
            return True
        return False

    async def get_ventilation_step(self) -> int | None:
        """Get fan speed as climate levels 0-4.

        Compact P holding 21771 is percent (0-100) on live installs, not 0-4.
        """
        value = await self._read_holding_unsigned(CTS700NewHoldingRegisters.fan_speed)
        if value is None:
            _LOGGER.error("Could not read get_ventilation_step")
            return None
        if value > 4:
            return min(4, max(0, int(round(value / 25.0))))
        return value

    async def set_ventilation_step(self, mode: int) -> bool:
        """Set fan speed level 0-4 (writes percent 0/25/50/75/100 to 21771)."""
        if mode in (0, 1, 2, 3, 4):
            await self._write_holding(CTS700NewHoldingRegisters.fan_speed, mode * 25)
            return True
        return False

    async def get_control_state(self) -> int | None:
        """Approximate control state from run + operating mode for climate UI."""
        running = await self.get_run_state()
        if running is None:
            return None
        if not running:
            return 0
        mode = await self.get_operation_mode()
        if mode == 1:
            return 7  # heating
        if mode == 2:
            return 8  # cooling
        return 6  # ventilation

    async def get_control_temperature(self) -> float | None:
        """Room / extract air temperature (Compact P current)."""
        value = await self._read_temp(
            CTS700NewHoldingRegisters.t3_extract_air_temperature
        )
        if value is None:
            _LOGGER.error("Could not read get_control_temperature")
        return value

    async def get_user_temperature_setpoint(self) -> float | None:
        """Room temperature setpoint."""
        value = await self._read_temp(
            CTS700NewHoldingRegisters.room_temperature_setpoint
        )
        if value is None:
            _LOGGER.error("Could not read get_user_temperature_setpoint")
        return value

    async def set_user_temperature_setpoint(self, value: float) -> None:
        """Set room temperature setpoint."""
        await self._write_temp(
            CTS700NewHoldingRegisters.room_temperature_setpoint, value, 5, 30
        )

    async def get_t1_intake_temperature(self) -> float | None:
        """Outdoor air temperature."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t1_outdoor_air_temperature
        )

    async def get_t2_inlet_temperature(self) -> float | None:
        """Supply air temperature."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t2_supply_air_temperature
        )

    async def get_t3_exhaust_temperature(self) -> float | None:
        """Extract / room air temperature."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t3_extract_air_temperature
        )

    async def get_t4_outlet(self) -> float | None:
        """Discharge after heat exchanger."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t4_discharge_air_after_heat_exchanger
        )

    async def get_t5_condenser_temperature(self) -> float | None:
        """Discharge after heat pump."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t5_discharge_air_after_heat_pump
        )

    async def get_t6_evaporator_temperature(self) -> float | None:
        """Evaporator temperature."""
        return await self._read_temp(CTS700NewHoldingRegisters.t6_evaporator_temperature)

    async def get_t8_outdoor_temperature(self) -> float | None:
        """Outdoor air before pre-heater (holding 20296)."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t8_outdoor_air_before_pre_heater
        )

    async def get_humidity(self) -> float | None:
        """Average humidity (no 0.1 scale)."""
        value = await self._read_holding_unsigned(
            CTS700NewHoldingRegisters.average_humidity
        )
        if value is None:
            _LOGGER.error("Could not read get_humidity")
            return None
        return float(value)

    async def get_days_to_air_filter_change(self) -> int | None:
        """Days until filter change."""
        value = await self._read_holding_unsigned(
            CTS700NewHoldingRegisters.air_filter_days_to_filter_change
        )
        if value is None:
            _LOGGER.error("Could not read get_days_to_air_filter_change")
        return value

    async def get_electric_water_heater_setpoint(self) -> float | None:
        """DHW setpoint (shared Compact P register)."""
        return await self._read_temp(CTS700NewHoldingRegisters.hot_water_set_point)

    async def set_electric_water_heater_setpoint(self, value: float) -> None:
        """Set DHW setpoint."""
        if value == 0:
            await self._write_holding(CTS700NewHoldingRegisters.hot_water_set_point, 0)
            return
        await self._write_temp(
            CTS700NewHoldingRegisters.hot_water_set_point, value, 5, 85
        )

    async def get_compressor_water_heater_setpoint(self) -> float | None:
        """Same Compact P DHW setpoint as electric path."""
        return await self.get_electric_water_heater_setpoint()

    async def set_compressor_water_heater_setpoint(self, value: float) -> None:
        """Set shared Compact P DHW setpoint."""
        await self.set_electric_water_heater_setpoint(value)

    async def get_t11_electric_water_heater_temperature(self) -> float | None:
        """Top DHW tank temperature."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t11_top_temperature_in_dhw_water_tank
        )

    async def get_t12_compressor_water_heater_temperature(self) -> float | None:
        """Bottom DHW tank temperature."""
        return await self._read_temp(
            CTS700NewHoldingRegisters.t12_bottom_temperature_in_dhw_water_tank
        )

    async def get_electric_water_heater_state(self) -> bool | None:
        """Electrical supplement heater (holding 20464, 0/1)."""
        value = await self._read_holding_unsigned(
            CTS700NewHoldingRegisters.electrical_supplement_heater
        )
        if value is None:
            _LOGGER.error("Could not read get_electric_water_heater_state")
            return None
        return bool(value)

    async def set_electric_water_heater_state(self, value: bool | int) -> None:
        """Write electrical supplement heater holding 20464 (0/1)."""
        on = 1 if value else 0
        await self._write_holding(
            CTS700NewHoldingRegisters.electrical_supplement_heater, on
        )
