#!/usr/bin/env python3
"""Read-only probe of Nordic candidate holdings/inputs (LAN)."""
from __future__ import annotations

from datetime import datetime

from pymodbus.client import ModbusTcpClient

HOST = "192.168.50.105"
PORT = 502
UNIT = 1


def to_s16(v: int) -> int:
    v = int(v) & 0xFFFF
    return v - 0x10000 if v >= 0x8000 else v


def read_regs(client: ModbusTcpClient, kind: str, address: int, count: int = 1):
    try:
        if kind == "h":
            result = client.read_holding_registers(
                address=address, count=count, device_id=UNIT
            )
        else:
            result = client.read_input_registers(
                address=address, count=count, device_id=UNIT
            )
    except Exception as exc:  # noqa: BLE001
        return f"exc:{exc}"
    if result is None:
        return "no_response"
    if getattr(result, "isError", lambda: False)():
        return f"err:{getattr(result, 'exception_code', None)}"
    out = []
    for i, raw in enumerate(result.registers):
        raw_i = int(raw)
        out.append((address + i, raw_i, to_s16(raw_i)))
    return out


def main() -> int:
    client = ModbusTcpClient(host=HOST, port=PORT, timeout=3)
    if not client.connect():
        print(f"cannot connect {HOST}:{PORT}")
        return 1

    print(f"probed_at={datetime.now().strftime('%d/%m/%Y %H:%M:%S')} host={HOST}")

    singles = [
        ("vent_pause", "h", 20100),
        ("run_20101", "h", 20101),
        ("room_set_20102", "h", 20102),
        ("filter_20103", "h", 20103),
        ("dhw_20460", "h", 20460),
        ("dhw_dial_5548", "h", 5548),
        ("dhw_min_2828", "h", 2828),
        ("dhw_max_3935", "h", 3935),
        ("el_supp_20464", "h", 20464),
        ("t8_hold_20296", "h", 20296),
        ("avg_hum_20164", "h", 20164),
        ("hum_live", "i", 4716),
        ("filter_alarm", "i", 5168),
        ("anode", "h", 4233),
        ("op_mode", "h", 5432),
        ("heater_4701", "h", 4701),
        ("unk_4703", "h", 4703),
        ("unk_21774", "h", 21774),
        ("comp_st_21775", "h", 21775),
        ("unk_21776", "h", 21776),
        ("unk_21777", "h", 21777),
        ("unk_21778", "h", 21778),
        ("unk_21779", "h", 21779),
        ("unk_21780", "h", 21780),
        ("h20461", "h", 20461),
        ("h20462", "h", 20462),
        ("h20463", "h", 20463),
        ("h20105", "h", 20105),
        ("h20106", "h", 20106),
        ("h20107", "h", 20107),
        ("h20108", "h", 20108),
        ("pause_4727", "h", 4727),
        ("sys_mode_1047", "h", 1047),
        ("op_type_2402", "h", 2402),
        ("sw_5065", "h", 5065),
        ("alarm_i400", "i", 400),
        ("in_5164", "i", 5164),
        ("in_5165", "i", 5165),
        ("in_5166", "i", 5166),
        ("in_5167", "i", 5167),
        ("in_5169", "i", 5169),
        ("in_5170", "i", 5170),
        ("t1", "i", 5152),
        ("t2", "i", 5153),
        ("t3", "i", 5154),
        ("t8", "i", 5159),
        ("t11", "i", 5162),
        ("t12", "i", 5163),
        ("hum_20165", "h", 20165),
        ("hum_20166", "h", 20166),
        ("filt_1325", "h", 1325),
        ("filt_1330", "h", 1330),
        ("fan_step_4747", "h", 4747),
        ("room_4746", "h", 4746),
        ("effort_4706", "h", 4706),
        ("effort2_4707", "h", 4707),
        ("bypass_4704", "h", 4704),
        ("bypass_pct", "h", 21773),
        ("fan_pwr", "h", 21771),
    ]

    for label, kind, addr in singles:
        print(f"{label:20} {kind} {addr:5} {read_regs(client, kind, addr)}")

    print("BLOCK 20100-20110", read_regs(client, "h", 20100, 11))
    print("BLOCK 20460-20470", read_regs(client, "h", 20460, 11))
    print("BLOCK 21770-21780", read_regs(client, "h", 21770, 11))
    print("BLOCK 20280-20300", read_regs(client, "h", 20280, 21))

    client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
