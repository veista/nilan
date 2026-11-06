#!/usr/bin/env python3
"""Probe mark007 candidate holding registers on live CTS700 Nordic."""
from __future__ import annotations

from datetime import datetime

from pymodbus.client import ModbusTcpClient

HOST = "192.168.50.105"
PORT = 502
UNIT = 1


def to_s16(v: int) -> int:
    v = int(v) & 0xFFFF
    return v - 0x10000 if v >= 0x8000 else v


def read_one(client: ModbusTcpClient, address: int) -> tuple[str, int | None, int | None]:
    try:
        result = client.read_holding_registers(address=address, count=1, device_id=UNIT)
    except Exception as exc:  # noqa: BLE001
        return (f"exc:{exc}", None, None)
    if result is None:
        return ("no_response", None, None)
    if getattr(result, "isError", lambda: False)():
        return (f"err:{getattr(result, 'exception_code', None)}", None, None)
    raw = int(result.registers[0])
    return ("ok", raw, to_s16(raw))


def main() -> int:
    client = ModbusTcpClient(host=HOST, port=PORT, timeout=3)
    if not client.connect():
        print(f"cannot connect {HOST}:{PORT}")
        return 1

    regs = [
        ("main_compressor_effort", 4706),
        ("water_compressor_2", 4707),
        ("bypass_1", 4704),
        ("bypass_2", 4705),
        ("heater_control", 4701),
        ("holding_4702", 4702),
        ("holding_4703", 4703),
        ("holding_4708", 4708),
        ("holding_4709", 4709),
        ("holding_4710", 4710),
        ("holding_4711", 4711),
        ("holding_4712", 4712),
        ("supply_fan", 4699),
        ("extract_fan", 4700),
        ("compressor_state", 21775),
        ("bypass_pct", 21773),
        ("fan_power", 21771),
        ("op_mode", 5432),
        ("filter_interval_in", 1326),
        ("filter_interval_ex", 1327),
        ("filter_remain_in", 1328),
        ("filter_remain_ex", 1329),
        ("filter_days_20103", 20103),
        ("fan_step", 4747),
        ("room_set", 4746),
        # Candidate AI / effort / DHW max effort guesses near known maps
        ("holding_5549", 5549),
        ("holding_5550", 5550),
        ("holding_20461", 20461),
        ("holding_20462", 20462),
        ("holding_20463", 20463),
        ("holding_21774", 21774),
        ("holding_21776", 21776),
        ("holding_20104", 20104),
        ("holding_20105", 20105),
        ("holding_20106", 20106),
    ]

    print(f"probed_at={datetime.now().strftime('%d/%m/%Y %H:%M:%S')} host={HOST} unit={UNIT}")
    for label, addr in regs:
        status, raw, s16 = read_one(client, addr)
        if status == "ok":
            print(f"{label:28} {addr:5} raw={raw:5} s16={s16:5}")
        else:
            print(f"{label:28} {addr:5} {status}")

    block = client.read_holding_registers(address=4699, count=14, device_id=UNIT)
    if block is not None and not getattr(block, "isError", lambda: True)():
        print("BLOCK 4699-4712:")
        for i, v in enumerate(block.registers):
            print(f"  {4699 + i}: raw={v} s16={to_s16(v)}")
    else:
        print("BLOCK failed", getattr(block, "exception_code", None))

    client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
