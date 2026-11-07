"""Config flow for Nilan integration."""

from __future__ import annotations

from typing import Any, Optional

import voluptuous as vol

from homeassistant import config_entries

from .const import (
    BOARD_TYPE_CTS602,
    BOARD_TYPE_CTS700,
    BOARD_TYPE_CTS700_LEGACY,
    BOARD_TYPE_CTS700_NORDIC,
    DOMAIN,
)
from .config_flow_menus import async_menu_options
from .modbus_hub_util import coexistence_warning, find_conflicting_modbus_hub
from .modbus_probe import (
    async_detect_board,
    async_validate_cts602,
    async_validate_cts700,
    async_validate_cts700_legacy,
    async_validate_cts700_nordic,
    is_cts700_schema_board,
)

STEP_TCP_CTS602_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan CTS602"): str,
        vol.Required("host_ip"): str,
        vol.Required("host_port", default="502"): str,
        vol.Required("unit_id", default=30): int,
    }
)

STEP_TCP_CTS700_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan CTS700"): str,
        vol.Required("host_ip"): str,
        vol.Required("host_port", default="502"): str,
        vol.Required("unit_id", default=1): int,
    }
)

STEP_SERIAL_CTS602_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan CTS602"): str,
        vol.Required("host_port"): str,
        vol.Required("unit_id", default=30): int,
    }
)

STEP_SERIAL_CTS700_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan CTS700"): str,
        vol.Required("host_port"): str,
        vol.Required("unit_id", default=1): int,
    }
)

STEP_TCP_DETECT_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan"): str,
        vol.Required("host_ip"): str,
        vol.Required("host_port", default="502"): str,
        vol.Optional("unit_id"): int,
    }
)

STEP_SERIAL_DETECT_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Nilan"): str,
        vol.Required("host_port"): str,
        vol.Optional("unit_id"): int,
    }
)


class NilanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nilan Modbus."""

    VERSION = 3

    data: Optional[dict[str, Any]]

    def __init__(self) -> None:
        """Initialize flow state."""
        self._com_type: str | None = None
        self._board_type: str | None = None
        self._detect_result: dict[str, Any] | None = None
        self._pending_user_input: dict[str, Any] | None = None

    def _flow_placeholders(self) -> dict[str, str]:
        """Shared description placeholders (warnings stay empty when OK)."""
        warning = coexistence_warning(self.hass)
        conflict = find_conflicting_modbus_hub(self.hass)
        return {
            "coexistence_warning": warning,
            "hub_conflict": conflict or "",
        }

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        """Invoke when a user initiates a flow via the user interface."""
        return await self.async_step_menu(user_input)

    async def async_step_menu(self, user_input: Optional[dict[str, Any]] = None):
        """Show Communications Selection."""
        return self.async_show_menu(
            step_id="menu",
            menu_options=await async_menu_options(self.hass, "menu"),
            description_placeholders=self._flow_placeholders(),
        )

    async def async_step_tcp(self, user_input: Optional[dict[str, Any]] = None):
        """Select board type after choosing TCP."""
        self._com_type = "tcp"
        return await self.async_step_board()

    async def async_step_serial(self, user_input: Optional[dict[str, Any]] = None):
        """Select board type after choosing Serial."""
        self._com_type = "serial"
        return await self.async_step_board()

    async def async_step_board(self, user_input: Optional[dict[str, Any]] = None):
        """Choose auto-detect, CTS602, or a CTS700 era map."""
        # Dict labels stay visible if YAML hub ``nilan`` blanks translations (#6).
        return self.async_show_menu(
            step_id="board",
            menu_options=await async_menu_options(self.hass, "board"),
            description_placeholders=self._flow_placeholders(),
        )

    async def async_step_auto_detect(self, user_input: Optional[dict[str, Any]] = None):
        """Connection form for auto-detect."""
        if self._com_type == "serial":
            return await self.async_step_serial_detect()
        return await self.async_step_tcp_detect()

    async def async_step_tcp_detect(self, user_input: Optional[dict[str, Any]] = None):
        """TCP connection details then probe board type."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                detected = await async_detect_board(
                    "tcp",
                    user_input["host_port"],
                    user_input["host_ip"],
                    user_input.get("unit_id"),
                )
            except ValueError as error:
                code = str(error)
                if code not in (
                    "cannot_connect",
                    "invalid_response",
                    "unsupported_device",
                    "cannot_detect",
                ):
                    code = "cannot_detect"
                errors["base"] = code
            if not errors:
                self._pending_user_input = {
                    "name": user_input["name"],
                    "host_ip": user_input["host_ip"],
                    "host_port": user_input["host_port"],
                    "com_type": "tcp",
                }
                self._detect_result = detected
                return await self.async_step_confirm()
        return self.async_show_form(
            step_id="tcp_detect",
            data_schema=STEP_TCP_DETECT_SCHEMA,
            errors=errors,
            description_placeholders=self._flow_placeholders(),
        )

    async def async_step_serial_detect(
        self, user_input: Optional[dict[str, Any]] = None
    ):
        """Serial connection details then probe board type."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                detected = await async_detect_board(
                    "serial",
                    user_input["host_port"],
                    None,
                    user_input.get("unit_id"),
                )
            except ValueError as error:
                code = str(error)
                if code not in (
                    "cannot_connect",
                    "invalid_response",
                    "unsupported_device",
                    "cannot_detect",
                ):
                    code = "cannot_detect"
                errors["base"] = code
            if not errors:
                self._pending_user_input = {
                    "name": user_input["name"],
                    "host_port": user_input["host_port"],
                    "host_ip": None,
                    "com_type": "serial",
                }
                self._detect_result = detected
                return await self.async_step_confirm()
        return self.async_show_form(
            step_id="serial_detect",
            data_schema=STEP_SERIAL_DETECT_SCHEMA,
            errors=errors,
            description_placeholders=self._flow_placeholders(),
        )

    async def async_step_confirm(self, user_input: Optional[dict[str, Any]] = None):
        """Confirm auto-detect result (menu: accept / manual)."""
        detected = self._detect_result or {}
        placeholders = self._flow_placeholders()
        placeholders.update(
            {
                "board_type": str(detected.get("board_type", "")),
                "model": str(detected.get("model", "")),
                "unit_id": str(detected.get("unit_id", "")),
            }
        )
        return self.async_show_menu(
            step_id="confirm",
            menu_options=await async_menu_options(self.hass, "confirm"),
            description_placeholders=placeholders,
        )

    async def async_step_accept(self, user_input: Optional[dict[str, Any]] = None):
        """Create entry from successful auto-detect."""
        pending = self._pending_user_input or {}
        detected = self._detect_result or {}
        self.data = {
            **pending,
            "unit_id": detected["unit_id"],
            "board_type": detected["board_type"],
        }
        return self.async_create_entry(title=pending["name"], data=self.data)

    async def async_step_manual(self, user_input: Optional[dict[str, Any]] = None):
        """Fall back to manual board choice after auto-detect."""
        self._detect_result = None
        self._pending_user_input = None
        return await self.async_step_board()

    async def async_step_cts602(self, user_input: Optional[dict[str, Any]] = None):
        """CTS602 selected; continue to connection form."""
        self._board_type = BOARD_TYPE_CTS602
        if self._com_type == "serial":
            return await self.async_step_serial_config()
        return await self.async_step_tcp_config()

    async def async_step_cts700(self, user_input: Optional[dict[str, Any]] = None):
        """CTS700 2018+ map selected; continue to connection form."""
        self._board_type = BOARD_TYPE_CTS700
        if self._com_type == "serial":
            return await self.async_step_serial_config()
        return await self.async_step_tcp_config()

    async def async_step_cts700_nordic(
        self, user_input: Optional[dict[str, Any]] = None
    ):
        """CTS700 Nordic XL hybrid map selected; continue to connection form."""
        self._board_type = BOARD_TYPE_CTS700_NORDIC
        if self._com_type == "serial":
            return await self.async_step_serial_config()
        return await self.async_step_tcp_config()

    async def async_step_cts700_legacy(
        self, user_input: Optional[dict[str, Any]] = None
    ):
        """CTS700 2015 map selected; continue to connection form."""
        self._board_type = BOARD_TYPE_CTS700_LEGACY
        if self._com_type == "serial":
            return await self.async_step_serial_config()
        return await self.async_step_tcp_config()

    async def async_step_tcp_config(self, user_input: Optional[dict[str, Any]] = None):
        """Configure ModBus TCP entry."""
        errors: dict[str, str] = {}
        board = self._board_type or BOARD_TYPE_CTS602
        schema = (
            STEP_TCP_CTS700_SCHEMA
            if is_cts700_schema_board(board)
            else STEP_TCP_CTS602_SCHEMA
        )

        if user_input is not None:
            try:
                if board == BOARD_TYPE_CTS700:
                    await async_validate_cts700(
                        "tcp",
                        user_input["host_port"],
                        user_input["unit_id"],
                        user_input["host_ip"],
                    )
                elif board == BOARD_TYPE_CTS700_NORDIC:
                    await async_validate_cts700_nordic(
                        "tcp",
                        user_input["host_port"],
                        user_input["unit_id"],
                        user_input["host_ip"],
                    )
                elif board == BOARD_TYPE_CTS700_LEGACY:
                    await async_validate_cts700_legacy(
                        "tcp",
                        user_input["host_port"],
                        user_input["unit_id"],
                        user_input["host_ip"],
                    )
                else:
                    await async_validate_cts602(
                        "tcp",
                        user_input["host_port"],
                        user_input["unit_id"],
                        user_input["host_ip"],
                    )
            except ValueError as error:
                errors["base"] = str(error)
            if not errors:
                self.data = user_input
                self.data.update({"com_type": "tcp"})
                self.data.update({"board_type": board})
                return self.async_create_entry(title=user_input["name"], data=self.data)
        return self.async_show_form(
            step_id="tcp_config",
            data_schema=schema,
            errors=errors,
            description_placeholders=self._flow_placeholders(),
        )

    async def async_step_serial_config(
        self, user_input: Optional[dict[str, Any]] = None
    ):
        """Configure ModBus Serial RTU entry."""
        errors: dict[str, str] = {}
        board = self._board_type or BOARD_TYPE_CTS602
        schema = (
            STEP_SERIAL_CTS700_SCHEMA
            if is_cts700_schema_board(board)
            else STEP_SERIAL_CTS602_SCHEMA
        )

        if user_input is not None:
            try:
                if board == BOARD_TYPE_CTS700:
                    await async_validate_cts700(
                        "serial", user_input["host_port"], user_input["unit_id"], None
                    )
                elif board == BOARD_TYPE_CTS700_NORDIC:
                    await async_validate_cts700_nordic(
                        "serial", user_input["host_port"], user_input["unit_id"], None
                    )
                elif board == BOARD_TYPE_CTS700_LEGACY:
                    await async_validate_cts700_legacy(
                        "serial", user_input["host_port"], user_input["unit_id"], None
                    )
                else:
                    await async_validate_cts602(
                        "serial", user_input["host_port"], user_input["unit_id"], None
                    )
            except ValueError as error:
                errors["base"] = str(error)
            if not errors:
                self.data = user_input
                self.data.update({"com_type": "serial"})
                self.data.update({"host_ip": None})
                self.data.update({"board_type": board})
                return self.async_create_entry(title=user_input["name"], data=self.data)
        return self.async_show_form(
            step_id="serial_config",
            data_schema=schema,
            errors=errors,
            description_placeholders=self._flow_placeholders(),
        )
