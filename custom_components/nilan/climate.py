"""Platform for climate integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    CURRENT_HVAC_OFF,
    CURRENT_HVAC_DRY,
    CURRENT_HVAC_COOL,
    CURRENT_HVAC_FAN,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    HVAC_MODE_AUTO,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_FAN_MODE,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_HUMIDITY,
    SUPPORT_TARGET_TEMPERATURE,
)

from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS

from .const import DOMAIN, SCAN_INTERVAL_TIME
from .__init__ import NilanEntity

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

HVAC_MODE_TO_STATE = {
    1: HVAC_MODE_HEAT,
    2: HVAC_MODE_COOL,
    3: HVAC_MODE_AUTO,
}

STATE_TO_HVAC_MODE = {
    HVAC_MODE_HEAT: 1,
    HVAC_MODE_COOL: 2,
    HVAC_MODE_AUTO: 3,
}

PRESET_TO_HVAC = {
    "Energy": 0,
    "Comfort": 1,
    "Water": 2,
}

HVAC_TO_PRESET = {
    0: "Energy",
    1: "Comfort",
    2: "Water",
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add climate entities for a config entry."""
    supported_features = SUPPORT_FAN_MODE | SUPPORT_TARGET_HUMIDITY

    hvac_basic_attributes = [
        "get_run_state",
        "get_ventilation_step",
        "get_operation_mode",
        "get_user_humidity_setpoint",
        "get_humidity",
        "get_inlet_speed_step",
        "get_ventilation_state",
        "get_control_state",
    ]
    hvac_temperature_attributes = [
        "get_user_temperature_setpoint",
        "get_room_master_temperature",
    ]

    hvac_preset_attributes = [
        "get_air_exchange_mode",
    ]

    # refine to select supported features automatically
    entities = []
    device = hass.data[DOMAIN][config_entry.entry_id]
    if all(attribute in device.get_attributes for attribute in hvac_basic_attributes):
        if all(
            attribute in device.get_attributes
            for attribute in hvac_temperature_attributes
        ):
            supported_features |= SUPPORT_TARGET_TEMPERATURE
        if all(
            attribute in device.get_attributes for attribute in hvac_preset_attributes
        ):
            supported_features |= SUPPORT_PRESET_MODE
        entities.append(NilanClimate(device, supported_features))
    async_add_entities(entities, True)


class NilanClimate(NilanEntity, ClimateEntity):
    """Define a Nilan HVAC."""

    def __init__(self, device, supported_featrures):
        """Init the class."""
        super().__init__(device)
        self._hvac_on = False
        self._attr_max_humidity = 45
        self._attr_min_humidity = 15
        self._attr_min_temp = 5
        self._attr_max_temp = 30
        self._attr_target_temperature_step = 1
        self._attr_hvac_modes = [
            HVAC_MODE_COOL,
            HVAC_MODE_HEAT,
            HVAC_MODE_AUTO,
            HVAC_MODE_OFF,
        ]
        self._attr_preset_modes = ["Energy", "Comfort", "Water"]
        self._attr_fan_modes = [0, 1, 2, 3, 4]
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_supported_features = supported_featrures

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
        if hvac_mode == HVAC_MODE_OFF:
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
        self._attr_current_temperature = (
            await self._device.get_room_master_temperature()
        )
        self._hvac_on = await self._device.get_run_state()
        self._attr_target_humidity = await self._device.get_user_humidity_setpoint()
        self._attr_preset_mode = HVAC_TO_PRESET.get(
            await self._device.get_air_exchange_mode()
        )
        self._attr_fan_mode = await self._device.get_ventilation_step()
        control_state = await self._device.get_control_state()
        fan_inlet_state = await self._device.get_inlet_speed_step()
        ventilation_state = await self._device.get_ventilation_state()

        if ventilation_state == 3:
            self._attr_hvac_action = CURRENT_HVAC_DRY
        elif control_state in (7, 17):
            self._attr_hvac_action = CURRENT_HVAC_HEAT
        elif control_state in (8, 11):
            self._attr_hvac_action = CURRENT_HVAC_COOL
        elif fan_inlet_state > 0:
            self._attr_hvac_action = CURRENT_HVAC_FAN
        elif fan_inlet_state == 0 and control_state > 0:
            self._attr_hvac_action = CURRENT_HVAC_IDLE
        else:
            self._attr_hvac_action = CURRENT_HVAC_OFF

        if not self._hvac_on:
            self._attr_hvac_mode = HVAC_MODE_OFF
        else:
            self._attr_hvac_mode = HVAC_MODE_TO_STATE.get(
                await self._device.get_operation_mode()
            )

    @property
    def name(self) -> str | None:
        """Return a name"""
        _name = self._device.get_device_name
        return f"{_name}: HVAC"

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = "hvac"
        return f"{_name}.{_unique_id}"
