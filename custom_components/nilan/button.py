"""Platform for button integration."""
from __future__ import annotations

from datetime import datetime

from .__init__ import NilanEntity

from homeassistant.components.button import ButtonEntity

from homeassistant.util.dt import now

from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Set up the number platform."""
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
    for attribute in device.get_assigned("button"):
        if attribute in ("set_time"):
            async_add_entities(
                [NilanCTS602SyncTimeButton(device)], update_before_add=True
            )


class NilanCTS602SyncTimeButton(ButtonEntity, NilanEntity):
    """Representation of a Sync Time Button."""

    def __init__(
        self,
        device,
    ) -> None:
        """Init Sync Time Button"""
        super().__init__(device)
        self._device = device
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_icon = "mdi:clock-edit-outline"
        self._attr_translation_key = "sync_time"
        self._attr_has_entity_name = True
        self._attr_unique_id = "sync_time"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._device.set_time(now())
