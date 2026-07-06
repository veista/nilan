"""Platform for button integration."""
from __future__ import annotations

from collections import namedtuple

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.util.dt import now

from .__init__ import NilanEntity
from .const import DOMAIN

Map = namedtuple("map", "name icon entity_category")

ATTRIBUTE_TO_BUTTONS = {
    "set_cts400_reset_filter_timer": Map(
        "cts400_reset_filter_timer",
        "mdi:air-filter",
        EntityCategory.CONFIG,
    ),
    "set_cts400_reset_alarm": Map(
        "cts400_reset_alarm",
        "mdi:alarm-light-off-outline",
        EntityCategory.CONFIG,
    ),
}


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Set up the number platform."""
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
    for attribute in device.get_assigned("button"):
        if attribute == "set_time":
            async_add_entities(
                [NilanCTS602SyncTimeButton(device)], update_before_add=True
            )
        elif attribute in ATTRIBUTE_TO_BUTTONS:
            entity = ATTRIBUTE_TO_BUTTONS[attribute]
            async_add_entities(
                [
                    NilanButton(
                        device,
                        attribute,
                        entity.name,
                        entity.icon,
                        entity.entity_category,
                    )
                ],
                update_before_add=True,
            )


class NilanCTS602SyncTimeButton(ButtonEntity, NilanEntity):
    """Representation of a Sync Time Button."""

    def __init__(
        self,
        device,
    ) -> None:
        """Init Sync Time Button."""
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


class NilanButton(ButtonEntity, NilanEntity):
    """Representation of a Nilan write-1 action button."""

    def __init__(self, device, attribute, name, icon, entity_category) -> None:
        """Init the action button."""
        super().__init__(device)
        self._device = device
        self._attribute = attribute
        self._attr_entity_category = entity_category
        self._attr_icon = icon
        self._attr_translation_key = name
        self._attr_has_entity_name = True
        self._attr_unique_id = name

    async def async_press(self) -> None:
        """Handle the button press."""
        await getattr(self._device, self._attribute)()
