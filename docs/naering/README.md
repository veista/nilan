# Næring (commercial) research

Commercial units from [nilan.no/produkter](https://www.nilan.no/produkter) (Comfort 600+, VR, VPR, VPM, HCR).

## Findings (08/08/2026)

| Family | Controller (manuals / product pages) | Modbus | Integration path today |
|---|---|---|---|
| Comfort 600 / 1200 | CTS602 | RS485, default unit id 30 | Use **CTS602**; type id often unknown until dump |
| Comfort 5000 | Likely CTS602 | Research | Dump `control_type` |
| VPM 120–560 M2 and larger VPM | CTS602 (product guide) | RS485 Modbus | CTS602 when type id known |
| VPR / VR | CTS602 commercial gateway docs | RS485 | CTS602 when type id known |
| HCR 800T | Unknown | | `needs_dump` |
| Some older Comfort (App gateway table) | CTS400 also listed | RJ45 on CTS400 | [cts400.md](cts400.md) dump-gated |

Sources: Nilan Comfort 600 product page (CTS602 Modbus), Product Guide 2025 commercial (VPM M2 + CTS602), MB Gateway LAN instructions (commercial Comfort / VPM / VPR on CTS602; CTS400 for some residential Comfort).

## Implementation policy

1. **Do not** invent a commercial-only register map.
2. If Auto-detect / CTS602 reads a known `control_type` in `CTS602_DEVICE_TYPES`, the unit is supported like other CTS602 devices.
3. Unknown type ids fail with a clear dump request (see CONTRIBUTING).
4. Never route commercial units to CTS700 Compact P 20xxx maps unless a dump proves it.
5. Capability flag `commercial_scale` is reserved for large airflow entities when registers are verified.

## MVP registers to collect (per dump)

Temps (outdoor, supply, extract), fan step / airflow, humidity, filter days, alarms, setpoints. Optional: bypass, after-heat, cooling.

## Matrix

Full SKU list: [../catalog/naering-matrix.md](../catalog/naering-matrix.md).
