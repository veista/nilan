# GEO / slave 4 / space heating (dump-gated)

Floor / GEO / slave 4 maps are **not** claimed as fully supported on this fork until community register dumps exist.

## Status

| Path | GEO / space heating |
|---|---|
| CTS602 CompactP (type 44) with GEO software | Partial: AIR vs GEO probe exists; HPS entity path used when detected |
| CTS700 Compact P (2018+ / 2015) | Out of MVP scope for slave 4 / GEO |
| Compact P2 GEO3 / GEO6 / GEO9 | Prefer CTS602; full GEO dump-gated |

## What we need in a dump

- Model plate (P GEO / P2 GEO3/6/9)
- Board (CTS602 vs CTS700)
- Unit ids for indoor and any secondary / slave 4 node
- Holding/input reads for floor circuit temps, setpoints, and pump / valve states
- What the HMI labels those values

Use the [register dump checklist](../../CONTRIBUTING.md#register-dump-checklist).

## Dashboard

A dedicated GEO dashboard will ship when entities exist. Until then use:

- [`dashboards/cts602_overview.yaml`](../../dashboards/cts602_overview.yaml) for CTS602
- [`dashboards/cts700_compact_p.yaml`](../../dashboards/cts700_compact_p.yaml) for CTS700 air/DHW MVP

See [dashboards/README.md](../../dashboards/README.md) note on GEO.

## Related

- [Bolig matrix](../catalog/bolig-matrix.md)
- [CTS700 overview](README.md)
- [Compact P2](../cts602/compact-p2.md)
