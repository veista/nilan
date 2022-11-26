"""Platform for switch integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

from .__init__ import NilanEntity

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, SCAN_INTERVAL_TIME


SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

Map = namedtuple(
    "map", "name set_attr entity_category off_value on_value off_icon on_icon"
)

ATTRIBUTE_TO_SWITCHES = {
    "get_supply_air_after_heating": [
        Map(
            "Supply Air After Heating",
            "set_supply_air_after_heating",
            None,
            0,
            1,
            "mdi:radiator-disabled",
            "mdi:radiator",
        )
    ],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the number platform."""
    device = hass.data[DOMAIN][config_entry.entry_id]
    numbers = []
    for attribute in device.get_assigned("switch"):
        if attribute in ATTRIBUTE_TO_SWITCHES:
            maps = ATTRIBUTE_TO_SWITCHES[attribute]
            numbers.extend(
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
    async_add_entities(numbers, update_before_add=True)


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
        self._attr_name = "Nilan: " + name
        self._set_attr = set_attr
        self._attr_entity_category = entity_category
        self._off_icon = off_icon
        self._on_icon = on_icon
        self._name = name
        self._off_value = off_value
        self._on_value = on_value

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        _name = self._device.get_device_name.lower().replace(" ", "_")
        _unique_id = self._name.lower().replace(" ", "_")
        return f"{_name}.{_unique_id}"

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
