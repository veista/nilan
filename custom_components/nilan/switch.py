"""Platform for switch integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

from .__init__ import NilanEntity

from homeassistant.components.switch import SwitchEntity

from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN, SCAN_INTERVAL_TIME


SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

Map = namedtuple(
    "map", "name set_attr entity_category off_value on_value off_icon on_icon"
)

ATTRIBUTE_TO_SWITCHES = {
    "get_supply_air_after_heating": [
        Map(
            "supply_air_after_heating",
            "set_supply_air_after_heating",
            EntityCategory.CONFIG,
            0,
            1,
            "mdi:radiator-off",
            "mdi:radiator",
        )
    ],
}


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Set up the number platform."""
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
    switches = []
    for attribute in device.get_assigned("switch"):
        if attribute in ATTRIBUTE_TO_SWITCHES:
            maps = ATTRIBUTE_TO_SWITCHES[attribute]
            switches.extend(
                [
                    NilanCTS602Number(
                        device,
                        attribute,
                        m.name,
                        m.set_attr,
                        m.entity_category,
                        m.off_value,
                        m.on_value,
                        m.off_icon,
                        m.on_icon,
                    )
                    for m in maps
                ]
            )
    async_add_entities(switches, update_before_add=True)


class NilanCTS602Number(SwitchEntity, NilanEntity):
    """Representation of a Switch."""

    def __init__(
        self,
        device,
        attribute,
        name,
        set_attr,
        entity_category,
        off_value,
        on_value,
        off_icon,
        on_icon,
    ) -> None:
        """Init Number"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._available = True
        self._set_attr = set_attr
        self._attr_entity_category = entity_category
        self._off_icon = off_icon
        self._on_icon = on_icon
        self._name = name
        self._off_value = off_value
        self._on_value = on_value
        self._attr_translation_key = self._name
        self._attr_has_entity_name = True
        self._attr_unique_id = self._name

    @property
    def icon(self) -> str | None:
        if self._attr_is_on:
            return self._on_icon
        return self._off_icon

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        await getattr(self._device, self._set_attr)(int(self._off_value))

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        await getattr(self._device, self._set_attr)(int(self._on_value))

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_is_on = await getattr(self._device, self._attribute)()
