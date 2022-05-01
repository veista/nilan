"""Platform for number integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

from .__init__ import NilanEntity

from homeassistant.helpers.entity import EntityCategory

from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
)

from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    TEMP_CELSIUS,
    TIME_MINUTES,
    TIME_SECONDS,
)

from .const import DOMAIN, SCAN_INTERVAL_TIME


SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

Map = namedtuple(
    "map", "name set_attr entity_category min_value max_value step mode unit icon"
)

ATTRIBUTE_TO_NUMBERS = {
    "get_scalding_protection_setpoint": [
        Map(
            "Scalding Protection Setpoint",
            "set_scalding_setpoint",
            EntityCategory.CONFIG,
            60,
            80,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:coolant-temperature",
        )
    ],
    "get_max_high_humidity_vent_time": [
        Map(
            "Maximum Time in High Humidity Ventilation",
            "set_max_high_humidity_vent_time",
            EntityCategory.CONFIG,
            1,
            180,
            1,
            NumberMode.BOX,
            TIME_MINUTES,
            "mdi:wrench-clock",
        )
    ],
    "get_low_temperature_curve": [
        Map(
            "Low Temperature Curve",
            "set_low_temperature_curve",
            EntityCategory.CONFIG,
            15,
            46,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-chevron-down",
        )
    ],
    "get_high_temperature_curve": [
        Map(
            "High Temperature Curve",
            "set_high_temperature_curve",
            EntityCategory.CONFIG,
            39,
            60,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-chevron-up",
        )
    ],
    "get_low_temperature_compressor_start_setpoint": [
        Map(
            "Low Temperature Compressor Start Setpoint",
            "set_low_temperature_compressor_start_setpoint",
            EntityCategory.CONFIG,
            0,
            15,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_low_outdoor_temperature_setpoint": [
        Map(
            "Low Outdoor Temp Setpoint",
            "set_low_outdoor_temperature_setpoint",
            EntityCategory.CONFIG,
            -20,
            10,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_min_supply_air_summer_setpoint": [
        Map(
            "Minimum Supply Air Temperature in Summer",
            "set_min_supply_air_summer_setpoint",
            EntityCategory.CONFIG,
            5,
            16,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_min_supply_air_winter_setpoint": [
        Map(
            "Minimum Supply Air Temperature in Winter",
            "set_min_supply_air_winter_setpoint",
            EntityCategory.CONFIG,
            14,
            22,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_max_supply_air_summer_setpoint": [
        Map(
            "Maximum Supply Air Temperature in Summer",
            "set_max_supply_air_summer_setpoint",
            EntityCategory.CONFIG,
            16,
            25,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-high",
        )
    ],
    "get_max_supply_air_winter_setpoint": [
        Map(
            "Maximum Supply Air Temperature in Winter",
            "set_max_supply_air_winter_setpoint",
            EntityCategory.CONFIG,
            22,
            50,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-high",
        )
    ],
    "get_summer_state_change_setpoint": [
        Map(
            "Change to Summer State Setpoint",
            "set_summer_state_change_setpoint",
            EntityCategory.CONFIG,
            5,
            30,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:sun-thermometer-outline",
        )
    ],
    "get_supply_power_at_level_1": [
        Map(
            "Supply Fan Power at Level 1",
            "set_supply_power_at_level_1",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_supply_power_at_level_2": [
        Map(
            "Supply Fan Power at Level 2",
            "set_supply_power_at_level_2",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_supply_power_at_level_3": [
        Map(
            "Supply Fan Power at Level 3",
            "set_supply_power_at_level_3",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_supply_power_at_level_4": [
        Map(
            "Supply Fan Power at Level 4",
            "set_supply_power_at_level_4",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_return_power_at_level_1": [
        Map(
            "Return Fan Power at Level 1",
            "set_return_power_at_level_1",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_return_power_at_level_2": [
        Map(
            "Return Fan Power at Level 2",
            "set_return_power_at_level_2",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_return_power_at_level_3": [
        Map(
            "Return Fan Power at Level 3",
            "set_return_power_at_level_3",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_return_power_at_level_4": [
        Map(
            "Return Fan Power at Level 4",
            "set_return_power_at_level_4",
            EntityCategory.CONFIG,
            20,
            100,
            1,
            NumberMode.BOX,
            PERCENTAGE,
            "mdi:brightness-percent",
        )
    ],
    "get_fan_startup_delay": [
        Map(
            "Fan Start-Up Delay",
            "set_fan_startup_delay",
            EntityCategory.CONFIG,
            0,
            240,
            1,
            NumberMode.BOX,
            TIME_SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_defrost_start_setpoint": [
        Map(
            "Defrost Start Setpoint",
            "set_defrost_start_setpoint",
            EntityCategory.CONFIG,
            -10,
            0,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:snowflake-melt",
        )
    ],
    "get_defrost_stop_setpoint": [
        Map(
            "Defrost Stop Setpoint",
            "set_defrost_stop_setpoint",
            EntityCategory.CONFIG,
            2,
            12,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:snowflake-off",
        )
    ],
    "get_minimum_defrost_time": [
        Map(
            "Minimum Defrost Time",
            "set_minimum_defrost_time",
            EntityCategory.CONFIG,
            10,
            120,
            1,
            NumberMode.BOX,
            TIME_SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_compressor_stop_time": [
        Map(
            "Compressor Stop Time",
            "set_compressor_stop_time",
            EntityCategory.CONFIG,
            0,
            3600,
            1,
            NumberMode.BOX,
            TIME_SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_co2_low_limit_setpoint": [
        Map(
            "CO2 Low Limit",
            "set_co2_low_limit_setpoint",
            None,
            400,
            750,
            1,
            NumberMode.SLIDER,
            CONCENTRATION_PARTS_PER_MILLION,
            "mdi:molecule-co2",
        )
    ],
    "get_co2_high_limit_setpoint": [
        Map(
            "CO2 High Limit",
            "set_co2_high_limit_setpoint",
            None,
            650,
            2500,
            1,
            NumberMode.SLIDER,
            CONCENTRATION_PARTS_PER_MILLION,
            "mdi:molecule-co2",
        )
    ],
    "get_low_room_temperature_setpoint": [
        Map(
            "Low Room Temperature Setpoint",
            "set_low_room_temperature_setpoint",
            EntityCategory.CONFIG,
            0,
            20,
            1,
            NumberMode.BOX,
            TEMP_CELSIUS,
            "mdi:thermometer-low",
        )
    ],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the number platform."""
    device = hass.data[DOMAIN][config_entry.entry_id]
    numbers = []
    for attribute in device.get_assigned("number"):
        if attribute in ATTRIBUTE_TO_NUMBERS:
            maps = ATTRIBUTE_TO_NUMBERS[attribute]
            numbers.extend(
                [
                    NilanCTS602Number(
                        device,
                        attribute,
                        m.name,
                        m.set_attr,
                        m.entity_category,
                        m.min_value,
                        m.max_value,
                        m.step,
                        m.mode,
                        m.unit,
                        m.icon,
                    )
                    for m in maps
                ]
            )
    async_add_entities(numbers, update_before_add=True)


class NilanCTS602Number(NumberEntity, NilanEntity):
    """Representation of a Number."""

    def __init__(
        self,
        device,
        attribute,
        name,
        set_attr,
        entity_category,
        min_value,
        max_value,
        step,
        mode,
        unit,
        icon,
    ) -> None:
        """Init Number"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._available = True
        self._attr_name = "Nilan: " + name
        self._set_attr = set_attr
        self._attr_entity_category = entity_category
        self._attr_min_value = min_value
        self._attr_max_value = max_value
        self._attr_step = step
        self._attr_mode = mode
        self._attr_unit_of_measurement = unit
        self._attr_icon = icon
        self._name = name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = self._name.lower().replace(" ", "_")
        return f"{_name}.{_unique_id}"

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""
        await getattr(self._device, self._set_attr)(int(value))

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_value = await getattr(self._device, self._attribute)()
