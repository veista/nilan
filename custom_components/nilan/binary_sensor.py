"""Platform for binary sensor integration."""
from __future__ import annotations

from datetime import timedelta

from collections import namedtuple

from .__init__ import NilanEntity

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)

from .const import (
    DOMAIN,
    SCAN_INTERVAL_TIME,
)

SCAN_INTERVAL = timedelta(seconds=SCAN_INTERVAL_TIME)

Map = namedtuple("map", "name device_class entity_category on_icon off_icon")

ATTRIBUTE_TO_BINARY_SENSORS = {
    "get_compressor_state": [
        Map(
            "Compressor",
            BinarySensorDeviceClass.RUNNING,
            None,
            None,
            None,
        )
    ],
    "get_smoke_alarm_state": [
        Map(
            "Smoke Alarm",
            BinarySensorDeviceClass.SMOKE,
            None,
            None,
            None,
        )
    ],
    "get_defrost_state": [
        Map(
            "Defrost",
            BinarySensorDeviceClass.RUNNING,
            None,
            "mdi:snowflake-melt",
            None,
        )
    ],
    "get_bypass_flap_state": [
        Map(
            "Bypass Flap",
            BinarySensorDeviceClass.OPENING,
            None,
            None,
            None,
        )
    ],
    "get_user_function_1_state": [
        Map(
            "User Selection 1",
            BinarySensorDeviceClass.RUNNING,
            None,
            "mdi:account",
            "mdi:account-off",
        )
    ],
    "get_user_function_2_state": [
        Map(
            "User Selection 2",
            BinarySensorDeviceClass.RUNNING,
            None,
            "mdi:account",
            "mdi:account-off",
        )
    ],
    "get_display_led_1_state": [
        Map(
            "Display LED 1",
            BinarySensorDeviceClass.LIGHT,
            None,
            "mdi:led-on",
            "mdi:led-off",
        )
    ],
    "get_display_led_2_state": [
        Map(
            "Display LED 2",
            BinarySensorDeviceClass.LIGHT,
            None,
            "mdi:led-on",
            "mdi:led-off",
        )
    ],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    device = hass.data[DOMAIN][config_entry.entry_id]
    binary_sensors = []
    for attribute in device.get_assigned("binary_sensor"):
        if attribute in ATTRIBUTE_TO_BINARY_SENSORS:
            maps = ATTRIBUTE_TO_BINARY_SENSORS[attribute]
            binary_sensors.extend(
                [
                    NilanCTS602BinarySensor(
                        device,
                        attribute,
                        m.name,
                        m.device_class,
                        m.entity_category,
                        m.on_icon,
                        m.off_icon,
                    )
                    for m in maps
                ]
            )
    async_add_entities(binary_sensors, update_before_add=True)


class NilanCTS602BinarySensor(BinarySensorEntity, NilanEntity):
    """Representation of a Binary Sensor."""

    def __init__(
        self,
        device,
        attribute,
        name,
        device_class,
        entity_category,
        on_icon,
        off_icon,
    ) -> None:
        """Init Binary Sensor"""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._available = True
        self._attr_name = "Nilan: " + name
        self._attr_device_class = device_class
        self._attr_entity_category = entity_category
        self._name = name
        self._on_icon = on_icon
        self._off_icon = off_icon

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

    async def async_update(self) -> None:
        """Fetch new state data for the binary sensor."""
        self._attr_is_on = await getattr(self._device, self._attribute)()
