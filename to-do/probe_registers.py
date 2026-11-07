#!/usr/bin/env python3
"""One-shot Modbus TCP register probe (issue #3 matrix). Example host: 192.168.1.50"""
from __future__ import annotations

import json
import sys
from datetime import datetime

try:
    from pymodbus.client import ModbusTcpClient
except ImportError:
    print("pymodbus required: pip install pymodbus", file=sys.stderr)
    sys.exit(1)

HOST = "192.168.1.50"
PORT = 502
UNIT = 1

# (label, reg_type, address)
REGISTERS = [
    ("filter_interval_inlet", "holding", 1326),
    ("filter_interval_exhaust", "holding", 1327),
    ("filter_remaining_inlet", "holding", 1328),
    ("filter_remaining_exhaust", "holding", 1329),
    ("filter_days_20103", "holding", 20103),
    ("room_setpoint_4746", "holding", 4746),
    ("room_setpoint_20102", "holding", 20102),
    ("fan_step_4747", "holding", 4747),
    ("fan_pct_21771", "holding", 21771),
    ("supply_fan_4699", "holding", 4699),
    ("extract_fan_4700", "holding", 4700),
    ("t4_20288", "holding", 20288),
    ("t5_20290", "holding", 20290),
    ("t6_20292", "holding", 20292),
    ("t8_20296", "holding", 20296),
    ("t4_5155", "holding", 5155),
    ("t5_5156", "holding", 5156),
    ("t6_5157", "holding", 5157),
    ("t8_5159", "input", 5159),
    ("dhw_setpoint_5548", "holding", 5548),
    ("dhw_setpoint_20460", "holding", 20460),
    ("dhw_top_5162", "input", 5162),
    ("humidity_4716", "input", 4716),
    ("avg_humidity_20164", "holding", 20164),
    ("op_mode_5432", "holding", 5432),
]


def probe_one(client: ModbusTcpClient, reg_type: str, address: int) -> dict:
    try:
        if reg_type == "holding":
            result = client.read_holding_registers(address=address, count=1, device_id=UNIT)
        else:
            result = client.read_input_registers(address=address, count=1, device_id=UNIT)
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "detail": str(exc)}

    if result is None:
        return {"status": "error", "detail": "no response"}

    if getattr(result, "isError", lambda: False)():
        exc_code = None
        if hasattr(result, "exception_code"):
            exc_code = result.exception_code
        return {"status": "exception", "exception_code": exc_code}

    values = getattr(result, "registers", None) or getattr(result, "bits", None)
    if not values:
        return {"status": "error", "detail": "empty registers"}

    return {"status": "ok", "value": int(values[0])}


def main() -> int:
    client = ModbusTcpClient(host=HOST, port=PORT, timeout=3)
    if not client.connect():
        print(json.dumps({"error": f"cannot connect to {HOST}:{PORT}"}, indent=2))
        return 1

    rows = []
    for label, reg_type, address in REGISTERS:
        outcome = probe_one(client, reg_type, address)
        rows.append(
            {
                "label": label,
                "type": reg_type,
                "address": address,
                **outcome,
            }
        )

    client.close()

    dead = [r for r in rows if r.get("status") != "ok"]
    alive = [r for r in rows if r.get("status") == "ok"]

    summary = {
        "host": HOST,
        "port": PORT,
        "unit": UNIT,
        "probed_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "alive_count": len(alive),
        "dead_count": len(dead),
        "registers": rows,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
