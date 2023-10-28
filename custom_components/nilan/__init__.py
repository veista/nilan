"""The Nilan integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import Entity

from .device import Device

import logging

from .const import DOMAIN

PLATFORMS = [
    "button",
    "climate",
    "water_heater",
    "sensor",
    "select",
    "binary_sensor",
    "number",
    "switch",
]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Nilan CTS602 Modbus TCP from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    name = entry.data["name"]
    host_port = entry.data["host_port"]
    unit_id = entry.data["unit_id"]
    com_type = entry.data["com_type"]
    host_ip = entry.data["host_ip"]
    # board_type = entry.data["board_type"]

    device = Device(hass, name, com_type, host_ip, host_port, unit_id)
    try:
        await device.setup()
    except ValueError as ex:
        raise ConfigEntryNotReady(f"Timeout while connecting {host_ip}") from ex
    hass.data[DOMAIN][entry.entry_id] = device

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )
    return True


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        new = {**config_entry.data}
        new.update({"com_type": "tcp"})
        new.update({"board_type": "CTS602"})
        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new)

    elif config_entry.version == 2:
        new = {**config_entry.data}
        new.update({"board_type": "CTS602"})
        config_entry.version = 3
        hass.config_entries.async_update_entry(config_entry, data=new)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class NilanEntity(Entity):
    """Nilan Entity"""

    def __init__(self, device: Device) -> None:
        """Initialize the instance."""
        self._device = device

    @property
    def device_info(self):
        """Device Info"""
        unique_id = self._device.get_device_name + self._device.get_device_type

        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, unique_id),
            },
            "name": self._device.get_device_name,
            "manufacturer": "Nilan",
            "model": self._device.get_device_type,
            "sw_version": self._device.get_device_sw_version,
            "hw_version": self._device.get_device_hw_version,
            "suggested_area": "Boiler Room",
        }
