"""Modbus probe helpers for Nilan config flow.

Auto-detect order (compatibility contract):
1. CTS602 (incl. commercial units that share CTS602)
2. CTS700 Nordic hybrid (holding 4747 in 101-104)
3. CTS700 2018+ (20xxx outdoor temp)
4. CTS700 2015 legacy

Never force commercial VR/VPM/Comfort 600 onto CTS700 Compact P maps
without a dump. CTS400 is not probed until a verified map exists.
"""

from __future__ import annotations

import logging
from typing import Any

from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from .const import (
    BOARD_TYPE_CTS602,
    BOARD_TYPE_CTS700,
    BOARD_TYPE_CTS700_LEGACY,
    BOARD_TYPE_CTS700_NORDIC,
)
from .device_map import CTS602_DEVICE_TYPES
from .registers import (
    CTS602HoldingRegisters,
    CTS700LegacyHoldingRegisters,
    CTS700NewHoldingRegisters,
    CTS700NordicRegisters,
)

# Scaled CTS700 temps (register / 10). Plausible outdoor/extract band.
_CTS700_TEMP_MIN = -40.0
_CTS700_TEMP_MAX = 80.0
_NORDIC_FAN_STEPS = frozenset({101, 102, 103, 104})

_LOGGER = logging.getLogger(__name__)


def holding_u16(registers: list) -> int | None:
    """Decode first holding register as unsigned little-endian."""
    if not registers:
        return None
    return int.from_bytes(
        registers[0].to_bytes(2, "little", signed=False),
        "little",
        signed=False,
    )


def holding_s16_temp(registers: list) -> float | None:
    """Decode first holding register as signed temp with 0.1 scale."""
    if not registers:
        return None
    raw = int.from_bytes(
        registers[0].to_bytes(2, "little", signed=False),
        "little",
        signed=True,
    )
    return float(raw) / 10.0


async def open_client(com_type: str, port, address: str | None):
    """Create and connect a Modbus client."""
    if com_type == "tcp":
        client = AsyncModbusTcpClient(address, port=port)
    else:
        client = AsyncModbusSerialClient(
            port=port,
            stopbits=1,
            bytesize=8,
            parity="E",
            baudrate=19200,
            timeout=1,
        )
    await client.connect()
    return client


async def async_validate_cts602(com_type, port, unit_id, address: str | None) -> int:
    """Validate CTS602 device model. Returns type id."""
    client = await open_client(com_type, port, address)
    try:
        result = await client.read_holding_registers(
            CTS602HoldingRegisters.control_type, count=1, device_id=int(unit_id)
        )
    except ModbusException as value_error:
        client.close()
        raise ValueError("cannot_connect") from value_error
    if hasattr(result, "message"):
        client.close()
        raise ValueError("invalid_response")
    if result is None or len(result.registers) == 0:
        client.close()
        raise ValueError("invalid_response")
    value_output = holding_u16(result.registers)
    client.close()
    if value_output is None or value_output not in CTS602_DEVICE_TYPES:
        _LOGGER.debug(
            "Device Type %s not found in supported devices list",
            str(value_output),
        )
        raise ValueError("unsupported_device")
    return value_output


async def async_validate_cts700_nordic(
    com_type, port, unit_id, address: str | None
) -> None:
    """Validate Nordic hybrid: fan step 101-104 and T3 input readable."""
    client = await open_client(com_type, port, address)
    try:
        fan = await client.read_holding_registers(
            CTS700NordicRegisters.user_fan_step,
            count=1,
            device_id=int(unit_id),
        )
        extract = await client.read_input_registers(
            CTS700NordicRegisters.t3_extract,
            count=1,
            device_id=int(unit_id),
        )
    except ModbusException as value_error:
        client.close()
        raise ValueError("cannot_connect") from value_error
    if hasattr(fan, "message") or hasattr(extract, "message"):
        client.close()
        raise ValueError("invalid_response")
    if (
        fan is None
        or extract is None
        or len(fan.registers) == 0
        or len(extract.registers) == 0
    ):
        client.close()
        raise ValueError("invalid_response")
    fan_val = holding_u16(fan.registers)
    extract_c = holding_s16_temp(extract.registers)
    client.close()
    if fan_val not in _NORDIC_FAN_STEPS:
        raise ValueError("invalid_response")
    if (
        extract_c is None
        or extract_c < _CTS700_TEMP_MIN
        or extract_c > _CTS700_TEMP_MAX
    ):
        raise ValueError("invalid_response")


async def async_validate_cts700(com_type, port, unit_id, address: str | None) -> None:
    """Validate CTS700 (2018+ map) by probing outdoor temperature register."""
    client = await open_client(com_type, port, address)
    try:
        result = await client.read_holding_registers(
            CTS700NewHoldingRegisters.t1_outdoor_air_temperature,
            count=1,
            device_id=int(unit_id),
        )
    except ModbusException as value_error:
        client.close()
        raise ValueError("cannot_connect") from value_error
    if hasattr(result, "message"):
        client.close()
        raise ValueError("invalid_response")
    if result is None or len(result.registers) == 0:
        client.close()
        raise ValueError("invalid_response")
    temp = holding_s16_temp(result.registers)
    client.close()
    if temp is None or temp < _CTS700_TEMP_MIN or temp > _CTS700_TEMP_MAX:
        raise ValueError("invalid_response")


async def async_validate_cts700_legacy(
    com_type, port, unit_id, address: str | None
) -> None:
    """Validate CTS700 2015 map via T1 and user setpoint registers."""
    client = await open_client(com_type, port, address)
    try:
        outdoor = await client.read_holding_registers(
            CTS700LegacyHoldingRegisters.tsens1,
            count=1,
            device_id=int(unit_id),
        )
        setpoint = await client.read_holding_registers(
            CTS700LegacyHoldingRegisters.user_temperature,
            count=1,
            device_id=int(unit_id),
        )
    except ModbusException as value_error:
        client.close()
        raise ValueError("cannot_connect") from value_error
    if hasattr(outdoor, "message") or hasattr(setpoint, "message"):
        client.close()
        raise ValueError("invalid_response")
    if (
        outdoor is None
        or setpoint is None
        or len(outdoor.registers) == 0
        or len(setpoint.registers) == 0
    ):
        client.close()
        raise ValueError("invalid_response")
    outdoor_c = holding_s16_temp(outdoor.registers)
    setpoint_c = holding_s16_temp(setpoint.registers)
    client.close()
    if outdoor_c is None or outdoor_c < _CTS700_TEMP_MIN or outdoor_c > _CTS700_TEMP_MAX:
        raise ValueError("invalid_response")
    if setpoint_c is None or setpoint_c < 5.0 or setpoint_c > 50.0:
        raise ValueError("invalid_response")
    # Reject Nordic step encoding mis-classified as percent legacy.
    client2 = await open_client(com_type, port, address)
    try:
        fan = await client2.read_holding_registers(
            CTS700LegacyHoldingRegisters.user_fan_speed,
            count=1,
            device_id=int(unit_id),
        )
    except ModbusException:
        client2.close()
        return
    if fan is not None and not hasattr(fan, "message") and len(fan.registers) > 0:
        fan_val = holding_u16(fan.registers)
        if fan_val in _NORDIC_FAN_STEPS:
            client2.close()
            raise ValueError("invalid_response")
    client2.close()


def is_cts700_schema_board(board: str) -> bool:
    """True when board uses CTS700 TCP/Serial defaults (unit id 1)."""
    return board in (
        BOARD_TYPE_CTS700,
        BOARD_TYPE_CTS700_LEGACY,
        BOARD_TYPE_CTS700_NORDIC,
    )


async def async_detect_board(
    com_type: str, port, address: str | None, unit_id: int | None
) -> dict[str, Any]:
    """Probe CTS602, Nordic, 2018+, then 2015. Returns board info."""
    candidates: list[int] = []
    if unit_id is not None:
        candidates.append(int(unit_id))
    for default_id in (1, 30):
        if default_id not in candidates:
            candidates.append(default_id)

    last_error = "cannot_detect"
    for candidate in candidates:
        try:
            type_id = await async_validate_cts602(com_type, port, candidate, address)
            return {
                "board_type": BOARD_TYPE_CTS602,
                "unit_id": candidate,
                "model": CTS602_DEVICE_TYPES[type_id],
                "type_id": type_id,
            }
        except ValueError as err:
            last_error = str(err)
            _LOGGER.debug("CTS602 probe unit_id=%s failed: %s", candidate, err)

        try:
            await async_validate_cts700_nordic(com_type, port, candidate, address)
            return {
                "board_type": BOARD_TYPE_CTS700_NORDIC,
                "unit_id": candidate,
                "model": "Compact P Nordic XL CTS700",
                "type_id": None,
            }
        except ValueError as err:
            last_error = str(err)
            _LOGGER.debug("CTS700 Nordic probe unit_id=%s failed: %s", candidate, err)

        try:
            await async_validate_cts700(com_type, port, candidate, address)
            return {
                "board_type": BOARD_TYPE_CTS700,
                "unit_id": candidate,
                "model": "Compact P CTS700 (2018+ map)",
                "type_id": None,
            }
        except ValueError as err:
            last_error = str(err)
            _LOGGER.debug("CTS700 probe unit_id=%s failed: %s", candidate, err)

        try:
            await async_validate_cts700_legacy(com_type, port, candidate, address)
            return {
                "board_type": BOARD_TYPE_CTS700_LEGACY,
                "unit_id": candidate,
                "model": "CTS700 (2015 map)",
                "type_id": None,
            }
        except ValueError as err:
            last_error = str(err)
            _LOGGER.debug("CTS700 legacy probe unit_id=%s failed: %s", candidate, err)

    raise ValueError(last_error if last_error else "cannot_detect")
