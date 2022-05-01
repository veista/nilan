"""The Nilan integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .device import Device


from .const import DOMAIN

PLATFORMS = ["climate", "water_heater", "sensor", "select", "binary_sensor", "number"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Nilan CTS602 Modbus TCP from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    name = entry.data["name"]
    host_ip = entry.data["host_ip"]
    host_port = entry.data["host_port"]
    unit_id = entry.data["unit_id"]

    device = Device(hass, name, host_ip, host_port, unit_id)
    await device.setup()

    hass.data[DOMAIN][entry.entry_id] = device

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
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
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._device.get_device_type)
            },
            "name": self._device.get_device_name,
            "manufacturer": "Nilan",
            "model": self._device.get_device_type,
            "sw_version": self._device.get_device_sw_version,
            "hw_version": self._device.get_device_hw_version,
            "suggested_area": "Boiler Room",
        }
