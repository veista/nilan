"""Platform for fan integration."""
from __future__ import annotations

from homeassistant.components.fan import FanEntity, FanEntityFeature

from .__init__ import NilanEntity
from .const import DOMAIN

# CTS400 ventilation maps Home Assistant 0-100 % onto fan levels 1-4.
# 0 % = stop; 25/50/75/100 % = level 1/2/3/4. speed_count = 4 makes the
# tile's increase/decrease arrows step exactly one level.
SPEED_COUNT = 4

ATTRIBUTE_TO_FAN = {
    # entity-map key (a Device method) -> translation/unique_id name
    "get_cts400_fan": "cts400_ventilation",
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the fan platform."""
    device = hass.data[DOMAIN][config_entry.entry_id]
    fans = []
    for attribute in device.get_assigned("fan"):
        if attribute in ATTRIBUTE_TO_FAN:
            fans.append(
                NilanCTS400Fan(device, attribute, ATTRIBUTE_TO_FAN[attribute])
            )
    async_add_entities(fans, update_before_add=True)


class NilanCTS400Fan(FanEntity, NilanEntity):
    """CTS400 ventilation fan: run/stop plus four speed levels."""

    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.TURN_ON
        | FanEntityFeature.TURN_OFF
    )
    _attr_speed_count = SPEED_COUNT

    def __init__(self, device, attribute, name) -> None:
        """Init the fan."""
        super().__init__(device)
        self._device = device
        self._attribute = attribute
        self._name = name
        self._enable_turn_on_off_backwards_compatibility = False
        self._attr_translation_key = name
        self._attr_has_entity_name = True
        self._attr_unique_id = name
        self._attr_is_on = None
        self._attr_percentage = None

    @property
    def icon(self) -> str:
        """Pick an icon based on run state."""
        return "mdi:fan" if self._attr_is_on else "mdi:fan-off"

    async def async_turn_on(
        self, percentage=None, preset_mode=None, **kwargs
    ) -> None:
        """Turn the unit on, optionally at a given speed."""
        if percentage is not None and percentage > 0:
            await self.async_set_percentage(percentage)
        else:
            await self._device.set_cts400_run_state(True)

    async def async_turn_off(self, **kwargs) -> None:
        """Stop the unit."""
        await self._device.set_cts400_run_state(False)

    async def async_set_percentage(self, percentage: int) -> None:
        """Map a percentage to fan level 1-4 (0 % stops the unit)."""
        level = max(0, min(SPEED_COUNT, round(percentage / 25)))
        if level == 0:
            await self._device.set_cts400_run_state(False)
            return
        await self._device.set_cts400_fan_level_setpoint(level)
        await self._device.set_cts400_run_state(True)

    async def async_update(self) -> None:
        """Fetch run state and current speed."""
        is_on = await self._device.get_cts400_run_state()
        self._attr_is_on = is_on
        if not is_on:
            self._attr_percentage = 0
            return
        # The live level (input 63) lags right after a start, reading 0 for a
        # poll or two; fall back to the setpoint so the slider doesn't snap to 0.
        level = await self._device.get_cts400_fan_level()
        if not level:
            level = await self._device.get_cts400_fan_level_setpoint()
        self._attr_percentage = level * 25 if level else None
