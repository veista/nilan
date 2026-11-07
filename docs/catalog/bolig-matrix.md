# Bolig product coverage matrix

Source catalog: [nilan.no/produkter](https://www.nilan.no/produkter) (Boligløsninger).

Status values:

| Status | Meaning |
|---|---|
| `supported` | Known controller path; HMI type or CTS700 map verified in this fork |
| `partial` | Connects on a family path; some features (GEO, slave 4, variants) dump-gated |
| `needs_dump` | Marketing model listed; needs `control_type` / register dump to confirm |
| `research` | Controller hypothesis from manuals; not live-verified here |

Capability flags: `vent`, `passive`, `active`, `heat`, `cool`, `dhw`, `space`, `geo` (from the site columns).

| Catalog SKU | Max air (m3/h) | Caps (site) | Controller path | HMI / map | Status | Notes |
|---|---|---|---|---|---|---|
| Comfort CT200 | 198 | vent,passive | CTS602 | Comfort light / COMFORT / COMFORTn | `partial` | Alias; confirm type id |
| Comfort CT500 | 500 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | Alias; confirm type id |
| Comfort 200 Top | 308 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | |
| Comfort 250 Top | 250 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | |
| Comfort 350 Top | 372 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | |
| Comfort 300LR | 400 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | |
| Comfort 250L / 250R | 250 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | |
| Comfort 350L / 350R | 372 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | |
| Comfort 450 | 525 | vent,passive | CTS602 | COMFORT / COMFORTn | `partial` | |
| Combi 400 Polar Top | 425 | vent,passive,active,heat,cool | CTS602 | COMBI* | `needs_dump` | Type id unknown |
| Combi 302 Polar | 375 | vent,passive,active,heat,cool | CTS602 | COMBI 302 (35) | `supported` | |
| Combi 302 Polar Top | 430 | vent,passive,active,heat,cool | CTS602 | COMBI 302 T (36) | `supported` | Confirm Polar naming |
| Combi S 302 Polar Top | 340 | vent,passive,active,heat,cool | CTS602 | COMBI 300 N (33) / 302 | `partial` | Confirm S variant |
| VPL 15 Top M2 | 400 | vent,passive,active,heat,cool | CTS602 | VPL 15c (4) | `partial` | M2 alias |
| VPL 15 | 425 | vent,passive,active,heat,cool | CTS602 | VPL 15c (4) | `supported` | |
| VPL 28 | 1000 | vent,passive,active,heat,cool | CTS602 | VPM/28EC (26) | `partial` | Confirm vs commercial VPM |
| Compact P2 | 425 | vent,passive,active,heat,cool,dhw | CTS602 | CompactP (44) | `research` | Manuals: CTS602 HMI |
| Compact P2 GEO3 | 425 | +geo,space | CTS602 | CompactP GEO | `partial` | GEO dump-gated |
| Compact P2 GEO6 | 425 | +geo,space | CTS602 | CompactP GEO | `partial` | GEO dump-gated |
| Compact P2 GEO9 | 425 | +geo,space | CTS602 | CompactP GEO | `partial` | GEO dump-gated |
| Compact P2 AIR E-Silent | 425 | vent,passive,active,heat,cool,dhw | CTS602 | CompactP AIR | `research` | Prefer CTS602 |
| Compact P2 AIR | 425 | vent,passive,active,heat,cool,dhw | CTS602 | CompactP AIR | `research` | Prefer CTS602 |
| Compact P2 EK | 425 | vent,passive,active,heat,cool,dhw | CTS602 | CompactP | `research` | Prefer CTS602 |
| Compact P Nordic | 275 | vent,passive,active,heat,cool,dhw | CTS602 44 or CTS700 | CompactP / CTS700 | `partial` | Board depends on unit |
| Compact P XL Nordic | 430 | vent,passive,active,heat,cool,dhw | CTS602 44 or CTS700_NORDIC or CTS700 | CompactP / CTS700_NORDIC / CTS700 | `supported` | See [compact-p-xl-nordic](compact-p-xl-nordic.md) |
| Compact P Køl Polar/Nordic/Arctic (XL) | 430 | vent,passive,active,heat,cool,dhw | CTS700 LC (75124xx) | CTS700_NORDIC | `supported` | Wiring CTS700 LC v4.0; [hardware](../cts700/hardware/) |
| Compact P GEO | 275 | +geo,space | CTS602 44 or CTS700 | CompactP GEO | `partial` | Slave 4 dump-gated on CTS700 |
| Compact P AIR | 275 | vent,passive,active,heat,cool,dhw | CTS602 44 or CTS700 | CompactP AIR / CTS700 | `partial` | |
| Compact P EK | 275 | vent,passive,active,heat,cool,dhw | CTS602 44 or CTS700 | CompactP / CTS700 | `partial` | |
| Compact S | 340 | vent,passive,active,heat,cool,dhw | CTS602 | CompactS (10) | `supported` | |
| VP 18 M2 | 425 | vent,passive,active,heat,cool,dhw | CTS602 | VP18 M2 (32) | `supported` | |
| VP 18 M2 EK | 425 | vent,passive,active,heat,cool,dhw | CTS602 | VP 18ek family | `partial` | Confirm type id |
| VGU 250 M2 Nordic | | dhw,space | CTS602 | unknown | `needs_dump` | |
| VGU 180 EK | | dhw,space | CTS602 | VGU180 ek (38) | `supported` | |

## Board choice

| Situation | Config board |
|---|---|
| HMI / plate says CTS602, typical unit id 30 | CTS602 or Auto-detect |
| Compact P with Ethernet Modbus TCP, unit id 1, 20xxx registers | CTS700 (2018+) |
| Holding 4747 in 101–104 (Nordic step fan) | CTS700 Compact P Nordic XL |
| Older CTS700 map under 10000, 4747 percent | CTS700 (2015 legacy) |
| Compact P XL Nordic catalog / type 44 RS485 | CTS602 first; see [compact-p-xl-nordic](compact-p-xl-nordic.md) |
| Compact P2 (current manuals) | CTS602 first |

## Related

- [Marketing aliases](aliases.md)
- [Næring matrix](naering-matrix.md)
- [GEO / slave 4](../cts700/geo.md)
- [Dump checklist](../../CONTRIBUTING.md#register-dump-checklist)
