#!/usr/bin/env python3
"""Restore Nordic holdings after probe write tests. Safe FC6 with retries."""
from __future__ import annotations

import time
from datetime import datetime

from pymodbus.client import ModbusTcpClient

HOST = "192.168.50.105"
PORT = 502
UNIT = 1

# Desired safe baseline after probes
WANT = {
    20100: 0,  # vent pause off
    20440: 0,  # dhw pause off
    20180: 0,  # cooling enable (leave as found earlier: 0)
    20300: 1,  # frost protection on
    20464: 1,  # el supplement (was 1 before tests)
    20481: 1,  # auto legionella on
    4747: 80,  # fan percent observed
}


def connect() -> ModbusTcpClient:
    client = ModbusTcpClient(host=HOST, port=PORT, timeout=5)
    if not client.connect():
        raise SystemExit(f"cannot connect {HOST}:{PORT}")
    return client


def read_h(client: ModbusTcpClient, address: int) -> int | None:
    for _ in range(3):
        try:
            result = client.read_holding_registers(
                address=address, count=1, device_id=UNIT
            )
            if result is not None and not getattr(result, "isError", lambda: True)():
                return int(result.registers[0])
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.8)
    return None


def write_h(client: ModbusTcpClient, address: int, value: int) -> bool:
    try:
        result = client.write_register(address=address, value=value, device_id=UNIT)
        if result is not None and not getattr(result, "isError", lambda: True)():
            return True
    except Exception:  # noqa: BLE001
        pass
    try:
        result = client.write_registers(
            address=address, values=[value], device_id=UNIT
        )
        if result is not None and not getattr(result, "isError", lambda: True)():
            return True
    except Exception:  # noqa: BLE001
        return False
    return False


def main() -> int:
    print(f"restore_at={datetime.now().strftime('%d/%m/%Y %H:%M:%S')} host={HOST}")
    client = connect()
    try:
        for address, wanted in WANT.items():
            current = read_h(client, address)
            print(f"  {address}: current={current} want={wanted}")
            if current is None:
                client.close()
                time.sleep(2)
                client = connect()
                current = read_h(client, address)
            if current == wanted:
                continue
            ok = write_h(client, address, wanted)
            time.sleep(1.2)
            after = read_h(client, address)
            print(f"    write_ok={ok} after={after}")
            if after != wanted:
                write_h(client, address, wanted)
                time.sleep(1.5)
                print(f"    retry after={read_h(client, address)}")
        print("SNAP", {a: read_h(client, a) for a in WANT})
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
