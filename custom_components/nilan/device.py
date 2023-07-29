"""implements nilan devices"""
from __future__ import annotations
import datetime

import logging

from homeassistant.components.modbus import modbus
from homeassistant.core import HomeAssistant
from .registers import CTS602InputRegisters, CTS602HoldingRegisters
from .device_map import CTS602_DEVICE_TYPES, CTS602_ENTITY_MAP

_LOGGER = logging.getLogger(__name__)


class Device:
    """Nilan Device"""

    def __init__(
        self,
        hass: HomeAssistant,
        name,
        com_type,
        host_ip: str | None,
        host_port,
        unit_id,
    ) -> None:
        """Create new entity of Device Class"""
        self.hass = hass
        self._device_name = name
        self._device_type = ""
        self._device_sw_ver = ""
        self._device_hw_ver = ""
        self._host_ip = host_ip
        self._host_port = host_port
        self._unit_id = int(unit_id)
        self._com_type = com_type
        self._client_config = {
            "name": self._device_name,
            "type": self._com_type,
            "method": "rtu",
            "delay": 0,
            "port": self._host_port,
            "timeout": 1,
            "close_comm_on_error": "false",
            "retries": 10,
            "retry_on_empty": "true",
            "host": self._host_ip,
            "parity": "E",
            "baudrate": 19200,
            "bytesize": 8,
            "stopbits": 1,
        }
        self._modbus = modbus.ModbusHub(self.hass, self._client_config)
        self._attributes = {}

    async def setup(self):
        """Setup Modbus and attribute map for Nilan Device"""
        hw_type = None
        success = await self._modbus.async_setup()
        if success:
            hw_type = await self.get_machine_type()
            bus_version = await self.get_bus_version()
        if hw_type in CTS602_DEVICE_TYPES:
            self._device_sw_ver = await self.get_controller_software_version()
            self._device_type = CTS602_DEVICE_TYPES[hw_type]
            if bus_version >= 10:  # PH
                co2_present = await self.get_co2_present()
            else:
                co2_present = True
            for entity, value in CTS602_ENTITY_MAP.items():
                if bus_version >= value["min_bus_version"] and (
                    hw_type in value["supported_devices"]
                    or "all" in value["supported_devices"]
                ):
                    if "extra_type" in value:
                        if co2_present and value["extra_type"] == "co2":
                            self._attributes[entity] = value["entity_type"]
                        else:
                            continue
                    if "max_bus_version" in value:
                        if bus_version <= value["max_bus_version"]:
                            self._attributes[entity] = value["entity_type"]
                    else:
                        self._attributes[entity] = value["entity_type"]
        if "get_controller_hardware_version" in self._attributes:
            self._device_hw_ver = await self.get_controller_hardware_version()

    def get_assigned(self, platform: str):
        """get platform assignment"""
        slots = self._attributes
        return [key for key, value in slots.items() if value == platform]

    @property
    def get_device_name(self):
        """device name."""
        return self._device_name

    @property
    def get_device_type(self):
        """device type."""
        return self._device_type

    @property
    def get_device_hw_version(self):
        """device hardware version."""
        return self._device_hw_ver

    @property
    def get_device_sw_version(self):
        """device hardware version."""
        return self._device_sw_ver

    @property
    def get_attributes(self):
        """return device attributes."""
        return self._attributes

    async def get_machine_type(self) -> int:
        """get hardware type."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.control_type, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_machine_type")
        return None

    async def get_bus_version(self) -> int:
        """get modbus version."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.bus_version, 1, "input"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_bus_version")
        return None

    async def get_after_heating_type(self) -> int:
        """get after heating type."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_heat_type, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_after_heating_type")
        return None

    async def get_air_heat_select(self) -> int:
        """get heat source selection."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_temp_heat_select, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_air_heat_select")
        return None

    async def get_controller_software_version(self) -> str:
        """get controller board software version."""
        version = ""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.app_version_major, 3, "input"
        )
        bus_version = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.bus_version, 1, "input"
        )
        if bus_version is not None:
            if int(bus_version.registers[0]) > 19:
                if result is not None:
                    for value in result.registers:
                        char1 = chr(value >> 8)
                        char2 = chr(value & 0x00FF)
                        version += char1 + char2 + "."
                    version = version.replace(" ", "")
                    version = version[:-1]
                    return version
            else:
                if result is not None:
                    for value in result.registers:
                        char1 = chr(value & 0x00FF)
                        char2 = chr(value >> 8)
                        version += char1 + char2
                    version = version.replace(" ", "")
                    return version
        _LOGGER.error("Could not read get_controller_software_version")
        return None

    async def get_controller_hardware_version(self) -> int:
        """get controller board hardware version."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.info_hw_type, 1, "input"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_controller_hardware_version")
        return None

    async def get_display_text_1(self) -> str:
        """get old HMI display text line 1."""
        text_string = ""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.display_text_1_2, 4, "input"
        )
        if result is not None:
            for value in result.registers:
                char1 = value & 0x00FF
                char2 = value >> 8
                if char1 == 0xDF:
                    char1 = "°"
                else:
                    char1 = chr(char1)
                if char2 == 0xDF:
                    char2 = "°"
                else:
                    char2 = chr(char2)
                text_string += char1 + char2
            return text_string
        _LOGGER.error("Could not read get_display_text_1")
        return None

    async def get_display_text_2(self) -> str:
        """get old HMI display text line 2."""
        text_string = ""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.display_text_9_10, 4, "input"
        )
        if result is not None:
            for value in result.registers:
                char1 = value & 0x00FF
                char2 = value >> 8
                if char1 == 0xDF:
                    char1 = "°"
                else:
                    char1 = chr(char1)
                if char2 == 0xDF:
                    char2 = "°"
                else:
                    char2 = chr(char2)
                text_string += char1 + char2
            return text_string
        _LOGGER.error("Could not read get_display_text_2")
        return None

    async def get_user_menu_state(self) -> int:
        """get user menu state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.user_user_menu_open, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_user_menu_state")
        return None

    async def get_anode_state(self) -> int:
        """get user menu state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.hot_water_anode_state, 1, "input"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_anode_state")
        return None

    async def get_supply_air_after_heating(self) -> int:
        """get After heating activation state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_heat_select_set, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_supply_air_after_heating")
        return None

    async def get_supply_power_at_level_1(self) -> int:
        """get supply fan power at level 1."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_inlet_spd_1, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_supply_power_at_level_1")
        return None

    async def get_supply_power_at_level_2(self) -> int:
        """get supply fan power at level 2."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_inlet_spd_2, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_supply_power_at_level_2")
        return None

    async def get_supply_power_at_level_3(self) -> int:
        """get supply fan power at level 3."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_inlet_spd_3, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_supply_power_at_level_3")
        return None

    async def get_supply_power_at_level_4(self) -> int:
        """get supply fan power at level 4."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_inlet_spd_4, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_supply_power_at_level_4")
        return None

    async def get_return_power_at_level_1(self) -> int:
        """get return fan power at level 1."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_exhaust_spd_1, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_return_power_at_level_1")
        return None

    async def get_return_power_at_level_2(self) -> int:
        """get return fan power at level 2."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_exhaust_spd_2, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_return_power_at_level_2")
        return None

    async def get_return_power_at_level_3(self) -> int:
        """get return fan power at level 3."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_exhaust_spd_3, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_return_power_at_level_3")
        return None

    async def get_return_power_at_level_4(self) -> int:
        """get return fan power at level 4."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_exhaust_spd_4, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_return_power_at_level_4")
        return None

    async def get_defrost_ventilation_level(self) -> int:
        """get defrost ventilation level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.defrost_fans, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_defrost_ventilation_level")
        return None

    async def get_central_heat_type(self) -> int:
        """get heat type."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.central_heat_heat_type, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_central_heat_type")
        return None

    async def get_central_heat_select(self) -> int:
        """get central heat select."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.central_heat_heat_select, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
        _LOGGER.error("Could not read get_central_heat_select")
        return None

    async def get_fan_startup_delay(self) -> int:
        """get fan startup delay."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_start_delay, 1, "holding"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_fan_startup_delay")
        return None

    async def get_actual_vent_set(self) -> int:
        """get Actual ventilation step set point."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_flow_vent_set, 1, "input"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_fan_startup_delay")
        return None

    async def get_supply_fan_level(self) -> int:
        """get Actual inlet fan speed step."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_flow_inlet_act, 1, "input"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_supply_fan_level")
        return None

    async def get_return_fan_level(self) -> int:
        """get Actual exhaust fan speed step."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_flow_exhaust_act, 1, "input"
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_return_fan_level")
        return None

    async def get_return_fan_speed(self) -> int:
        """get Actual exhaust fan speed."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_exhaust_speed, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value / 100
        _LOGGER.error("Could not read get_return_fan_speed")
        return None

    async def get_supply_fan_speed(self) -> int:
        """get Actual inlet fan speed."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_inlet_speed, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value / 100
        _LOGGER.error("Could not read get_supply_fan_speed")
        return None

    async def get_co2_low_limit_setpoint(self) -> int:
        """get co2 low limit setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_qual_co2_lim_lo,
            1,
            "holding",
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_co2_low_limit_setpoint")
        return None

    async def get_co2_high_limit_setpoint(self) -> int:
        """get CO2 high limit setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_qual_co2_lim_hi,
            1,
            "holding",
        )
        if result is not None:
            return int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
        _LOGGER.error("Could not read get_co2_high_limit_setpoint")
        return None

    async def get_room_master_temperature(self) -> float:
        """get Master Room Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_temp_temp_room, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_room_master_temperature")
        return None

    async def get_central_heating_setpoint(self) -> float:
        """get Central Heating Temperature Setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.central_heat_heat_ext_set, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_central_heating_setpoint")
        return None

    async def get_exchanger_efficiency(self) -> float:
        """get AirTemp Efficiency Pct"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_temp_eff_pct, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_exchanger_efficiency")
        return None

    async def get_control_temperature(self) -> float:
        """get Control Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_temp_temp_control, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_control_temperature")
        return None

    async def get_after_heating_element_capacity(self) -> float:
        """get After Heating Element Capacity."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.output_air_heat_cap,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_after_heating_element_capacity")
        return None

    async def get_external_heating_offset(self) -> float:
        """get external heating offset."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.central_heat_heat_extern,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_external_heating_offset")
        return None

    async def get_t0_controller_temperature(self) -> float:
        """get T0 Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t0_controller,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t0_controller_temperature")
        return None

    async def get_t1_intake_temperature(self) -> float:
        """get T1 fresh air intake Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t1_intake,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t1_intake_temperature")
        return None

    async def get_t2_inlet_temperature(self) -> float:
        """get T2 inlet Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t2_inlet,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t2_inlet_temperature")
        return None

    async def get_t3_exhaust_temperature(self) -> float:
        """get T3 Exhaust Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t3_exhaust,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t3_exhaust_temperature")
        return None

    async def get_t4_outlet(self) -> float:
        """get T4 Outlet Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t4_outlet,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t4_outlet")
        return None

    async def get_t5_condenser_temperature(self) -> float:
        """get T5 Condenser Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t5_cond, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t5_condenser_temperature")
        return None

    async def get_t6_evaporator_temperature(self) -> float:
        """get T6 evaporator Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t6_evap, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t6_evaporator_temperature")
        return None

    async def get_t7_inlet_temperature_after_heater(self) -> float:
        """get T7 inlet Temperature after heater."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t7_inlet, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t7_inlet_temperature_after_heater")
        return None

    async def get_t8_outdoor_temperature(self) -> float:
        """get T8 Outdoor Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t8_outdoor, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t8_outdoor_temperature")
        return None

    async def get_t9_heater_temperature(self) -> float:
        """get T9 Heater Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t9_heater, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t9_heater_temperature")
        return None

    async def get_t10_external_temperature(self) -> float:
        """get T10 external Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t10_extern,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t10_external_temperature")
        return None

    async def get_t11_electric_water_heater_temperature(self) -> float:
        """get T11 electric water heater temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t11_top,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t11_electric_water_heater_temperature")
        return None

    async def get_t12_compressor_water_heater_temperature(self) -> float:
        """get T12 compressor water heater temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t12_bottom,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t12_compressor_water_heater_temperature")
        return None

    async def get_t13_return_temperature(self) -> float:
        """get T13 Return temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t13_return,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t13_return_temperature")
        return None

    async def get_t14_supply_temperature(self) -> float:
        """get T13 Return temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.input_t14_supply,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t14_supply_temperature")
        return None

    async def get_t15_user_panel_temperature(self) -> float:
        """get T15 user panel Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t15_room, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t15_user_panel_temperature")
        return None

    async def get_t16_sacrificial_anode_temperature(self) -> float:
        """get T16 Sacrificial Anode Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t16, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t16_sacrificial_anode_temperature")
        return None

    async def get_t17_preheater_temperature(self) -> float:
        """get T17 Preheater Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_t17_pre_heat, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_t17_preheater_temperature")
        return None

    async def get_co2_sensor_value(self) -> float:
        """get co2 sensor value."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_qual_co2, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_co2_sensor_value")
        return None

    async def get_average_humidity(self) -> float:
        """get 24h average humidity."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_qual_rh_avg, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_average_humidity")
        return None

    async def get_user_temperature_setpoint(self) -> float:
        """get setpoint Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.control_temp_set,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_user_temperature_setpoint")
        return None

    async def get_defrost_start_setpoint(self) -> float:
        """get defrost start setpoint Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.defrost_temp_start,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_defrost_start_setpoint")
        return None

    async def get_defrost_stop_setpoint(self) -> float:
        """get defrost stop setpoint Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.defrost_temp_stop,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_defrost_stop_setpoint")
        return None

    async def get_low_room_temperature_setpoint(self) -> float:
        """get low room temperature setpoint Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_temp_room_low,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_low_room_temperature_setpoint")
        return None

    async def get_low_temperature_curve(self) -> float:
        """get Low Temperature curve."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.compressor_cond_temp_min,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_low_temperature_curve")
        return None

    async def get_high_temperature_curve(self) -> float:
        """get Hight Temperature curve."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.compressor_cond_temp_max,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_high_temperature_curve")
        return None

    async def get_low_temperature_compressor_start_setpoint(self) -> float:
        """get Compressor low temperature start setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_temp_min_cpr,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_low_temperature_compressor_start_setpoint")
        return None

    async def get_low_outdoor_temperature_setpoint(self) -> float:
        """get low temperature ventilation setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_flow_winter_temp,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value)
        _LOGGER.error("Could not read get_low_outdoor_temperature_setpoint")
        return None

    async def get_scalding_protection_setpoint(self) -> float:
        """get Scalding Protection setpoint Temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.hot_water_temp_cpr_max,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_scalding_protection_setpoint")
        return None

    async def get_user_humidity_setpoint(self) -> float:
        """get Humidity setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_qual_rh_lim_lo,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        return None

    async def get_electric_water_heater_setpoint(self) -> float:
        """get setpoint Humidity"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.hot_water_temp_set_t11,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_electric_water_heater_setpoint")
        return None

    async def get_compressor_water_heater_setpoint(self) -> float:
        """get compressor water heater setpoint temperature."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.hot_water_temp_set_t12,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_compressor_water_heater_setpoint")
        return None

    async def get_ch_min_supply_temperature(self) -> float:
        """get minimum supply air temperature setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.central_heat_supply_min,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_ch_min_supply_temperature")
        return None

    async def get_ch_max_supply_temperature(self) -> float:
        """get max supply air temperature setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.central_heat_supply_max,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_ch_max_supply_temperature")
        return None

    async def get_min_supply_air_summer_setpoint(self) -> float:
        """get minimum supply air temperature setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_temp_min_sum,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_min_supply_air_summer_setpoint")
        return None

    async def get_min_supply_air_winter_setpoint(self) -> float:
        """get minimum supply air winter temperature setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_temp_min_win,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_min_supply_air_winter_setpoint")
        return None

    async def get_max_supply_air_summer_setpoint(self) -> float:
        """get max supply air temperature summer setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_temp_max_sum,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_max_supply_air_summer_setpoint")
        return None

    async def get_max_supply_air_winter_setpoint(self) -> float:
        """get maximum supply air temperature winter"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_temp_max_win,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_max_supply_air_winter_setpoint")
        return None

    async def get_summer_state_change_setpoint(self) -> float:
        """get change to summer state temperature setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_temp_summer,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_summer_state_change_setpoint")
        return None

    async def get_operation_mode(self) -> int:
        """get operation mode."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.control_mode_set, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_operation_mode")
        return None

    async def get_pre_heater_defrost_select(self) -> int:
        """get Select anti frost also during evap. defrost."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.preheat_defrost, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_pre_heater_defrost_select")
        return None

    async def get_pre_heater_temp_set(self) -> int:
        """get Select anti frost start criteria."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.preheat_temp_set, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_pre_heater_temp_set")
        return None

    async def get_high_humidity_step(self) -> int:
        """get High humidity ventilation level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_qual_rh_vent_hi,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_high_humidity_step")
        return None

    async def get_max_high_humidity_vent_time(self) -> int:
        """get time in high ventilation due to high humidity."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_qual_time_out,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_max_high_humidity_vent_time")
        return None

    async def get_supply_heating_pid_time(self) -> int:
        """get pid integration time."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.central_heat_reg_time,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_supply_heating_pid_time")
        return None

    async def get_minimum_defrost_time(self) -> int:
        """get minimum defrost time."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.defrost_t6_min_run_sec,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_minimum_defrost_time")
        return None

    async def get_maximum_outlet_defrost_time(self) -> int:
        """get maximum outlet defrost time in m."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.defrost_dur_max_exh,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_maximum_outlet_defrost_time")
        return None

    async def get_maximum_compressor_defrost_time(self) -> int:
        """get maximum compressor defrost time in m."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.defrost_dur_max_cpr,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_maximum_compressor_defrost_time")
        return None

    async def get_time_between_defrost(self) -> int:
        """get Frost protection or de-icing - Time between activations in m."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.defrost_block_minutes,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_time_between_defrost")
        return None

    async def get_compressor_stop_time(self) -> int:
        """get time that compressor is in stop state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_cpr_restart,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_compressor_stop_time")
        return None

    async def get_hmi_language(self) -> int:
        """get HMI language."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.user_language,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_hmi_language")
        return None

    async def get_circulation_pump_mode(self) -> int:
        """get Circulation Pump Mode."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.central_heat_circ_pump_mode,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_circulation_pump_mode")
        return None

    async def get_low_humidity_step(self) -> int:
        """get low humidity ventilation level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_qual_rh_vent_lo,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return value
        _LOGGER.error("Could not read get_low_humidity_step")
        return None

    async def get_air_quality_control_type(self) -> int:
        """get air quality control type."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_qual_type, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return value
        _LOGGER.error("Could not read get_air_quality_control_type")
        return None

    async def get_cooling_setpoint(self) -> int:
        """get cooling offset setpoint."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_temp_cool_set,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return value
        _LOGGER.error("Could not read get_cooling_setpoint")
        return None

    async def get_cooling_mode_ventilation_step(self) -> int:
        """get cooling mode ventilation level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_cool_vent, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_cooling_mode_ventilation_step")
        return None

    async def get_co2_ventilation_high_step(self) -> int:
        """get CO2 High ventilation step."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_qual_co2_vent_hi,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_co2_ventilation_high_step")
        return None

    async def get_alarm_count(self) -> int:
        """get Alarm Count"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.alarm_status, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value & 0x03
        _LOGGER.error("Could not read get_alarm_count")
        return None

    async def get_legionella_day(self) -> int:
        """get legionella day."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.hot_water_legio_type, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_legionella_day")
        return None

    async def get_air_filter_alarm_interval(self) -> int:
        """get air filter alarm interval setting."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_flow_filt_alm_type,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_air_filter_alarm_interval")
        return None

    async def get_time_in_control_state(self) -> datetime:
        """get Time in Control State"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.control_sec_in_state,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return datetime.timedelta(seconds=value)
        _LOGGER.error("Could not read get_time_in_control_state")
        return None

    async def get_days_since_air_filter_change(self) -> int:
        """get number of days since last air filter change."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.air_flow_since_filt_day,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_days_since_air_filter_change")
        return None

    async def get_days_to_air_filter_change(self) -> int:
        """get Days to next air filter change."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602InputRegisters.air_flow_to_filt_day,
            1,
            "input",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_days_to_air_filter_change")
        return None

    async def get_air_exchange_mode(self) -> int:
        """get air exchange mode."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_air_exch_mode, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return value
        _LOGGER.error("Could not read get_air_exchange_mode")
        return None

    async def get_summer_state(self) -> bool:
        """get summer state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_temp_is_summer, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value:
                return True
            return False
        _LOGGER.error("Could not read get_summer_state")
        return None

    async def get_ventilation_step(self) -> int:
        """get ventilation level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.control_vent_set, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_ventilation_step")
        return None

    async def get_min_supply_step(self) -> int:
        """get minimum air supply level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_inlet_min, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_min_supply_step")
        return None

    async def get_min_return_step(self) -> int:
        """get minimum air return level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_exhaust_min, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_min_return_step")
        return None

    async def get_max_return_step(self) -> int:
        """get Maximum air return level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_flow_exhaust_max, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_max_return_step")
        return None

    async def get_low_outdoor_temperature_ventilation_step(self) -> int:
        """get low outdoor temperature ventilation level."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.air_flow_winter_vent,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_low_outdoor_temperature_ventilation_step")
        return None

    async def get_electric_water_heater_state(self) -> bool:
        """get state of electric water heater."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_water_heat, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value:
                return True
            return False
        _LOGGER.error("Could not read get_electric_water_heater_state")
        return None

    async def get_circulation_pump_state(self) -> bool:
        """get state of ch circulation pump."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_cen_circ_pump, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value:
                return True
            return False
        _LOGGER.error("Could not read get_circulation_pump_state")
        return None

    async def get_heater_relay_1_state(self) -> bool:
        """get state of heater relay 1."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_cen_heat_1, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value:
                return True
            return False
        _LOGGER.error("Could not read get_heater_relay_1_state")
        return None

    async def get_heater_relay_2_state(self) -> bool:
        """get state of heater relay 2."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_cen_heat_2, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value:
                return True
            return False
        _LOGGER.error("Could not read get_heater_relay_2_state")
        return None

    async def get_heater_relay_3_state(self) -> bool:
        """get state of heater relay 3."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_cen_heat_3, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value:
                return True
            return False
        _LOGGER.error("Could not read get_heater_relay_3_state")
        return None

    async def get_compressor_priority(self) -> int:
        """get comressor priority."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.hot_water_priority, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_compressor_priority")
        return None

    async def get_central_heat_supply_curve(self) -> int:
        """get central heating curve."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.central_heat_curve_select,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_central_heat_supply_curve")
        return None

    async def get_supply_heater_delay(self) -> int:
        """get supply heater delay."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.air_heat_delay, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_supply_heater_delay")
        return None

    async def get_ventilation_state(self) -> int:
        """get ventilation state"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_flow_vent_state, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_ventilation_state")
        return None

    async def get_control_state(self) -> int:
        """get control state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.control_state_display, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value
        _LOGGER.error("Could not read get_control_state")
        return None

    async def get_humidity(self) -> float:
        """get humidity"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_qual_rh, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_humidity")
        return None

    async def get_central_heat_supply_curve_offset(self) -> float:
        """get supply curve offset temp."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.central_heat_supply_offset,
            1,
            "holding",
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            return float(value) / 100
        _LOGGER.error("Could not read get_central_heat_supply_curve_offset")
        return None

    async def get_run_state(self) -> bool:
        """Get Run State."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.control_run_set, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_run_state")
        return None

    async def get_alarm_1_code(self) -> int:
        """Get alarm 1 Code"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.alarm_list_1_id, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value & 0x7F
        _LOGGER.error("Could not read get_alarm_1_code")
        return None

    async def get_alarm_2_code(self) -> int:
        """Get alarm 2 Code"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.alarm_list_2_id, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value & 0x7F
        _LOGGER.error("Could not read get_alarm_2_code")
        return None

    async def get_alarm_3_code(self) -> int:
        """Get alarm 3 Code"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.alarm_list_3_id, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            return value & 0x7F
        _LOGGER.error("Could not read get_alarm_3_code")
        return None

    async def get_smoke_alarm_state(self) -> bool:
        """Get smoke alarm State"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_smoke, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_smoke_alarm_state")
        return None

    async def get_user_function_1_state(self) -> bool:
        """Get user function State"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_user_func, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_user_function_1_state")
        return None

    async def get_user_function_2_state(self) -> bool:
        """Get user function 2 State"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.input_user_func_2, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_user_function_2_state")
        return None

    async def get_display_led_1_state(self) -> bool:
        """Get display led 1 State (older models)"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.display_led_1, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_display_led_1_state")
        return None

    async def get_display_led_2_state(self) -> bool:
        """Get display led 2 State (older models)"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.display_led_2, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_display_led_2_state")
        return None

    async def get_compressor_state(self) -> bool:
        """Get compressor State"""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_compressor, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=True,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_compressor_state")
        return None

    async def get_co2_present(self) -> bool:
        """get info of co2 sensor presence."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_qual_co2_enable, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_co2_present")
        return None

    async def get_defrost_state(self) -> bool:
        """get defrost state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.output_defrosting, 1, "holding"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_defrost_state")
        return None

    async def get_bypass_flap_state(self) -> bool:
        """get bypass flap state."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602InputRegisters.air_bypass_is_open, 1, "input"
        )
        if result is not None:
            value = int.from_bytes(
                result.registers[0].to_bytes(2, "little", signed=False),
                "little",
                signed=False,
            )
            if value == 0:
                return False
            return True
        _LOGGER.error("Could not read get_bypass_flap_state")
        return None

    async def get_time(self) -> datetime:
        """Get machine time."""
        result = await self._modbus.async_pymodbus_call(
            self._unit_id, CTS602HoldingRegisters.time_second, 6, "holding"
        )
        if result is not None:
            times = []
            for i in range(6):
                times.append(
                    int.from_bytes(
                        result.registers[i].to_bytes(2, "little", signed=False),
                        "little",
                        signed=False,
                    )
                )
            return datetime.datetime(
                times[5],
                times[4],
                times[3],
                times[2],
                times[1],
                times[0],
            )
        _LOGGER.error("Could not read get_time")
        return None

    async def set_operation_mode(self, mode: int) -> bool:
        """set operation mode."""
        if mode in (1, 2, 3):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.control_mode_set,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_display_button_press(self, mode: int) -> bool:
        """set display button."""
        if mode < 64:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.display_key_code,
                mode,
                "write_registers",
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.display_key_code,
                0,
                "write_registers",
            )
            return True
        return False

    async def set_compressor_priority(self, mode: int) -> bool:
        """set compressor priority."""
        if mode in (0, 1):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.hot_water_priority,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_air_exchange_mode(self, mode: int) -> bool:
        """set air exchange mode."""
        if mode in (0, 1, 2):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_air_exch_mode,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_cooling_mode_ventilation_step(self, mode: int) -> bool:
        """set cooling mode ventilation level."""
        if mode in (0, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_cool_vent,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_cooling_setpoint(self, mode: int) -> bool:
        """set cooling setpoint offset."""
        if mode in (0, 2, 3, 4, 5, 6, 7, 8):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_cool_set,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_ventilation_step(self, mode: int) -> bool:
        """set ventilation level."""
        if mode in (0, 1, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.control_vent_set,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_min_supply_step(self, mode: int) -> bool:
        """set minimum air supply level."""
        if mode in (0, 1, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_inlet_min,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_min_return_step(self, mode: int) -> bool:
        """set minimum air return level."""
        if mode in (1, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_exhaust_min,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_max_return_step(self, mode: int) -> bool:
        """set maximum return level."""
        if mode in (3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_exhaust_max,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_low_humidity_step(self, mode: int) -> bool:
        """set low humidity ventilation level."""
        if mode in (0, 1, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_rh_vent_lo,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_supply_air_after_heating(self, mode: int) -> bool:
        """set After heating activation."""
        if mode in (0, 1):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_heat_select_set,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_high_humidity_step(self, mode: int) -> bool:
        """set high humidity ventilation level."""
        if mode in (0, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_rh_vent_hi,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_co2_ventilation_high_step(self, mode: int) -> bool:
        """set high co2 ventilation level."""
        if mode in (0, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_co2_vent_hi,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_air_quality_control_type(self, mode: int) -> bool:
        """set air quality control type."""
        if mode in (0, 1, 2):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_type,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_air_filter_alarm_interval(self, mode: int) -> bool:
        """set air filter alarm interval."""
        if mode in (0, 1, 2, 3, 4, 5):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_filt_alm_type,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_legionella_day(self, mode: int) -> bool:
        """set legionella day."""
        if mode in (0, 1, 2, 3, 4, 5, 6, 7):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.hot_water_legio_type,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_low_outdoor_temperature_ventilation_step(self, mode: int) -> bool:
        """set low outdoor temp ventilation level."""
        if mode in (0, 1, 2, 3):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_winter_vent,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_defrost_ventilation_level(self, mode: int) -> bool:
        """set defrost ventilation level."""
        if mode in (0, 1, 2):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.defrost_fans,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_central_heat_type(self, mode: int) -> bool:
        """set central heating type."""
        if mode in (0, 1, 2, 3):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_heat_type,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_pre_heater_defrost_select(self, mode: int) -> bool:
        """set Select anti frost also during evap. defrost."""
        if mode in (0, 1):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.preheat_defrost,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_pre_heater_temp_set(self, mode: int) -> bool:
        """set Select anti frost start criteria."""
        if mode in (0, 1, 2, 3, 4, 5):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.preheat_temp_set,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_user_menu_state(self, mode: int) -> bool:
        """set User Menu Access."""
        if mode in (0, 1, 2):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.user_user_menu_open,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_air_heat_select(self, mode: int) -> bool:
        """set air heating."""
        if mode in (0, 1, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_heat_select,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_central_heat_select(self, mode: int) -> bool:
        """set central heating mode."""
        if mode in (0, 1, 2):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_heat_select,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_low_room_temp_ventilation_level(self, mode: int) -> bool:
        """set low room temperature ventilation level."""
        if mode in (0, 1, 2, 3, 4):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_room_low,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_hmi_language(self, mode: int) -> bool:
        """set HMI Language."""
        if mode in (0, 1, 2, 3, 4, 5, 6, 7):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.user_language,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_circulation_pump_mode(self, mode: int) -> bool:
        """set Circulation Pump Mode."""
        if mode in (0, 1):
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_circ_pump_mode,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_alarm_reset_code(self, mode: int) -> bool:
        """set alarm reset code."""
        if mode >= 0 and mode <= 254 or mode == 255:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.alarm_reset,
                mode,
                "write_registers",
            )
            return True
        return False

    async def set_supply_power_at_level_1(self, value: int) -> bool:
        """set supply fan power at level 1."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_inlet_spd_1,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_supply_power_at_level_2(self, value: int) -> bool:
        """set supply fan power at level 2."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_inlet_spd_2,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_supply_power_at_level_3(self, value: int) -> bool:
        """set supply fan power at level 3."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_inlet_spd_3,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_supply_power_at_level_4(self, value: int) -> bool:
        """set supply fan power at level 4."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_inlet_spd_4,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_return_power_at_level_1(self, value: int) -> bool:
        """set return fan power at level 1."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_exhaust_spd_1,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_return_power_at_level_2(self, value: int) -> bool:
        """set return fan power at level 2."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_exhaust_spd_2,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_return_power_at_level_3(self, value: int) -> bool:
        """set return fan power at level 3."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_exhaust_spd_3,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_return_power_at_level_4(self, value: int) -> bool:
        """set return fan power at level 4."""
        if value >= 20 and value <= 100:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_exhaust_spd_4,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_fan_startup_delay(self, value: int) -> bool:
        """set fan start-up delay time in s."""
        if value >= 0 and value <= 240:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_start_delay,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_minimum_defrost_time(self, value: int) -> bool:
        """set minimum defrost time in s."""
        if value >= 10 and value <= 120:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.defrost_t6_min_run_sec,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_maximum_outlet_defrost_time(self, value: int) -> bool:
        """set maximum outlet defrost time in s."""
        if value >= 5 and value <= 60:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.defrost_dur_max_exh,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_maximum_compressor_defrost_time(self, value: int) -> bool:
        """set maximum compressor defrost time in s."""
        if value >= 2 and value <= 60:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.defrost_dur_max_cpr,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_time_between_defrost(self, value: int) -> bool:
        """set Frost protection or de-icing - Time between activations in m."""
        if value >= 15 and value <= 720:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.defrost_dur_max_cpr,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_supply_heater_delay(self, value: int) -> bool:
        """set supply heater delay in m."""
        if value >= 0 and value <= 30:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_heat_delay,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_central_heat_supply_curve(self, value: int) -> bool:
        """set supply heater delay in m."""
        if value >= 1 and value <= 10:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_curve_select,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_compressor_stop_time(self, value: int) -> bool:
        """set compressor stop time in s."""
        if value >= 0 and value <= 3600:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_cpr_restart,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_co2_low_limit_setpoint(self, value: int) -> bool:
        """set co2 low setpoint."""
        if value >= 400 and value <= 750:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_co2_lim_lo,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_co2_high_limit_setpoint(self, value: int) -> bool:
        """set co2 high setpoint."""
        if value >= 650 and value <= 2500:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_co2_lim_hi,
                value,
                "write_registers",
            )
            return True
        return False

    async def set_user_temperature_setpoint(self, value: float):
        """set user hvac temperature setpoint"""
        if value >= 5 and value <= 30:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.control_temp_set,
                output,
                "write_registers",
            )

    async def set_low_temperature_curve(self, value: float):
        """set low temperature curve."""
        if value >= 15 and value <= 46:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.compressor_cond_temp_min,
                output,
                "write_registers",
            )

    async def set_high_temperature_curve(self, value: float):
        """set high temperature curve."""
        if value >= 39 and value <= 60:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.compressor_cond_temp_max,
                output,
                "write_registers",
            )

    async def set_external_heating_offset(self, value: float):
        """set external heating offset."""
        if value >= 0 and value <= 10:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_heat_extern,
                output,
                "write_registers",
            )

    async def set_ch_min_supply_temperature(self, value: float):
        """set min supply temperature."""
        if value >= 5 and value <= 40:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_supply_min,
                output,
                "write_registers",
            )

    async def set_ch_max_supply_temperature(self, value: float):
        """set max supply temperature."""
        if value >= 0 and value <= 100:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_supply_max,
                output,
                "write_registers",
            )

    async def set_central_heat_supply_curve_offset(self, value: float):
        """set supply curve offset."""
        if value >= -15 and value <= 10:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.central_heat_supply_offset,
                output,
                "write_registers",
            )

    async def set_defrost_start_setpoint(self, value: float):
        """set defrost temperature start setpoint."""
        if value >= -10 and value <= 0:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.defrost_temp_start,
                output,
                "write_registers",
            )

    async def set_defrost_stop_setpoint(self, value: float):
        """set defrost stop temperature setpoint."""
        if value >= 2 and value <= 12:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.defrost_temp_stop,
                output,
                "write_registers",
            )

    async def set_low_temperature_compressor_start_setpoint(self, value: float):
        """set low temperature compressor start setpoint."""
        if value >= 0 and value <= 15:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_min_cpr,
                output,
                "write_registers",
            )

    async def set_min_supply_air_summer_setpoint(self, value: float):
        """set minimum supply air temperature summer."""
        if value >= 5 and value <= 16:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_min_sum,
                output,
                "write_registers",
            )

    async def set_min_supply_air_winter_setpoint(self, value: float):
        """set minimum supply air temperature winter."""
        if value >= 14 and value <= 22:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_min_win,
                output,
                "write_registers",
            )

    async def set_max_supply_air_summer_setpoint(self, value: float):
        """set maximum supply air temperature summer."""
        if value >= 16 and value <= 25:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_max_sum,
                output,
                "write_registers",
            )

    async def set_max_supply_air_winter_setpoint(self, value: float):
        """set maximum supply air temperature winter."""
        if value >= 22 and value <= 50:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_max_win,
                output,
                "write_registers",
            )

    async def set_summer_state_change_setpoint(self, value: float):
        """set change to summer state temperature setpoint."""
        if value >= 5 and value <= 30:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_summer,
                output,
                "write_registers",
            )

    async def set_low_outdoor_temperature_setpoint(self, value: float):
        """set low outdoor temperature ventilation temperature setpoint."""
        if value >= -20 and value <= 10:
            value = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_flow_winter_temp,
                value,
                "write_registers",
            )

    async def set_low_room_temperature_setpoint(self, value: float):
        """set low room temperature setpoint."""
        if value >= 0 and value <= 20:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_temp_temp_room_low,
                output,
                "write_registers",
            )

    async def set_scalding_protection_setpoint(self, value: float):
        """set scalding protection temperature setpoint."""
        if value >= 60 and value <= 80:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.hot_water_temp_cpr_max,
                output,
                "write_registers",
            )

    async def set_user_humidity_setpoint(self, value: float):
        """set user humidity setpoint"""
        if value >= 15 and value <= 45:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_rh_lim_lo,
                output,
                "write_registers",
            )

    async def set_max_high_humidity_vent_time(self, value: float):
        """set maximum time in high humidity ventilation in m"""
        if value >= 1 and value <= 180:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_time_out,
                value,
                "write_registers",
            )

    async def set_supply_heating_pid_time(self, value: float):
        """set pid integration time"""
        if value >= 0 and value <= 25:
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.air_qual_time_out,
                value,
                "write_registers",
            )

    async def set_electric_water_heater_setpoint(self, value: float):
        """set electric water heater temperature setpoint."""
        if value >= 5 and value <= 85 or value == 0:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.hot_water_temp_set_t11,
                output,
                "write_registers",
            )

    async def set_compressor_water_heater_setpoint(self, value: float):
        """set compressor water heater temperature setpoint."""
        if value >= 5 and value <= 60 or value == 0:
            value = int(value * 100)
            output = int.from_bytes(
                value.to_bytes(2, "little", signed=True), "little", signed=False
            )
            await self._modbus.async_pymodbus_call(
                self._unit_id,
                CTS602HoldingRegisters.hot_water_temp_set_t12,
                output,
                "write_registers",
            )

    async def set_run_state(self, state: bool):
        """Set Run state."""
        if state:
            value = 1
        else:
            value = 0
        await self._modbus.async_pymodbus_call(
            self._unit_id,
            CTS602HoldingRegisters.control_run_set,
            value,
            "write_registers",
        )
