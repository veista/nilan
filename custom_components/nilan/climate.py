"""Platform for climate integration."""
from __future__ import annotations

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
)

from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature

from .const import DOMAIN
from .__init__ import NilanEntity

HVAC_MODE_TO_STATE = {
    1: HVACMode.HEAT,
    2: HVACMode.COOL,
    3: HVACMode.AUTO,
}

STATE_TO_HVAC_MODE = {
    HVACMode.HEAT: 1,
    HVACMode.COOL: 2,
    HVACMode.AUTO: 3,
}

PRESET_TO_HVAC = {
    "energy": 0,
    "comfort": 1,
    "water": 2,
}

HVAC_TO_PRESET = {
    0: "energy",
    1: "comfort",
    2: "water",
}


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Add climate entities for a config entry."""
    supported_features = ClimateEntityFeature.FAN_MODE

    hvac_basic_attributes = [
        "get_run_state",
        "get_operation_mode",
        "get_ventilation_step",
        "get_control_state",
    ]
    hvac_extra_status_attributes = [
        "get_ventilation_state",
        "get_supply_fan_level",
    ]
    hvac_temperature_attributes = [
        "get_user_temperature_setpoint",
        "get_control_temperature",
    ]

    hvac_preset_attributes = [
        "get_air_exchange_mode",
    ]

    hvac_humidity_attributes = [
        "get_user_humidity_setpoint",
        "get_humidity",
    ]

    entities = []
    extra_status_attributes = False
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
    if all(attribute in device.get_attributes for attribute in hvac_basic_attributes):
        if all(
            attribute in device.get_attributes
            for attribute in hvac_temperature_attributes
        ):
            supported_features |= ClimateEntityFeature.TARGET_TEMPERATURE
        if all(
            attribute in device.get_attributes for attribute in hvac_preset_attributes
        ):
            supported_features |= ClimateEntityFeature.PRESET_MODE
        if all(
            attribute in device.get_attributes for attribute in hvac_humidity_attributes
        ):
            supported_features |= ClimateEntityFeature.TARGET_HUMIDITY
        if all(
            attribute in device.get_attributes
            for attribute in hvac_extra_status_attributes
        ):
            extra_status_attributes = True
        entities.append(
            NilanClimate(device, supported_features, extra_status_attributes)
        )
    async_add_entities(entities, True)


class NilanClimate(NilanEntity, ClimateEntity):
    """Define a Nilan HVAC."""

    def __init__(self, device, supported_featrures, extra_status_attributes) -> None:
        """Init the class."""
        super().__init__(device)
        self._attr_translation_key = "hvac"
        self._attr_has_entity_name = True
        self._attr_unique_id = "hvac"
        self._hvac_on = False
        self._attr_max_humidity = 45
        self._attr_min_humidity = 15
        self._attr_min_temp = 5
        self._attr_max_temp = 30
        self._attr_target_temperature_step = 1
        self._attr_hvac_modes = [
            HVACMode.COOL,
            HVACMode.HEAT,
            HVACMode.AUTO,
            HVACMode.OFF,
        ]
        self._attr_preset_modes = ["energy", "comfort", "water"]
        self._attr_fan_modes = ["0", "1", "2", "3", "4"]
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_supported_features = supported_featrures
        self._extra_status_attributes = extra_status_attributes

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        await self._device.set_ventilation_step(int(fan_mode))
        self.async_write_ha_state()

    async def async_set_preset_mode(self, preset_mode):
        """Set new target preset mode."""
        await self._device.set_air_exchange_mode(PRESET_TO_HVAC.get(preset_mode))
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target operation mode."""
        if hvac_mode == HVACMode.OFF:
            await self._device.set_run_state(False)
        else:
            self._hvac_on = await self._device.get_run_state()
            if not self._hvac_on:
                await self._device.set_run_state(True)
            await self._device.set_operation_mode(STATE_TO_HVAC_MODE.get(hvac_mode))
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        await self._device.set_user_temperature_setpoint(kwargs[ATTR_TEMPERATURE])
        self.async_write_ha_state()

    async def async_set_humidity(self, humidity):
        """Set new target temperature."""
        await self._device.set_user_humidity_setpoint(humidity)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """update sensor values"""
        self._attr_target_temperature = (
            await self._device.get_user_temperature_setpoint()
        )
        self._attr_current_humidity = await self._device.get_humidity()
        self._attr_current_temperature = await self._device.get_control_temperature()
        self._hvac_on = await self._device.get_run_state()
        self._attr_target_humidity = await self._device.get_user_humidity_setpoint()

        self._attr_fan_mode = str(await self._device.get_ventilation_step())
        control_state = await self._device.get_control_state()
        if control_state is None:
            return

        if self._attr_supported_features & ClimateEntityFeature.PRESET_MODE:
            self._attr_preset_mode = HVAC_TO_PRESET.get(
                await self._device.get_air_exchange_mode()
            )
        if self._extra_status_attributes:
            ventilation_state = await self._device.get_ventilation_state()
            fan_supply_level = await self._device.get_supply_fan_level()
            if ventilation_state == 3:
                self._attr_hvac_action = HVACAction.DRYING
            elif control_state in (7, 17):
                self._attr_hvac_action = HVACAction.HEATING
            elif control_state in (8, 11):
                self._attr_hvac_action = HVACAction.COOLING
            elif fan_supply_level > 0:
                self._attr_hvac_action = HVACAction.FAN
            elif fan_supply_level == 0 and control_state > 0:
                self._attr_hvac_action = HVACAction.IDLE
            else:
                self._attr_hvac_action = HVACAction.OFF
        else:
            if control_state in (7, 17):
                self._attr_hvac_action = HVACAction.HEATING
            elif control_state in (8, 11):
                self._attr_hvac_action = HVACAction.COOLING
            else:
                self._attr_hvac_action = HVACAction.OFF

        if not self._hvac_on:
            self._attr_hvac_mode = HVACAction.OFF
        else:
            self._attr_hvac_mode = HVAC_MODE_TO_STATE.get(
                await self._device.get_operation_mode()
            )
