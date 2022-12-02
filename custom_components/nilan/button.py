"""Platform for button integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

from .__init__ import NilanEntity

from homeassistant.components.button import ButtonEntity

from .const import DOMAIN, SCAN_INTERVAL_TIME

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

Map = namedtuple("map", "press_attr name entity_category press_value auto_clear icon")

ATTRIBUTE_TO_BUTTONS = {
    "display_escape_button": [
        Map(
            "Display Escape Button",
            "set_display_button",
            None,
            0x01,
            True,
            None,
        )
    ],
    "display_up_button": [
        Map(
            "Display Up Button",
            "set_display_button",
            None,
            0x02,
            True,
            None,
        )
    ],
    "display_down_button": [
        Map(
            "Display Down Button",
            "set_display_button",
            None,
            0x04,
            True,
            None,
        )
    ],
    "display_enter_button": [
        Map(
            "Display Enter Button",
            "set_display_button",
            None,
            0x08,
            True,
            None,
        )
    ],
    "display_off_button": [
        Map(
            "Display Off Button",
            "set_display_button",
            None,
            0x10,
            True,
            None,
        )
    ],
    "display_on_button": [
        Map(
            "Display On Button",
            "set_display_button",
            None,
            0x20,
            True,
            None,
        )
    ],
    "display_down_escape_button": [
        Map(
            "Display Down + Escape Button",
            "set_display_button",
            None,
            0x05,
            False,
            None,
        )
    ],
    "display_clear_down_escape_button": [
        Map(
            "Display Clear Down Escape Press",
            "set_display_button",
            None,
            0x00,
            False,
            None,
        )
    ],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the number platform."""
    device = hass.data[DOMAIN][config_entry.entry_id]
    numbers = []
    for attribute in device.get_assigned("button"):
        if attribute in ATTRIBUTE_TO_BUTTONS:
            maps = ATTRIBUTE_TO_BUTTONS[attribute]
            numbers.extend(
                [
                    NilanCTS602Number(
                        device,
                        attribute,
                        m.name,
                        m.press_attr,
                        m.entity_category,
                        m.press_value,
                        m.auto_clear,
                        m.icon,
                    )
                    for m in maps
                ]
            )
    async_add_entities(numbers, update_before_add=True)


class NilanCTS602Number(ButtonEntity, NilanEntity):
    """Representation of a Switch."""

    def __init__(
        self,
        device,
        attribute,
        press_attr,
        name,
        entity_category,
        press_value,
        auto_clear,
        icon,
    ) -> None:
        """Init Number"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._available = True
        self._attr_name = "Nilan: " + name
        self._press_attr = press_attr
        self._attr_entity_category = entity_category
        self._attr_icon = icon
        self._name = name
        self._press_value = press_value
        self._auto_clear = auto_clear

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = self._name.lower().replace(" ", "_")
        return f"{_name}.{_unique_id}"

    async def async_press(self, **kwargs):
        """Handle the button press."""
        await getattr(self._device, self._press_attr)(int(self._press_value))
        if self._auto_clear:
            await getattr(self._device, self._press_attr)(int(0))
