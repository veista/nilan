"""Platform for select integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

from .__init__ import NilanEntity

from homeassistant.helpers.entity import EntityCategory

from homeassistant.components.select import (
    SelectEntity,
)

from .const import ALARM_CODES_TO_TEXT, DOMAIN, SCAN_INTERVAL_TIME, TEXT_TO_ALARM_CODES

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

NUMBER_TO_AIR_FILTER_INTERVAL = {
    1: "30 Days",
    2: "90 Days",
    3: "180 Days",
    4: "360 Days",
}

AIR_FILTER_INTERVAL_TO_NUMBER = {
    "30 Days": 1,
    "90 Days": 2,
    "180 Days": 3,
    "360 Days": 4,
}

NUMBER_TO_DAY = {
    0: "Off",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}

DAY_TO_NUMBER = {
    "Off": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7,
}

IAQ_TYPE_TO_NUMBER = {
    "Off": 0,
    "Humidity": 1,
    "Humidity + CO2": 2,
}

NUMBER_TO_IAQ_TYPE = {
    0: "Off",
    1: "Humidity",
    2: "Humidity + CO2",
}

COMPRESSOR_PRIORITY_TO_NUMBER = {
    "Water": 0,
    "Air": 1,
}

NUMBER_TO_COMPRESSOR_PRIORITY = {
    0: "Water",
    1: "Air",
}

COOLING_SETPOINT_TO_NUMBER = {
    "Cooling Disabled": 0,
    "+1 ºC": 2,
    "+2 ºC": 3,
    "+3 ºC": 4,
    "+4 ºC": 5,
    "+5 ºC": 6,
    "+7 ºC": 7,
    "+10 ºC": 8,
}

NUMBER_TO_COOLING_SETPOINT = {
    0: "Cooling Disabled",
    2: "+1 ºC",
    3: "+2 ºC",
    4: "+3 ºC",
    5: "+4 ºC",
    6: "+5 ºC",
    7: "+7 ºC",
    8: "+10 ºC",
}

COOLING_STEP_TO_NUMBER = {
    "No Change": 0,
    "2": 2,
    "3": 3,
    "4": 4,
}

NUMBER_TO_COOLING_STEP = {
    0: "No Change",
    2: "2",
    3: "3",
    4: "4",
}

HMI_LANGUAGE_TO_NUMBER = {
    "English": 0,
    "German": 1,
    "French": 2,
    "Swedish": 3,
    "Danish": 4,
    "Norwegian": 5,
    "Finnish": 6,
    "Czech": 7,
    "Polish": 8,
    "Italian": 9,
}

NUMBER_TO_HMI_LANGUAGE = {
    0: "English",
    1: "German",
    2: "French",
    3: "Swedish",
    4: "Danish",
    5: "Norwegian",
    6: "Finnish",
    7: "Czech",
    8: "Polish",
    9: "Italian",
}

NUMBER_TO_CENTRAL_HEAT_TYPE = {
    0: "Off",
    1: "Electric",
    2: "Heatpump",
    3: "Both",
}

CENTRAL_HEAT_TYPE_TO_NUMBER = {
    "Off": 0,
    "Electric": 1,
    "Heatpump": 2,
    "Both": 3,
}

NUMBER_TO_CENTRAL_HEAT_SELECT = {
    0: "Off",
    1: "Heating",
    2: "Requirement",
}

CENTRAL_HEAT_SELECT_TO_NUMBER = {
    "Off": 0,
    "Heating": 1,
    "Requirement": 2,
}

NUMBER_TO_AIR_TEMP_HEAT_SELECT = {
    0: "Off",
    1: "HP",
    # 2: "HP + Afterheat",
    # 3: "Afterheat",
    # 4: "Afterheat + HP",
}

AIR_TEMP_HEAT_SELECT_TO_NUMBER = {
    "Off": 0,
    "HP": 1,
    # "HP + Afterheat": 2,
    # "Afterheat": 3,
    # "Afterheat + HP": 4,
}
NUMBER_TO_CIRCULATION_PUMP_MODE = {
    0: "Energy",
    1: "Continuous",
}
CIRCULATION_PUMP_MODE_TO_NUMBER = {
    "Energy": 0,
    "Continuous": 1,
}

NUMBER_TO_USER_MENU_STATE = {
    0: "Locked",
    1: "Open",
    2: "Disable Off Key",
}

USER_MENU_STATE_TO_NUMBER = {
    "Locked": 0,
    "Open": 1,
    "Disable Off Key": 2,
}


NUMBER_TO_DEFROST_VENTILATION = {0: "None", 1: "Constant Flow", 2: "Low Flow"}

DEFROST_VENTILATION_TO_NUMBER = {
    "None": 0,
    "Constant Flow": 1,
    "Low Flow": 2,
}

PRE_HEATER_EFFECT_TO_NUMBER = {
    "Standard": 0,
    "Extra": 1,
}
NUMBER_TO_PRE_HEATER_EFFECT = {
    0: "Standard",
    1: "Extra",
}

PRE_HEATER_TEMP_TO_NUMBER = {
    "Off": 0,
    "1 ºC": 1,
    "2 ºC": 2,
    "3 ºC": 3,
    "4 ºC": 4,
    "5 ºC": 5,
}

NUMBER_TO_PRE_HEATER_TEMP = {
    0: "Off",
    1: "1 ºC",
    2: "2 ºC",
    3: "3 ºC",
    4: "4 ºC",
    5: "5 ºC",
}


Map = namedtuple("map", "name set_attr entity_category options enum icon")

ATTRIBUTE_TO_SELECT = {
    "get_air_filter_alarm_interval": [
        Map(
            "Air Filter Alarm Interval",
            "set_air_filter_alarm_interval",
            EntityCategory.CONFIG,
            AIR_FILTER_INTERVAL_TO_NUMBER,
            NUMBER_TO_AIR_FILTER_INTERVAL,
            "mdi:air-filter",
        )
    ],
    "get_legionella_day": [
        Map(
            "Legionella Day",
            "set_legionella_day",
            EntityCategory.CONFIG,
            DAY_TO_NUMBER,
            NUMBER_TO_DAY,
            "mdi:calendar-today",
        )
    ],
    "get_air_quality_control_type": [
        Map(
            "Indoor Air Quality Control",
            "set_air_quality_control_type",
            EntityCategory.CONFIG,
            IAQ_TYPE_TO_NUMBER,
            NUMBER_TO_IAQ_TYPE,
            "mdi:air-purifier",
        )
    ],
    "get_compressor_priority": [
        Map(
            "Compressor Heating Priority",
            "set_compressor_priority",
            EntityCategory.CONFIG,
            COMPRESSOR_PRIORITY_TO_NUMBER,
            NUMBER_TO_COMPRESSOR_PRIORITY,
            "mdi:priority-high",
        )
    ],
    "get_cooling_mode_ventilation_step": [
        Map(
            "Cooling Mode Ventilation Level",
            "set_cooling_mode_ventilation_step",
            EntityCategory.CONFIG,
            COOLING_STEP_TO_NUMBER,
            NUMBER_TO_COOLING_STEP,
            "mdi:fan",
        )
    ],
    "get_cooling_setpoint": [
        Map(
            "Cooling Setpoint Offset",
            "set_cooling_setpoint",
            EntityCategory.CONFIG,
            COOLING_SETPOINT_TO_NUMBER,
            NUMBER_TO_COOLING_SETPOINT,
            "mdi:thermometer-lines",
        )
    ],
    "get_low_humidity_step": [
        Map(
            "Low Humidity Ventilation Level",
            "set_low_humidity_step",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4"],
            None,
            "mdi:fan-chevron-down",
        )
    ],
    "get_high_humidity_step": [
        Map(
            "High Humidity Ventilation Level",
            "set_high_humidity_step",
            EntityCategory.CONFIG,
            ["0", "2", "3", "4"],
            None,
            "mdi:fan-chevron-up",
        )
    ],
    "get_hmi_language": [
        Map(
            "HMI Language",
            "set_hmi_language",
            EntityCategory.CONFIG,
            HMI_LANGUAGE_TO_NUMBER,
            NUMBER_TO_HMI_LANGUAGE,
            "mdi:translate",
        )
    ],
    "get_low_outdoor_temperature_ventilation_step": [
        Map(
            "Low Outdoor Temp Ventilation Level",
            "set_low_outdoor_temperature_ventilation_step",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3"],
            None,
            "mdi:fan-chevron-down",
        )
    ],
    "get_min_supply_step": [
        Map(
            "Minimum Ventilation Supply Level",
            "set_min_supply_step",
            EntityCategory.CONFIG,
            ["0", "1", "2", "3", "4"],
            None,
            "mdi:fan",
        )
    ],
    "get_min_return_step": [
        Map(
            "Minimum Ventilation Return Level",
            "set_min_return_step",
            EntityCategory.CONFIG,
            ["1", "2", "3", "4"],
            None,
            "mdi:fan",
        )
    ],
    "get_max_return_step": [
        Map(
            "Maximum Ventilation Return Level",
            "set_max_return_step",
            EntityCategory.CONFIG,
            ["3", "4"],
            None,
            "mdi:fan",
        )
    ],
    "get_co2_ventilation_high_step": [
        Map(
            "CO2 High Ventilation Level",
            "set_co2_ventilation_high_step",
            EntityCategory.CONFIG,
            ["0", "2", "3", "4"],
            None,
            "mdi:fan-chevron-up",
        )
    ],
    "get_defrost_ventilation_level": [
        Map(
            "Defrost Ventilation Level",
            "set_defrost_ventilation_level",
            EntityCategory.CONFIG,
            DEFROST_VENTILATION_TO_NUMBER,
            NUMBER_TO_DEFROST_VENTILATION,
            "mdi:fan",
        )
    ],
    "get_central_heat_type": [
        Map(
            "Central Heating Type",
            "set_central_heat_type",
            EntityCategory.CONFIG,
            CENTRAL_HEAT_TYPE_TO_NUMBER,
            NUMBER_TO_CENTRAL_HEAT_TYPE,
            "mdi:radiator",
        )
    ],
    "get_central_heat_select": [
        Map(
            "After Heating Mode",
            "set_central_heat_select",
            EntityCategory.CONFIG,
            CENTRAL_HEAT_SELECT_TO_NUMBER,
            NUMBER_TO_CENTRAL_HEAT_SELECT,
            "mdi:radiator",
        )
    ],
    "get_air_heat_select": [
        Map(
            "Heat Source Select",
            "set_air_heat_select",
            EntityCategory.CONFIG,
            AIR_TEMP_HEAT_SELECT_TO_NUMBER,
            NUMBER_TO_AIR_TEMP_HEAT_SELECT,
            "mdi:radiator",
        )
    ],
    "get_pre_heater_defrost_select": [
        Map(
            "Pre-Heating Effect",
            "set_pre_heater_defrost_select",
            EntityCategory.CONFIG,
            PRE_HEATER_EFFECT_TO_NUMBER,
            NUMBER_TO_PRE_HEATER_EFFECT,
            "mdi:snowflake-melt",
        )
    ],
    "get_pre_heater_temp_set": [
        Map(
            "Pre-Heating Temperature",
            "set_pre_heater_temp_set",
            EntityCategory.CONFIG,
            PRE_HEATER_TEMP_TO_NUMBER,
            NUMBER_TO_PRE_HEATER_TEMP,
            "mdi:snowflake-melt",
        )
    ],
    "get_circulation_pump_mode": [
        Map(
            "Circulation Pump Mode",
            "set_circulation_pump_mode",
            EntityCategory.CONFIG,
            CIRCULATION_PUMP_MODE_TO_NUMBER,
            NUMBER_TO_CIRCULATION_PUMP_MODE,
            "mdi:pump",
        )
    ],
    "get_user_menu_state": [
        Map(
            "User Menu Lock",
            "set_user_menu_state",
            EntityCategory.CONFIG,
            USER_MENU_STATE_TO_NUMBER,
            NUMBER_TO_USER_MENU_STATE,
            "mdi:menu",
        )
    ],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the select platform."""
    device = hass.data[DOMAIN][config_entry.entry_id]
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
                        m.enum,
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
        enum,
        icon,
    ) -> None:
        """Init Select"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._available = True
        self._attr_name = self._device.get_device_name + ": " + name
        self._set_attr = set_attr
        self._attr_entity_category = entity_category
        self._options = options
        self._attr_icon = icon
        self._enum = enum
        self._name = name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = self._name.lower().replace(" ", "_")
        return f"{_name}.{_unique_id}"

    @property
    def options(self) -> list[str]:
        """Return options."""
        options = []
        for option in self._options:
            options.append(option)
        return options

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if self._enum is not None:
            await getattr(self._device, self._set_attr)(self._options.get(option))
        else:
            await getattr(self._device, self._set_attr)(int(option))

    async def async_update(self) -> None:
        """Fetch new state data for the select."""
        if self._enum is not None:
            self._attr_current_option = self._enum.get(
                await getattr(self._device, self._attribute)()
            )
        else:
            self._attr_current_option = str(
                await getattr(self._device, self._attribute)()
            )


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
        self._name = "Reset Alarm"
        self._attr_name = self._device.get_device_name + ": " + self._name
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def unique_id(self) -> str:
        """Return an unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = self._name.lower().replace(" ", "_")
        return f"{_name}.{_unique_id}"

    @property
    def icon(self) -> str | None:
        """Return an icon."""
        if len(self.options) > 0:
            return "mdi:alert-circle"
        return "mdi:alert-circle-outline"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self._device.set_alarm_reset_code(TEXT_TO_ALARM_CODES.get(option))

    async def async_update(self) -> None:
        """Fetch new state data for the select."""
        self._attr_current_option = None
        self._attr_options = None
        options = []
        option1 = await self._device.get_alarm_1_code()
        option2 = await self._device.get_alarm_2_code()
        option3 = await self._device.get_alarm_3_code()
        if option1 != 0:
            options.append(ALARM_CODES_TO_TEXT.get(option1))
        if option2 != 0:
            options.append(ALARM_CODES_TO_TEXT.get(option2))
        if option3 != 0:
            options.append(ALARM_CODES_TO_TEXT.get(option3))
        if len(options) > 1:
            options.append(ALARM_CODES_TO_TEXT.get(255))
        self._attr_options = options
