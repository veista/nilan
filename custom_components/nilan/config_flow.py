"""Config flow for Nilan integration."""
from __future__ import annotations

from typing import Any, Optional

import voluptuous as vol


from homeassistant import config_entries

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from .device import DEVICE_TYPES

from .registers import CTS602HoldingRegisters

from .const import DOMAIN


CONF_LOCATION_ID = "location_id"

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan"): str,
        vol.Required("host_ip"): str,
        vol.Required("host_port", default="502"): str,
        vol.Required("unit_id", default="30"): str,
    }
)


async def validate_device(address, port, unit_id) -> None:
    """validate device model"""
    client = ModbusTcpClient(address, port)
    try:
        result = client.read_holding_registers(
            CTS602HoldingRegisters.machine_type_select, 1, unit=int(unit_id)
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
        signed=True,
    )
    if not value_output in DEVICE_TYPES:
        raise ValueError("unsupported_device")
    client.close()
    return


def format_unique_id(app_id: str, location_id: str) -> str:
    """Format the unique id for a config entry."""
    return f"{app_id}_{location_id}"


class NilanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nilan CTS602 Modbus TCP."""

    VERSION = 1

    data: Optional[dict(str, Any)]

    async def async_step_user(self, user_input: Optional[dict(str, Any)] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: dict(str, str) = {}
        if user_input is not None:
            try:
                await validate_device(
                    user_input["host_ip"],
                    user_input["host_port"],
                    user_input["unit_id"],
                )
            except ValueError as error:
                errors["base"] = str(error)
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                return self.async_create_entry(title=user_input["name"], data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
