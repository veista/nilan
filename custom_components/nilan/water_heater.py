"""Platform for water heater integration."""

from __future__ import annotations

from homeassistant.components.water_heater import (
    STATE_ELECTRIC,
    STATE_HEAT_PUMP,
    STATE_OFF,
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature

from .__init__ import NilanEntity
from .const import DOMAIN


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Add water heater entities for a config entry."""
    water_heater_capabilities = [
        "get_control_state",
        "get_electric_water_heater_setpoint",
        "get_t11_electric_water_heater_temperature",
        "get_electric_water_heater_state",
        "get_compressor_water_heater_setpoint",
        "get_t12_compressor_water_heater_temperature",
    ]
    entities = []
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
    if all(
        attribute in device.get_attributes for attribute in water_heater_capabilities
    ):
        entities.append(NilanTopWaterHeater(device))
        entities.append(NilanBottomWaterHeater(device))
    async_add_entities(entities, True)


class NilanTopWaterHeater(NilanEntity, WaterHeaterEntity):
    """Define Nilan Top Water Heater."""

    def __init__(self, device) -> None:
        """Init the class."""
        super().__init__(device)
        self._state = None
        self._previous_temp = 55
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_operation_list = [STATE_OFF, STATE_ELECTRIC]
        self._attr_supported_features = (
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
        )
        self._attr_translation_key = "top_water_heater"
        self._attr_has_entity_name = True
        self._attr_unique_id = "top_water_heater"

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        await self._device.set_electric_water_heater_setpoint(kwargs[ATTR_TEMPERATURE])
        self.async_write_ha_state()

    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""
        if operation_mode == STATE_OFF:
            await self._device.set_electric_water_heater_setpoint(0)
        else:
            await self._device.set_electric_water_heater_setpoint(self._previous_temp)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update sensor values."""
        self._attr_target_temperature = (
            await self._device.get_electric_water_heater_setpoint()
        )
        self._attr_current_temperature = (
            await self._device.get_t11_electric_water_heater_temperature()
        )
        running_state = await self._device.get_electric_water_heater_state()
        if running_state == 1:
            self._state = "heating"
        elif self._attr_target_temperature != 0:
            self._state = "idle"
        else:
            self._state = STATE_OFF

        if self._attr_target_temperature != 0:
            self._previous_temp = self._attr_target_temperature
            self._attr_current_operation = STATE_ELECTRIC
        else:
            self._attr_current_operation = STATE_OFF

    @property
    def min_temp(self):
        """Define minimum temperature."""
        return 5

    @property
    def max_temp(self):
        """Define maximum temperature."""
        return 85

    @property
    def icon(self) -> str | None:
        """Select icon."""
        if self._attr_current_operation == STATE_OFF:
            return "mdi:water-boiler-off"
        return "mdi:water-boiler"

    @property
    def extra_state_attributes(self):
        """Return state."""
        return {"state": self._state}


class NilanBottomWaterHeater(NilanEntity, WaterHeaterEntity):
    """Define Nilan Bottom Water Heater."""

    def __init__(self, device) -> None:
        """Init the class."""
        super().__init__(device)
        self._state = None
        self._previous_temp = 55
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_operation_list = [STATE_OFF, STATE_HEAT_PUMP]
        self._attr_supported_features = (
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
        )
        self._attr_translation_key = "bottom_water_heater"
        self._attr_has_entity_name = True
        self._attr_unique_id = "bottom_water_heater"

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        await self._device.set_compressor_water_heater_setpoint(
            kwargs[ATTR_TEMPERATURE]
        )
        self.async_write_ha_state()

    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""
        if operation_mode == STATE_OFF:
            await self._device.set_compressor_water_heater_setpoint(0)
        else:
            await self._device.set_compressor_water_heater_setpoint(self._previous_temp)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update sensor values."""
        self._attr_target_temperature = (
            await self._device.get_compressor_water_heater_setpoint()
        )
        self._attr_current_temperature = (
            await self._device.get_t12_compressor_water_heater_temperature()
        )
        running_state = await self._device.get_control_state()
        if running_state in (9, 11, 17):
            self._state = "heating"
        elif self._attr_target_temperature != 0:
            self._state = "idle"
        else:
            self._state = STATE_OFF

        if self._attr_target_temperature != 0:
            self._previous_temp = self._attr_target_temperature
            self._attr_current_operation = STATE_HEAT_PUMP
        else:
            self._attr_current_operation = STATE_OFF

    @property
    def min_temp(self):
        """Define minimum temperature."""
        return 5

    @property
    def max_temp(self):
        """Define maximum temperature."""
        return 60

    @property
    def icon(self) -> str | None:
        """Select icon."""
        if self._attr_current_operation == STATE_OFF:
            return "mdi:water-boiler-off"
        return "mdi:water-boiler"

    @property
    def extra_state_attributes(self):
        """Return state."""
        return {"state": self._state}
