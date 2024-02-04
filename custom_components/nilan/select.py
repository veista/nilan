"""Platform for select integration."""
from __future__ import annotations

from collections import namedtuple

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import EntityCategory

from .__init__ import NilanEntity
from .const import DOMAIN

Map = namedtuple("map", "name set_attr entity_category options icon")

ATTRIBUTE_TO_SELECT = {
    "get_air_filter_alarm_interval": [
        Map(
            "air_filter_alarm_interval",
            "set_air_filter_alarm_interval",
            EntityCategory.CONFIG,
            ["1", "2", "3", "4"],
            "mdi:air-filter",
        )
    ],
    "get_legionella_day": [
        Map(
            "legionella_day",
            "set_legionella_day",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4", "5", "6", "7"],
            "mdi:calendar-today",
        )
    ],
    "get_air_quality_control_type": [
        Map(
            "indoor_air_quality_control",
            "set_air_quality_control_type",
            EntityCategory.CONFIG,
            ["0", "1", "2"],
            "mdi:air-purifier",
        )
    ],
    "get_compressor_priority": [
        Map(
            "compressor_heating_priority",
            "set_compressor_priority",
            EntityCategory.CONFIG,
            ["0", "1"],
            "mdi:priority-high",
        )
    ],
    "get_cooling_mode_ventilation_step": [
        Map(
            "cooling_mode_ventilation_level",
            "set_cooling_mode_ventilation_step",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4"],
            "mdi:fan",
        )
    ],
    "get_cooling_setpoint": [
        Map(
            "cooling_setpoint_offset",
            "set_cooling_setpoint",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4", "5", "6", "7", "8"],
            "mdi:thermometer-lines",
        )
    ],
    "get_low_humidity_step": [
        Map(
            "low_humidity_ventilation_level",
            "set_low_humidity_step",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4"],
            "mdi:fan-chevron-down",
        )
    ],
    "get_high_humidity_step": [
        Map(
            "high_humidity_ventilation_level",
            "set_high_humidity_step",
            EntityCategory.CONFIG,
            ["0", "2", "3", "4"],
            "mdi:fan-chevron-up",
        )
    ],
    "get_hmi_language": [
        Map(
            "hmi_language",
            "set_hmi_language",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "mdi:translate",
        )
    ],
    "get_low_outdoor_temperature_ventilation_step": [
        Map(
            "low_outdoor_temp_ventilation_level",
            "set_low_outdoor_temperature_ventilation_step",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3"],
            "mdi:fan-chevron-down",
        )
    ],
    "get_min_supply_step": [
        Map(
            "minimum_ventilation_supply_level",
            "set_min_supply_step",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4"],
            "mdi:fan",
        )
    ],
    "get_min_return_step": [
        Map(
            "minimum_ventilation_return_level",
            "set_min_return_step",
            EntityCategory.CONFIG,
            ["1", "2", "3", "4"],
            "mdi:fan",
        )
    ],
    "get_max_return_step": [
        Map(
            "maximum_ventilation_return_level",
            "set_max_return_step",
            EntityCategory.CONFIG,
            ["3", "4"],
            "mdi:fan",
        )
    ],
    "get_co2_ventilation_high_step": [
        Map(
            "co2_high_ventilation_level",
            "set_co2_ventilation_high_step",
            EntityCategory.CONFIG,
            ["0", "2", "3", "4"],
            "mdi:fan-chevron-up",
        )
    ],
    "get_defrost_ventilation_level": [
        Map(
            "defrost_ventilation_level",
            "set_defrost_ventilation_level",
            EntityCategory.CONFIG,
            ["0", "1", "2"],
            "mdi:fan",
        )
    ],
    "get_central_heat_type": [
        Map(
            "central_heating_type",
            "set_central_heat_type",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3"],
            "mdi:radiator",
        )
    ],
    "get_central_heat_select": [
        Map(
            "central_heating_mode",
            "set_central_heat_select",
            EntityCategory.CONFIG,
            ["0", "1", "2"],
            "mdi:radiator",
        )
    ],
    "get_air_heat_select": [
        Map(
            "heat_source_select",
            "set_air_heat_select",
            EntityCategory.CONFIG,
            ["0", "1"],
            "mdi:radiator",
        )
    ],
    "get_pre_heater_defrost_select": [
        Map(
            "pre_heating_effect",
            "set_pre_heater_defrost_select",
            EntityCategory.CONFIG,
            ["0", "1"],
            "mdi:snowflake-melt",
        )
    ],
    "get_pre_heater_temp_set": [
        Map(
            "pre_heating_temperature",
            "set_pre_heater_temp_set",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4", "5"],
            "mdi:snowflake-melt",
        )
    ],
    "get_circulation_pump_mode": [
        Map(
            "circulation_pump_mode",
            "set_circulation_pump_mode",
            EntityCategory.CONFIG,
            ["0", "1"],
            "mdi:pump",
        )
    ],
    "get_user_menu_state": [
        Map(
            "user_menu_lock",
            "set_user_menu_state",
            EntityCategory.CONFIG,
            ["0", "1", "2"],
            "mdi:menu",
        )
    ],
}


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Set up the select platform."""
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
    selects = []
    for attribute in device.get_assigned("select"):
        if attribute in ATTRIBUTE_TO_SELECT:
            maps = ATTRIBUTE_TO_SELECT[attribute]
            selects.extend(
                [
                    NilanCTS602Select(
                        device,
                        attribute,
                        m.name,
                        m.set_attr,
                        m.entity_category,
                        m.options,
                        m.icon,
                    )
                    for m in maps
                ]
            )
    if "alarm_reset" in device.get_assigned("select"):
        selects.extend([NilanCTS602AlarmSelect(device)])
    async_add_entities(selects, update_before_add=True)


class NilanCTS602Select(SelectEntity, NilanEntity):
    """Representation of a Select."""

    def __init__(
        self,
        device,
        attribute,
        name,
        set_attr,
        entity_category,
        options,
        icon,
    ) -> None:
        """Init Select"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._set_attr = set_attr
        self._attr_entity_category = entity_category
        self._options = options
        self._attr_icon = icon
        self._name = name
        self._attr_has_entity_name = True
        self._attr_translation_key = self._name
        self._attr_unique_id = self._name

    @property
    def options(self) -> list[str]:
        """Return options."""
        options = []
        for option in self._options:
            options.append(option)
        return options

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await getattr(self._device, self._set_attr)(int(option))

    async def async_update(self) -> None:
        """Fetch new state data for the select."""
        self._attr_current_option = str(await getattr(self._device, self._attribute)())


class NilanCTS602AlarmSelect(SelectEntity, NilanEntity):
    """Representation of an Alarm Select."""

    def __init__(
        self,
        device,
    ) -> None:
        """Init Alarm Select"""
        super().__init__(device)
        self._device = device
        self._available = True
        self._name = "reset_alarm"
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_has_entity_name = True
        self._attr_translation_key = self._name
        self._attr_unique_id = self._name

    @property
    def icon(self) -> str | None:
        """Return an icon."""
        if len(self.options) > 0:
            return "mdi:alert-circle"
        return "mdi:alert-circle-outline"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._device.set_alarm_reset_code(int(option))

    async def async_update(self) -> None:
        """Fetch new state data for the select."""
        self._attr_current_option = None
        self._attr_options = None
        options = []
        option1 = await self._device.get_alarm_1_code()
        option2 = await self._device.get_alarm_2_code()
        option3 = await self._device.get_alarm_3_code()
        if option1 != 0:
            options.append(str(option1))
        if option2 != 0:
            options.append(str(option2))
        if option3 != 0:
            options.append(str(option3))
        if len(options) > 1:
            options.append(str(255))
        self._attr_options = options
