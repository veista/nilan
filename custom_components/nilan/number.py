"""Platform for number integration."""
from __future__ import annotations

from collections import namedtuple

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.helpers.entity import EntityCategory

from .__init__ import NilanEntity
from .const import DOMAIN

Map = namedtuple(
    "map", "name set_attr entity_category min_value max_value step mode unit icon"
)

ATTRIBUTE_TO_NUMBERS = {
    "get_scalding_protection_setpoint": [
        Map(
            "scalding_protection_setpoint",
            "set_scalding_protection_setpoint",
            EntityCategory.CONFIG,
            60,
            80,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:coolant-temperature",
        )
    ],
    "get_max_high_humidity_vent_time": [
        Map(
            "maximum_time_in_high_humidity_ventilation",
            "set_max_high_humidity_vent_time",
            EntityCategory.CONFIG,
            1,
            180,
            1,
            NumberMode.BOX,
            UnitOfTime.MINUTES,
            "mdi:wrench-clock",
        )
    ],
    "get_low_temperature_curve": [
        Map(
            "low_temperature_curve",
            "set_low_temperature_curve",
            EntityCategory.CONFIG,
            15,
            46,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-chevron-down",
        )
    ],
    "get_high_temperature_curve": [
        Map(
            "high_temperature_curve",
            "set_high_temperature_curve",
            EntityCategory.CONFIG,
            39,
            60,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-chevron-up",
        )
    ],
    "get_low_temperature_compressor_start_setpoint": [
        Map(
            "low_temperature_compressor_start_setpoint",
            "set_low_temperature_compressor_start_setpoint",
            EntityCategory.CONFIG,
            0,
            15,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_low_outdoor_temperature_setpoint": [
        Map(
            "low_outdoor_temp_setpoint",
            "set_low_outdoor_temperature_setpoint",
            EntityCategory.CONFIG,
            -20,
            10,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_min_supply_air_summer_setpoint": [
        Map(
            "minimum_supply_air_temperature_in_summer",
            "set_min_supply_air_summer_setpoint",
            EntityCategory.CONFIG,
            5,
            50,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_min_supply_air_winter_setpoint": [
        Map(
            "minimum_supply_air_temperature_in_winter",
            "set_min_supply_air_winter_setpoint",
            EntityCategory.CONFIG,
            5,
            50,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_max_supply_air_summer_setpoint": [
        Map(
            "maximum_supply_air_temperature_in_summer",
            "set_max_supply_air_summer_setpoint",
            EntityCategory.CONFIG,
            5,
            50,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-high",
        )
    ],
    "get_max_supply_air_winter_setpoint": [
        Map(
            "maximum_supply_air_temperature_in_winter",
            "set_max_supply_air_winter_setpoint",
            EntityCategory.CONFIG,
            5,
            50,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-high",
        )
    ],
    "get_external_heating_offset": [
        Map(
            "room_temperature_neutral_zone",
            "set_external_heating_offset",
            EntityCategory.CONFIG,
            0,
            10,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-lines",
        )
    ],
    "get_summer_state_change_setpoint": [
        Map(
            "change_to_summer_state_setpoint",
            "set_summer_state_change_setpoint",
            EntityCategory.CONFIG,
            5,
            30,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:sun-thermometer-outline",
        )
    ],
    "get_supply_power_at_level_1": [
        Map(
            "supply_fan_power_at_level_1",
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
            "supply_fan_power_at_level_2",
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
            "supply_fan_power_at_level_3",
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
            "supply_fan_power_at_level_4",
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
            "return_fan_power_at_level_1",
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
            "return_fan_power_at_level_2",
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
            "return_fan_power_at_level_3",
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
            "return_fan_power_at_level_4",
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
            "fan_start_up_delay",
            "set_fan_startup_delay",
            EntityCategory.CONFIG,
            0,
            240,
            1,
            NumberMode.BOX,
            UnitOfTime.SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_defrost_start_setpoint": [
        Map(
            "defrost_start_setpoint",
            "set_defrost_start_setpoint",
            EntityCategory.CONFIG,
            -10,
            0,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:snowflake-melt",
        )
    ],
    "get_defrost_stop_setpoint": [
        Map(
            "defrost_stop_setpoint",
            "set_defrost_stop_setpoint",
            EntityCategory.CONFIG,
            2,
            12,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:snowflake-off",
        )
    ],
    "get_minimum_defrost_time": [
        Map(
            "minimum_defrost_time",
            "set_minimum_defrost_time",
            EntityCategory.CONFIG,
            10,
            120,
            1,
            NumberMode.BOX,
            UnitOfTime.SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_maximum_compressor_defrost_time": [
        Map(
            "maximum_evaporator_defrost_time",
            "set_maximum_compressor_defrost_time",
            EntityCategory.CONFIG,
            2,
            60,
            1,
            NumberMode.BOX,
            UnitOfTime.MINUTES,
            "mdi:wrench-clock",
        )
    ],
    "get_maximum_outlet_defrost_time": [
        Map(
            "maximum_outlet_defrost_time",
            "set_maximum_outlet_defrost_time",
            EntityCategory.CONFIG,
            5,
            60,
            1,
            NumberMode.BOX,
            UnitOfTime.MINUTES,
            "mdi:wrench-clock",
        )
    ],
    "get_time_between_defrost": [
        Map(
            "time_between_defrost_cycles",
            "set_time_between_defrost",
            EntityCategory.CONFIG,
            15,
            720,
            1,
            NumberMode.BOX,
            UnitOfTime.MINUTES,
            "mdi:wrench-clock",
        )
    ],
    "get_supply_heating_pid_time": [
        Map(
            "supply_air_pid_integration_time",
            "set_supply_heating_pid_time",
            EntityCategory.CONFIG,
            0,
            25,
            1,
            NumberMode.BOX,
            UnitOfTime.SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_compressor_stop_time": [
        Map(
            "compressor_stop_time",
            "set_compressor_stop_time",
            EntityCategory.CONFIG,
            0,
            3600,
            1,
            NumberMode.BOX,
            UnitOfTime.SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_co2_low_limit_setpoint": [
        Map(
            "co2_low_limit",
            "set_co2_low_limit_setpoint",
            EntityCategory.CONFIG,
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
            "co2_high_limit",
            "set_co2_high_limit_setpoint",
            EntityCategory.CONFIG,
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
            "low_room_temperature_setpoint",
            "set_low_room_temperature_setpoint",
            EntityCategory.CONFIG,
            0,
            20,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_central_heat_supply_curve_offset": [
        Map(
            "supply_heater_curve_offset",
            "set_central_heat_supply_curve_offset",
            EntityCategory.CONFIG,
            -15,
            10,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-lines",
        )
    ],
    "get_ch_min_supply_temperature": [
        Map(
            "central_heating_min_supply_temperature",
            "set_ch_min_supply_temperature",
            EntityCategory.CONFIG,
            5,
            40,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-low",
        )
    ],
    "get_ch_max_supply_temperature": [
        Map(
            "central_heating_max_supply_temperature",
            "set_ch_max_supply_temperature",
            EntityCategory.CONFIG,
            20,
            70,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer-high",
        )
    ],
    "get_central_heat_supply_curve": [
        Map(
            "outdoor_temperature_compensation_curve",
            "set_central_heat_supply_curve",
            EntityCategory.CONFIG,
            1,
            10,
            1,
            NumberMode.BOX,
            None,
            "mdi:chart-bell-curve-cumulative",
        )
    ],
    "get_supply_heater_delay": [
        Map(
            "supply_heater_delay",
            "set_supply_heater_delay",
            EntityCategory.CONFIG,
            0,
            30,
            1,
            NumberMode.BOX,
            UnitOfTime.SECONDS,
            "mdi:wrench-clock",
        )
    ],
    "get_hps_water_heater_setpoint": [
        Map(
            "hps_water_heater_setpoint",
            "set_hps_water_heater_setpoint",
            None,
            5,
            70,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer",
        )
    ],
    "get_hps_heating_setpoint_min": [
        Map(
            "hps_heating_setpoint_min",
            "set_hps_heating_setpoint_min",
            None,
            0,
            70,
            1,
            NumberMode.BOX,
            UnitOfTemperature.CELSIUS,
            "mdi:thermometer",
        )
    ],
}


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Set up the number platform."""
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
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
        """Init Number."""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._set_attr = set_attr
        self._attr_entity_category = entity_category
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_mode = mode
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._name = name
        self._attr_translation_key = self._name
        self._attr_has_entity_name = True
        self._attr_unique_id = self._name

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await getattr(self._device, self._set_attr)(int(value))

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = await getattr(self._device, self._attribute)()
