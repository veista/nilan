# Næring product coverage matrix

Source catalog: [nilan.no/produkter](https://www.nilan.no/produkter) (Næringsløsninger).

Research summary: Comfort 600 / 1200 / commercial Comfort, VPM M2, and VPR lines ship with **CTS602** and open Modbus RS485 (default unit id **30**) per Nilan product pages and gateway docs. Some older residential Comfort units also list **CTS400** for the Nilan App gateway. This fork does **not** invent a CTS400 register map until dumps exist.

| Status | Meaning |
|---|---|
| `supported` | Same CTS602 path when HMI type id is already in `CTS602_DEVICE_TYPES` |
| `partial` | CTS602 board works for known type ids; commercial SKU alias not uniquely typed |
| `needs_dump` | Needs `control_type` dump to add or map type id |
| `research` | Manuals say CTS602 (or CTS400); not live-verified on this fork |

| Catalog SKU | Max air (m3/h) | Caps | Controller | Status | Notes |
|---|---|---|---|---|---|
| Comfort 600 | 800 | vent,passive | CTS602 | `research` | Product page: CTS602 Modbus |
| Comfort 1200 | 1675 | vent,passive | CTS602 | `research` | Product guide: CTS602 |
| Comfort 5000 | 5000 | vent,passive | CTS602 | `research` | Confirm SW / type id |
| HCR 800T | 1000 | vent,passive,active | unknown | `needs_dump` | |
| VR 120 | 1950 | vent,passive | CTS602 | `research` | Commercial CTS602 |
| VR 240 | 2650 | vent,passive | CTS602 | `research` | |
| VR 360 | 4150 | vent,passive | CTS602 | `research` | |
| VR 480 | 5600 | vent,passive | CTS602 | `research` | |
| VR 560 | 6500 | vent,passive | CTS602 | `research` | |
| VPR 120 | 1950 | vent,passive,active | CTS602 | `research` | |
| VPR 240 | 2650 | vent,passive,active | CTS602 | `research` | |
| VPR 360 | 4150 | vent,passive,active | CTS602 | `research` | |
| VPR 480 | 5600 | vent,passive,active | CTS602 | `research` | |
| VPR 560 | 6500 | vent,passive,active | CTS602 | `research` | |
| VPM 120 M2 | 1950 | vent,passive,active | CTS602 | `research` | Guide: CTS602 + Modbus |
| VPM 240 M2 | 2650 | vent,passive,active | CTS602 | `research` | |
| VPM 360 M2 | 4150 | vent,passive,active | CTS602 | `research` | |
| VPM 480 M2 | 4800 | vent,passive,active | CTS602 | `research` | |
| VPM 560 M2 | 6500 | vent,passive,active | CTS602 | `research` | |
| VPM 600 | 7000 | vent,passive,active | CTS602 | `research` | |
| VPM 700 | 9000 | vent,passive,active | CTS602 | `research` | |
| VPM 800 | 11000 | vent,passive,active | CTS602 | `research` | |
| VPM 1000 | 11000 | vent,passive,active | CTS602 | `research` | |
| VPM 1200 | 14500 | vent,passive,active | CTS602 | `research` | |
| VPM 1500 | 18000 | vent,passive,active | CTS602 | `research` | |
| VPM 2200 | 24000 | vent,passive,active | CTS602 | `research` | |
| VPM 3200 | 36000 | vent,passive,active | CTS602 | `research` | |
| VPM 240 Cleanroom | 2850 | vent,passive,active | CTS602 | `research` | |
| VPM 360 Cleanroom | 4400 | vent,passive,active | CTS602 | `research` | |
| VPM 480 Cleanroom | 5800 | vent,passive,active | CTS602 | `research` | |
| VPM 560 Cleanroom | 6600 | vent,passive,active | CTS602 | `research` | |
| VPM 700 Cleanroom | 9000 | vent,passive,active | CTS602 | `research` | |
| VPM 800 Cleanroom | 11000 | vent,passive,active | CTS602 | `research` | |
| VPM 1000 Cleanroom | 11000 | vent,passive,active | CTS602 | `research` | |
| VPM 1200 Cleanroom | 14500 | vent,passive,active | CTS602 | `research` | |
| VPM 1500 Cleanroom | 18000 | vent,passive,active | CTS602 | `research` | |
| VPM 2200 Cleanroom | 24000 | vent,passive,active | CTS602 | `research` | |

Do **not** assume bolig HMI id `VPM/28EC` (26) covers VPM 120+.

## How to connect today

1. Prefer board **CTS602** (or Auto-detect).
2. Typical unit id **30**, Modbus RTU via bridge, or native RS485 wiring per unit manual.
3. If install fails with unsupported device type, open a dump issue ([checklist](../../CONTRIBUTING.md#register-dump-checklist)).
4. Do **not** select CTS700 Compact P maps for commercial VR/VPR/VPM unless a dump proves 20xxx answers.

## Related

- [Næring research notes](../naering/README.md)
- [Bolig matrix](bolig-matrix.md)
- [CTS400 note](../naering/cts400.md)
