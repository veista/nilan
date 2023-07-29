"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

from homeassistant.helpers.typing import UndefinedType

from .__init__ import NilanEntity

from homeassistant.helpers.entity import EntityCategory

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfTime,
)

from .const import DOMAIN, SCAN_INTERVAL_TIME

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

Map = namedtuple(
    "map", "name default_unit device_class state_class entity_category icon"
)

ATTRIBUTE_TO_SENSORS = {
    "get_t0_controller_temperature": [
        Map(
            "controller_board_temperature_t0",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
        )
    ],
    "get_t1_intake_temperature": [
        Map(
            "fresh_air_intake_temperature_t1",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t2_inlet_temperature": [
        Map(
            "supply_air_temperature_t2",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t3_exhaust_temperature": [
        Map(
            "return_air_temperature_t3",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t4_outlet": [
        Map(
            "waste_air_temperature_t4",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t5_condenser_temperature": [
        Map(
            "condenser_temperature_t5",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
        )
    ],
    "get_t6_evaporator_temperature": [
        Map(
            "waste_air_temperature_t6",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t7_inlet_temperature_after_heater": [
        Map(
            "supply_air_temperature_t7",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t8_outdoor_temperature": [
        Map(
            "fresh_air_intake_temperature_t8",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t10_external_temperature": [
        Map(
            "return_air_temperature_t10",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t13_return_temperature": [
        Map(
            "return_water_temperature_t13",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t14_supply_temperature": [
        Map(
            "supply_water_temperature_t14",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_t15_user_panel_temperature": [
        Map(
            "user_panel_temperature_t15",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
        )
    ],
    "get_t16_sacrificial_anode_temperature": [
        Map(
            "anode_temperature_t16",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_central_heating_setpoint": [
        Map(
            "central_heating_setpoint",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_humidity": [
        Map(
            "humidity",
            PERCENTAGE,
            SensorDeviceClass.HUMIDITY,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_average_humidity": [
        Map(
            "24h_average_humidity",
            PERCENTAGE,
            SensorDeviceClass.HUMIDITY,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_after_heating_element_capacity": [
        Map(
            "after_heating_element_capacity",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:radiator",
        )
    ],
    "get_co2_sensor_value": [
        Map(
            "co2_sensor",
            CONCENTRATION_PARTS_PER_MILLION,
            SensorDeviceClass.CO2,
            SensorStateClass.MEASUREMENT,
            None,
            None,
        )
    ],
    "get_control_state": [
        Map(
            "control_state",
            None,
            None,
            None,
            None,
            "mdi:state-machine",
        )
    ],
    "get_after_heating_type": [
        Map(
            "after_heating_type",
            None,
            None,
            None,
            EntityCategory.DIAGNOSTIC,
            None,
        )
    ],
    "get_time_in_control_state": [
        Map(
            "time_in_control_state",
            None,
            None,
            None,
            None,
            "mdi:calendar-clock",
        )
    ],
    "get_alarm_count": [
        Map(
            "alarms_active",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:alert-circle-outline",
        )
    ],
    "get_days_since_air_filter_change": [
        Map(
            "days_since_air_filter_change",
            UnitOfTime.DAYS,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:calendar-start",
        )
    ],
    "get_days_to_air_filter_change": [
        Map(
            "days_to_air_filter_change",
            UnitOfTime.DAYS,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:calendar-end",
        )
    ],
    "get_summer_state": [
        Map(
            "climate_season",
            None,
            None,
            None,
            None,
            "mdi:sun-snowflake",
        )
    ],
    "get_exchanger_efficiency": [
        Map(
            "exchanger_efficiency",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:air-filter",
        )
    ],
    "get_time": [
        Map(
            "time",
            None,
            None,
            None,
            None,
            "mdi:calendar-clock",
        )
    ],
    "get_ventilation_state": [
        Map(
            "ventilation_state",
            None,
            None,
            None,
            None,
            "mdi:state-machine",
        )
    ],
    "get_anode_state": [
        Map(
            "anode_state",
            None,
            None,
            None,
            None,
            None,
        )
    ],
    "get_supply_fan_level": [
        Map(
            "supply_fan_level",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
        )
    ],
    "get_return_fan_level": [
        Map(
            "return_fan_level",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
        )
    ],
    "get_return_fan_speed": [
        Map(
            "return_fan_speed",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
        )
    ],
    "get_supply_fan_speed": [
        Map(
            "supply_fan_speed",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
        )
    ],
    "get_display_text_1": [
        Map(
            "display_text_line_1",
            None,
            None,
            None,
            None,
            None,
        )
    ],
    "get_display_text_2": [
        Map(
            "display_text_line_2",
            None,
            None,
            None,
            None,
            None,
        )
    ],
    "get_bus_version": [
        Map(
            "modbus_version",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
        )
    ],
}


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Set up the sensor platform."""
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
    sensors = []
    for attribute in device.get_assigned("sensor"):
        if attribute in ATTRIBUTE_TO_SENSORS:
            maps = ATTRIBUTE_TO_SENSORS[attribute]
            sensors.extend(
                [
                    NilanCTS602Sensor(
                        device,
                        attribute,
                        m.name,
                        m.default_unit,
                        m.device_class,
                        m.state_class,
                        m.entity_category,
                        m.icon,
                    )
                    for m in maps
                ]
            )
    async_add_entities(sensors, update_before_add=True)


class NilanCTS602Sensor(SensorEntity, NilanEntity):
    """Representation of a Sensor."""

    def __init__(
        self,
        device,
        attribute,
        name,
        default_unit,
        device_class,
        state_class,
        entity_category,
        icon,
    ) -> None:
        """Init Sensor"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._available = True
        self._attr_native_unit_of_measurement = default_unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_entity_category = entity_category
        self._attr_icon = icon
        self._name = name
        self._attr_has_entity_name = True
        self._attr_translation_key = self._name
        self._attr_unique_id = self._name

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = await getattr(self._device, self._attribute)()
