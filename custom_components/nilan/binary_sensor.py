"""Platform for binary sensor integration."""
from __future__ import annotations

from collections import namedtuple

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .__init__ import NilanEntity
from .const import DOMAIN

Map = namedtuple("map", "name device_class entity_category on_icon off_icon")

ATTRIBUTE_TO_BINARY_SENSORS = {
    "get_compressor_state": [
        Map(
            "compressor",
            BinarySensorDeviceClass.RUNNING,
            None,
            None,
            None,
        )
    ],
    "get_smoke_alarm_state": [
        Map(
            "smoke_alarm",
            BinarySensorDeviceClass.SMOKE,
            None,
            None,
            None,
        )
    ],
    "get_defrost_state": [
        Map(
            "defrost",
            BinarySensorDeviceClass.RUNNING,
            None,
            "mdi:snowflake-melt",
            None,
        )
    ],
    "get_bypass_flap_state": [
        Map(
            "bypass_flap",
            BinarySensorDeviceClass.OPENING,
            None,
            None,
            None,
        )
    ],
    "get_user_function_1_state": [
        Map(
            "user_selection_1",
            BinarySensorDeviceClass.RUNNING,
            None,
            "mdi:account",
            "mdi:account-off",
        )
    ],
    "get_user_function_2_state": [
        Map(
            "user_selection_2",
            BinarySensorDeviceClass.RUNNING,
            None,
            "mdi:account",
            "mdi:account-off",
        )
    ],
    "get_display_led_1_state": [
        Map(
            "display_led_1",
            BinarySensorDeviceClass.LIGHT,
            None,
            "mdi:led-on",
            "mdi:led-off",
        )
    ],
    "get_display_led_2_state": [
        Map(
            "display_led_2",
            BinarySensorDeviceClass.LIGHT,
            None,
            "mdi:led-on",
            "mdi:led-off",
        )
    ],
    "get_circulation_pump_state": [
        Map(
            "circulation_pump",
            BinarySensorDeviceClass.RUNNING,
            None,
            "mdi:pump",
            "mdi:pump-off",
        )
    ],
    "get_heater_relay_1_state": [
        Map(
            "heater_relay_1",
            None,
            None,
            "mdi:electric-switch-closed",
            "mdi:electric-switch",
        )
    ],
    "get_heater_relay_2_state": [
        Map(
            "heater_relay_2",
            None,
            None,
            "mdi:electric-switch-closed",
            "mdi:electric-switch",
        )
    ],
    "get_heater_relay_3_state": [
        Map(
            "heater_relay_3",
            None,
            None,
            "mdi:electric-switch-closed",
            "mdi:electric-switch",
        )
    ],
}


async def async_setup_entry(HomeAssistant, config_entry, async_add_entities):
    """Set up the sensor platform."""
    device = HomeAssistant.data[DOMAIN][config_entry.entry_id]
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
        """Init Binary Sensor."""
        super().__init__(device)
        self._attribute = attribute
        self._device = device
        self._attr_device_class = device_class
        self._attr_entity_category = entity_category
        self._name = name
        self._on_icon = on_icon
        self._off_icon = off_icon
        self._attr_has_entity_name = True
        self._attr_translation_key = self._name
        self._attr_unique_id = self._name

    @property
    def icon(self) -> str | None:
        """Define icon."""
        if self._attr_is_on:
            return self._on_icon
        return self._off_icon

    async def async_update(self) -> None:
        """Fetch new state data for the binary sensor."""
        self._attr_is_on = await getattr(self._device, self._attribute)()
