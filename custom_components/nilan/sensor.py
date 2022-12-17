"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

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
    TEMP_CELSIUS,
    TIME_DAYS,
)

from .const import DOMAIN, SCAN_INTERVAL_TIME

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

CONTROL_STATES = {
    0: "Off",
    1: "Shift",
    2: "Stop",
    3: "Start",
    4: "Standby",
    5: "Ventilation Stop",
    6: "Ventilation",
    7: "Heating",
    8: "Cooling",
    9: "Hot Water",
    10: "Legionella",
    11: "Cooling + Hot Water",
    12: "Central Heating",
    13: "Defrost",
    14: "Frost Sequre",
    15: "Service",
    16: "Alarm",
    17: "Heating + Hot Water",
}

VENTILATION_STATES = {
    0: "Off",
    1: "Normal",
    2: "Low Humidity",
    3: "High Humidity",
    4: "High CO2",
    5: "Low Room Temperature",
    6: "Low Outdoor Temperature",
}

SEASON_STATES = {
    False: "Winter",
    True: "Summer",
}

AFTER_HEATING_TYPES = {
    0: "No Heater",
    1: "Electrical",
    2: "Electric on Binary Relays",
    3: "Water",
}

USER_MENU_STATES = {
    0: "Closed",
    1: "Open",
    2: "No Off Key",
}

ANODE_STATES = {
    0: "Off",
    1: "OK",
    2: "Service",
    3: "Error",
}

Map = namedtuple(
    "map", "name default_unit device_class state_class entity_category icon enum"
)

ATTRIBUTE_TO_SENSORS = {
    "get_t0_controller_temperature": [
        Map(
            "Controller Board Temperature (T0)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
            None,
        )
    ],
    "get_t1_intake_temperature": [
        Map(
            "Fresh Air Intake Temperature (T1)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t2_inlet_temperature": [
        Map(
            "Supply Air Temperature (T2)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t3_exhaust_temperature": [
        Map(
            "Return Air Temperature (T3)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t4_outlet": [
        Map(
            "Waste Air Temperature (T4)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t5_condenser_temperature": [
        Map(
            "Condenser Temperature (T5)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
            None,
        )
    ],
    "get_t6_evaporator_temperature": [
        Map(
            "Waste Air Temperature (T6)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t7_inlet_temperature_after_heater": [
        Map(
            "Supply Air Temperature (T7)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t8_outdoor_temperature": [
        Map(
            "Fresh Air Intake Temperature (T8)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t10_external_temperature": [
        Map(
            "Return Air Temperature (T10)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t13_return_temperature": [
        Map(
            "Return Water Temperature (T13)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t14_supply_temperature": [
        Map(
            "Supply Water Temperature (T14)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_t15_user_panel_temperature": [
        Map(
            "User Panel Temperature (T15)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
            None,
        )
    ],
    "get_t16_sacrificial_anode_temperature": [
        Map(
            "Anode Temperature (T16)",
            TEMP_CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_humidity": [
        Map(
            "Humidity",
            PERCENTAGE,
            SensorDeviceClass.HUMIDITY,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_air_temp_eff_pct": [
        Map(
            "Exchanger Efficiency",
            PERCENTAGE,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_average_humidity": [
        Map(
            "24h Average Humidity",
            PERCENTAGE,
            SensorDeviceClass.HUMIDITY,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_after_heating_element_capacity": [
        Map(
            "After Heating Element Capacity",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:radiator",
            None,
        )
    ],
    "get_co2_sensor_value": [
        Map(
            "CO2 Sensor",
            CONCENTRATION_PARTS_PER_MILLION,
            SensorDeviceClass.CO2,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_control_state": [
        Map(
            "Control State",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:state-machine",
            CONTROL_STATES,
        )
    ],
    "get_after_heating_type": [
        Map(
            "After Heating Type",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
            AFTER_HEATING_TYPES,
        )
    ],
    "get_time_in_control_state": [
        Map(
            "Time in Control State",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:calendar-clock",
            None,
        )
    ],
    "get_alarm_count": [
        Map(
            "Alarms Active",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:alert-circle-outline",
            None,
        )
    ],
    "get_days_since_air_filter_change": [
        Map(
            "Days Since Air Filter Change",
            TIME_DAYS,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:calendar-start",
            None,
        )
    ],
    "get_days_to_air_filter_change": [
        Map(
            "Days To Air Filter Change",
            TIME_DAYS,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:calendar-end",
            None,
        )
    ],
    "get_summer_state": [
        Map(
            "Climate Season",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:sun-snowflake",
            SEASON_STATES,
        )
    ],
    "get_time": [
        Map(
            "Time",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:calendar-clock",
            None,
        )
    ],
    "get_ventilation_state": [
        Map(
            "Ventilation State",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:state-machine",
            VENTILATION_STATES,
        )
    ],
    "get_user_menu_state": [
        Map(
            "User Menu State",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            USER_MENU_STATES,
        )
    ],
    "get_anode_state": [
        Map(
            "Anode State",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            ANODE_STATES,
        )
    ],
    "get_supply_fan_level": [
        Map(
            "Supply Fan Level",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
            None,
        )
    ],
    "get_return_fan_level": [
        Map(
            "Return Fan Level",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
            None,
        )
    ],
    "get_return_fan_speed": [
        Map(
            "Return Fan Speed",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
            None,
        )
    ],
    "get_supply_fan_speed": [
        Map(
            "Supply Fan Speed",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            "mdi:fan",
            None,
        )
    ],
    "get_display_text_1": [
        Map(
            "Display Text Line 1",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_display_text_2": [
        Map(
            "Display Text Line 2",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            None,
            None,
            None,
        )
    ],
    "get_bus_version": [
        Map(
            "ModBus Version",
            None,
            None,
            SensorStateClass.MEASUREMENT,
            EntityCategory.DIAGNOSTIC,
            None,
            None,
        )
    ],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    device = hass.data[DOMAIN][config_entry.entry_id]
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
                        m.enum,
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
        enum,
    ) -> None:
        """Init Sensor"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._available = True
        self._attr_name = "Nilan: " + name
        self._attr_native_unit_of_measurement = default_unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_entity_category = entity_category
        self._attr_icon = icon
        self._enum = enum
        self._name = name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = self._name.lower().replace(" ", "_")
        return f"{_name}.{_unique_id}"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        if self._enum is not None:
            self._attr_native_value = self._enum.get(
                await getattr(self._device, self._attribute)()
            )
        else:
            self._attr_native_value = await getattr(self._device, self._attribute)()
