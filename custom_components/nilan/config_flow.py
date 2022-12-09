"""Config flow for Nilan integration."""
from __future__ import annotations

from typing import Any, Optional

import voluptuous as vol

import logging

from homeassistant import config_entries

from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient
from pymodbus.exceptions import ModbusException

from .device import DEVICE_TYPES

from .registers import CTS602HoldingRegisters

from .const import DOMAIN


CONF_LOCATION_ID = "location_id"

STEP_TCP_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan"): str,
        vol.Required("host_ip"): str,
        vol.Required("host_port", default="502"): str,
        vol.Required("unit_id", default="30"): str,
    }
)

STEP_SERIAL_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan"): str,
        vol.Required("host_port"): str,
        vol.Required("unit_id", default="30"): str,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_validate_device(com_type, port, unit_id, address: str | None) -> None:
    """validate device model"""
    if com_type == "tcp":
        client = ModbusTcpClient(address, port)
    else:
        client = ModbusSerialClient(
            method="rtu",
            port=port,
            stopbits=1,
            bytesize=8,
            parity="E",
            baudrate=19200,
            timeout=1,
        )
    try:
        result = client.read_holding_registers(
            CTS602HoldingRegisters.control_type, 1, unit=int(unit_id)
        )
    except ModbusException as value_error:
        client.close()
        raise ValueError("cannot_connect") from value_error
    if hasattr(result, "message"):
        client.close()
        raise ValueError("invalid_response")
    value_output = int.from_bytes(
        result.registers[0].to_bytes(2, "little", signed=False),
        "little",
        signed=False,
    )
    if not value_output in DEVICE_TYPES:
        _LOGGER.debug(
            "Device Type %s not found in supported devices list",
            str(value_output),
        )
        raise ValueError("unsupported_device")
    client.close()
    return


def format_unique_id(app_id: str, location_id: str) -> str:
    """Format the unique id for a config entry."""
    return f"{app_id}_{location_id}"


class NilanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nilan CTS602 Modbus TCP."""

    VERSION = 2

    data: Optional[dict(str, Any)]

    async def async_step_user(self, user_input: Optional[dict(str, Any)] = None):
        """Invoked when a user initiates a flow via the user interface."""
        return await self.async_step_menu(user_input)

    async def async_step_menu(self, user_input: Optional[dict(str, Any)] = None):
        """Shows Communications Selection"""
        return self.async_show_menu(
            step_id="menu",
            menu_options=["tcp", "serial"],
            # description_placeholders={
            #     "model": "Example model",
            # },
        )

    async def async_step_tcp(self, user_input: Optional[dict(str, Any)] = None):
        """Configure ModBus TCP entry"""
        errors: dict(str, str) = {}

        if user_input is not None:
            try:
                await async_validate_device(
                    "tcp",
                    user_input["host_port"],
                    user_input["unit_id"],
                    user_input["host_ip"],
                )
            except ValueError as error:
                errors["base"] = str(error)
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                self.data.update({"com_type": "tcp"})
                return self.async_create_entry(title=user_input["name"], data=self.data)
        return self.async_show_form(
            step_id="tcp", data_schema=STEP_TCP_DATA_SCHEMA, errors=errors
        )

    async def async_step_serial(self, user_input: Optional[dict(str, Any)] = None):
        """Configure ModBus Serial RTU entry"""
        errors: dict(str, str) = {}

        if user_input is not None:
            try:
                await async_validate_device(
                    "serial", user_input["host_port"], user_input["unit_id"], None
                )
            except ValueError as error:
                errors["base"] = str(error)
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                self.data.update({"com_type": "tcp"})
                return self.async_create_entry(title=user_input["name"], data=self.data)
        return self.async_show_form(
            step_id="serial", data_schema=STEP_SERIAL_DATA_SCHEMA, errors=errors
        )
