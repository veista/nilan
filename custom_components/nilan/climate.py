"""Platform for climate integration."""

from __future__ import annotations

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature

from .__init__ import NilanEntity
from .const import DOMAIN

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
    supported_features = (
        ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.TURN_OFF
        | ClimateEntityFeature.TURN_ON
    )

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
    if device.get_assigned("climate"):
        entities.append(NilanCTS400Climate(device, device.cts400_has_heater))
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
        self._enable_turn_on_off_backwards_compatibility = False
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
        """Update sensor values."""
        self._hvac_on = await self._device.get_run_state()
        self._attr_fan_mode = str(await self._device.get_ventilation_step())

        if self._attr_supported_features & ClimateEntityFeature.TARGET_TEMPERATURE:
            self._attr_target_temperature = (
                await self._device.get_user_temperature_setpoint()
            )
            self._attr_current_temperature = (
                await self._device.get_control_temperature()
            )

        if self._attr_supported_features & ClimateEntityFeature.TARGET_HUMIDITY:
            self._attr_current_humidity = await self._device.get_humidity()
            self._attr_target_humidity = await self._device.get_user_humidity_setpoint()

        if self._attr_supported_features & ClimateEntityFeature.PRESET_MODE:
            self._attr_preset_mode = HVAC_TO_PRESET.get(
                await self._device.get_air_exchange_mode()
            )

        control_state = await self._device.get_control_state()
        if control_state is None:
            return

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
        elif control_state in (7, 17):
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


class NilanCTS400Climate(NilanEntity, ClimateEntity):
    """Minimal CTS400 climate: run/stop, fan level and (optionally) target temp.

    The CTS400 has no HVAC-mode register, so it is modelled as FAN_ONLY / OFF. A target-temperature setpoint (holding 37) only has an observable effect when an after-heater is fitted (holding 53 = 2 water / 3 electric); on a base unit (holding 53 = 1, verified live on the reference unit) it is inert, so TARGET_TEMPERATURE is only advertised when a heater is present.

    Because it overlaps with the dedicated fan entity (the primary speed control), this entity is disabled by default and can be enabled by users who want a single thermostat card.
    """

    _attr_translation_key = "cts400_hvac"
    _attr_has_entity_name = True
    _attr_unique_id = "cts400_hvac"
    _attr_entity_registry_enabled_default = False
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.FAN_ONLY, HVACMode.OFF]
    _attr_fan_modes = ["1", "2", "3", "4"]
    _attr_min_temp = 10
    _attr_max_temp = 30
    _attr_target_temperature_step = 0.5

    def __init__(self, device, has_heater) -> None:
        """Init the CTS400 climate entity."""
        super().__init__(device)
        self._device = device
        self._has_heater = has_heater
        self._enable_turn_on_off_backwards_compatibility = False
        supported = (
            ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        )
        if has_heater:
            supported |= ClimateEntityFeature.TARGET_TEMPERATURE
        self._attr_supported_features = supported

    async def async_turn_on(self) -> None:
        """Start the unit."""
        await self._device.set_cts400_run_state(True)

    async def async_turn_off(self) -> None:
        """Stop the unit."""
        await self._device.set_cts400_run_state(False)

    async def async_set_hvac_mode(self, hvac_mode) -> None:
        """Run (FAN_ONLY) or stop (OFF) the unit."""
        await self._device.set_cts400_run_state(hvac_mode != HVACMode.OFF)
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode) -> None:
        """Set the fan level (1-4) and ensure the unit is running."""
        await self._device.set_cts400_fan_level_setpoint(int(fan_mode))
        await self._device.set_cts400_run_state(True)
        self._attr_fan_mode = fan_mode
        self._attr_hvac_mode = HVACMode.FAN_ONLY
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs) -> None:
        """Set the wanted room temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            await self._device.set_cts400_wanted_room_temperature(temperature)
            self._attr_target_temperature = temperature
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Refresh run state, temperatures and fan level."""
        is_on = await self._device.get_cts400_run_state()
        self._attr_hvac_mode = HVACMode.FAN_ONLY if is_on else HVACMode.OFF
        self._attr_hvac_action = HVACAction.FAN if is_on else HVACAction.OFF
        if self._attr_supported_features & ClimateEntityFeature.TARGET_TEMPERATURE:
            self._attr_target_temperature = (
                await self._device.get_cts400_wanted_room_temperature()
            )
        self._attr_current_temperature = (
            await self._device.get_cts400_extract_temperature()
        )
        level = await self._device.get_cts400_fan_level()
        if not level:
            level = await self._device.get_cts400_fan_level_setpoint()
        self._attr_fan_mode = str(level) if level else None
