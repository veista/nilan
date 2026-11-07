#!/usr/bin/env python3
"""Read-only probe: DHW vs HVAC mode registers (mark007 question)."""
from __future__ import annotations

from datetime import datetime

from pymodbus.client import ModbusTcpClient

HOST = "192.168.50.105"
PORT = 502
UNIT = 1


def to_s16(v: int) -> int:
    v = int(v) & 0xFFFF
    return v - 0x10000 if v >= 0x8000 else v


def read_one(client: ModbusTcpClient, kind: str, address: int):
    try:
        if kind == "h":
            result = client.read_holding_registers(
                address=address, count=1, device_id=UNIT
            )
        else:
            result = client.read_input_registers(
                address=address, count=1, device_id=UNIT
            )
    except Exception as exc:  # noqa: BLE001
        return f"exc:{exc}", None, None
    if result is None:
        return "no_response", None, None
    if getattr(result, "isError", lambda: False)():
        return f"err:{getattr(result, 'exception_code', None)}", None, None
    raw = int(result.registers[0])
    return "ok", raw, to_s16(raw)


def main() -> int:
    client = ModbusTcpClient(host=HOST, port=PORT, timeout=3)
    if not client.connect():
        print(f"cannot connect {HOST}:{PORT}")
        return 1

    print(
        f"probed_at={datetime.now().strftime('%d/%m/%Y %H:%M:%S')} "
        f"host={HOST} unit={UNIT}"
    )

    holdings = [
        ("effort_4706", 4706),
        ("heater_4701", 4701),
        ("op_mode_5432", 5432),
        ("operating_mode_20120", 20120),
        ("cooling_prio_dhw_20184", 20184),
        ("hot_water_prio_1702", 1702),
        ("control_mode_set_1002h", 1002),
        ("room_set_4746", 4746),
        ("dhw_set_20460", 20460),
        ("dhw_dial_5548", 5548),
        ("fan_4747", 4747),
        ("dhw_pause_20440", 20440),
        ("allow_cool_20180", 20180),
        ("sys_mode_1047", 1047),
        ("op_type_2402", 2402),
    ]
    inputs = [
        ("control_state_1002i", 1002),
        ("T3_room_5154", 5154),
        ("T11_dhw_5162", 5162),
        ("T12_dhw_5163", 5163),
        ("T1_out_5152", 5152),
        ("T2_supply_5153", 5153),
        ("RH_4716", 4716),
    ]

    print("--- HOLDING ---")
    for label, addr in holdings:
        status, raw, s16 = read_one(client, "h", addr)
        if status == "ok":
            print(f"{label:28} {addr:5} raw={raw:5} s16={s16:5}")
        else:
            print(f"{label:28} {addr:5} {status}")

    print("--- INPUT ---")
    for label, addr in inputs:
        status, raw, s16 = read_one(client, "i", addr)
        if status == "ok":
            extra = ""
            if addr in (5154, 5162, 5163, 5152, 5153):
                extra = f" temp={s16 / 10:.1f}C"
            print(f"{label:28} {addr:5} raw={raw:5} s16={s16:5}{extra}")
        else:
            print(f"{label:28} {addr:5} {status}")

    # Map 5432 -> panel-like label for this snapshot
    _, raw5432, _ = read_one(client, "h", 5432)
    _, effort, _ = read_one(client, "h", 4706)
    label_map = {
        0: "Off",
        1: "Cooling",
        2: "Heating",
        3: "Dehumidification",
        4: "Hot water production / DHW",
    }
    print("--- INTERPRET ---")
    print(f"5432 raw={raw5432} -> {label_map.get(raw5432, 'unknown')}")
    print(f"4706 effort={effort} (heat_pump active={bool(effort and effort > 0)})")
    if raw5432 == 4:
        print("NOTE: panel Hot water production; control_state should be 9")
    elif raw5432 == 2 and effort and effort > 0:
        print("NOTE: panel Heating with compressor effort; control_state should be 7")
    elif raw5432 == 1 and effort and effort > 0:
        print("NOTE: panel Cooling with compressor effort; control_state should be 8")

    client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
