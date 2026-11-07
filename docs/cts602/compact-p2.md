# Compact P2 (CTS602)

| Item | Value |
|---|---|
| Controller | **CTS602** (current Nilan installation manuals) |
| HMI type name | CompactP (expected) |
| Control type id | 44 (confirm on your unit) |
| Typical unit id | **30** |
| Config board choice | CTS602 or Auto-detect |

## Marketing variants

Compact P2, Compact P2 AIR, Compact P2 AIR E-Silent, Compact P2 EK, Compact P2 GEO3 / GEO6 / GEO9.

## Important

- Prefer the **CTS602** board path for Compact P2. Manuals list Automation CTS602 / CTS602 HMI and Modbus RTU (default address 30).
- Do **not** choose CTS700 2018+ (20xxx Ethernet map) for P2 unless a register dump proves those registers answer.
- Older Compact P units with Ethernet Modbus TCP on unit id 1 still use [../cts700/compact-p.md](../cts700/compact-p.md).

## Setup

1. Install the integration ([installation](../installation.md)).
2. Add **Nilan** → **TCP** (via RS485 bridge) or **Serial**.
3. Select **CTS602** or **Auto-detect**.
4. Unit id **30** unless your HMI uses another address.
5. Confirm model shows CompactP, CompactP AIR, or CompactP GEO.

## GEO

GEO variants need slave / HPS dumps for full floor heating coverage. See [../cts700/geo.md](../cts700/geo.md) and [../catalog/bolig-matrix.md](../catalog/bolig-matrix.md).

## Troubleshooting

- Unsupported device type: share `control_type` and photos ([CONTRIBUTING.md](../../CONTRIBUTING.md#register-dump-checklist)).
- See also [compactp.md](compactp.md) (CTS602 CompactP family).
