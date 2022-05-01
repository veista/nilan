"""Platform for water heater integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    STATE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_OPERATION_MODE,
)

from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS

from .const import (
    DOMAIN,
    SCAN_INTERVAL_TIME,
)

from .__init__ import NilanEntity

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add water heater entities for a config entry."""
    water_heater_capabilities = [
        "get_control_state",
        "get_electric_water_heater_setpoint",
        "get_electric_water_heater_state",
        "get_compressor_water_heater_setpoint",
        "get_compressor_water_heater_temperature",
    ]
    entities = []
    device = hass.data[DOMAIN][config_entry.entry_id]
    if all(
        attribute in device.get_attributes for attribute in water_heater_capabilities
    ):
        entities.append(NilanTopWaterHeater(device))
        entities.append(NilanBottomWaterHeater(device))
    async_add_entities(entities, True)


class NilanTopWaterHeater(NilanEntity, WaterHeaterEntity):
    """Define a Nilan Water Heater."""

    def __init__(self, device):
        """Init the class."""
        super().__init__(device)
        self._state = None
        self._previous_temp = 55
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_operation_list = ["Off", "On"]
        self._attr_supported_features = (
            SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE
        )

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        await self._device.set_electric_water_heater_setpoint(kwargs[ATTR_TEMPERATURE])
        self.async_write_ha_state()

    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""
        if operation_mode == "Off":
            await self._device.set_electric_water_heater_setpoint(0)
        else:
            await self._device.set_electric_water_heater_setpoint(self._previous_temp)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """update sensor values"""
        self._attr_target_temperature = (
            await self._device.get_electric_water_heater_setpoint()
        )
        self._attr_current_temperature = (
            await self._device.get_electric_water_heater_temperature()
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
            self._attr_current_operation = "On"
        else:
            self._attr_current_operation = "Off"

    @property
    def state(self) -> str | None:  # pylint: disable=overridden-final-method
        """Return the current state."""
        return self._state

    @property
    def min_temp(self):
        return 5

    @property
    def max_temp(self):
        return 85

    @property
    def icon(self) -> str | None:
        if self._state == STATE_OFF:
            return "mdi:water-boiler-off"
        return "mdi:water-boiler"

    @property
    def name(self) -> str | None:
        """Return a name"""
        _name = self._device.get_device_name
        return f"{_name}: Top Water Heater (Electric)"

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = "top_water_heater"
        return f"{_name}.{_unique_id}"


class NilanBottomWaterHeater(NilanEntity, WaterHeaterEntity):
    """Define a Nilan Water Heater."""

    def __init__(self, device):
        """Init the class."""
        super().__init__(device)
        self._previous_temp = 55
        self._state = None
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_operation_list = ["Off", "On"]
        self._attr_supported_features = (
            SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE
        )

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        await self._device.set_compressor_water_heater_setpoint(
            kwargs[ATTR_TEMPERATURE]
        )
        self.async_write_ha_state()

    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""
        if operation_mode == "Off":
            await self._device.set_compressor_water_heater_setpoint(0)
        else:
            await self._device.set_compressor_water_heater_setpoint(self._previous_temp)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """update sensor values"""
        self._attr_target_temperature = (
            await self._device.get_compressor_water_heater_setpoint()
        )
        self._attr_current_temperature = (
            await self._device.get_compressor_water_heater_temperature()
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
            self._attr_current_operation = "On"
        else:
            self._attr_current_operation = "Off"

    @property
    def state(self) -> str | None:  # pylint: disable=overridden-final-method
        """Return the current state."""
        return self._state

    @property
    def min_temp(self):
        return 5

    @property
    def max_temp(self):
        return 60

    @property
    def icon(self) -> str | None:
        if self._state == STATE_OFF:
            return "mdi:water-boiler-off"
        return "mdi:water-boiler"

    @property
    def name(self) -> str | None:
        """Return a name"""
        _name = self._device.get_device_name
        return f"{_name}: Bottom Water Heater (Compressor)"

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = "bottom_water_heater"
        return f"{_name}.{_unique_id}"
