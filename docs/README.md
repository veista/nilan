# Device documentation

Setup guides for each controller / model supported by this integration.

## Controllers

Years are **document / map eras**, not exact first-build dates.

| Controller | Approx. years in use | Status | Docs |
|---|---|---|---|
| [CTS400](naering/cts400.md) | Older residential Comfort (named on some gateway docs with CTS602) | Not implemented | Dump-gated |
| [CTS602](cts602/README.md) | **~2008–present** (Modbus PDF 12/09/2008; Compact P2 + commercial still) | Stable | Full device list below |
| [CTS700](cts700/README.md) | **~2015–present** (2015 map, 2018 protocol, Nordic LC **2019**) | MVP (2015 / Nordic / 2018+) | [compact-p](cts700/compact-p.md) · [nordic-xl](cts700/compact-p-nordic-xl.md) · [legacy-2015](cts700/legacy-2015.md) · [geo](cts700/geo.md) |

## Product catalog (nilan.no)

| Matrix | Scope |
|---|---|
| [Bolig](catalog/bolig-matrix.md) | Residential SKUs |
| [Næring](catalog/naering-matrix.md) | Commercial SKUs |
| [Aliases](catalog/aliases.md) | Marketing name → HMI |
| [Compact P XL Nordic hub](catalog/compact-p-xl-nordic.md) | CTS602 vs CTS700 Nordic vs 2018+ |
| [Næring research](naering/README.md) | Commercial controller notes |

## Shared topics

- [Hardware and connection](hardware.md)
- [Installation](installation.md)
- [Manufacturer manuals (official links)](manuals.md)
- [Dashboards (Nilan only)](dashboards.md)
- [CTS700 AI packages (optional)](cts700-ai/README.md)
- [FAQ](faq.md)
- [Changelog (releases)](../changelog/README.md)

## CTS602 devices (HMI type names)

All types below are on the **CTS602** board (~**2008–present**). Pick by HMI type id / plate, not calendar year.

| HMI name | Type id | Guide |
|---|---|---|
| Comfort light | 2 | [comfort-light.md](cts602/comfort-light.md) |
| Comfort Polar | 3 | [comfort-polar.md](cts602/comfort-polar.md) |
| VPL 15c | 4 | [vpl-15c.md](cts602/vpl-15c.md) |
| CompactS | 10 | [compacts.md](cts602/compacts.md) |
| VP 18comp | 11 | [vp-18comp.md](cts602/vp-18comp.md) |
| VP18cCom | 12 | [vp18ccom.md](cts602/vp18ccom.md) |
| COMFORT | 13 | [comfort.md](cts602/comfort.md) |
| VP 18c | 19 | [vp-18c.md](cts602/vp-18c.md) |
| VP 18ek | 20 | [vp-18ek.md](cts602/vp-18ek.md) |
| VP 18cek | 21 | [vp-18cek.md](cts602/vp-18cek.md) |
| VPL 25c | 25 | [vpl-25c.md](cts602/vpl-25c.md) |
| VPM/28EC | 26 | [vpm-28ec.md](cts602/vpm-28ec.md) |
| VP18cCoB | 28 | [vp18ccob.md](cts602/vp18ccob.md) |
| COMPACTn | 30 | [compactn.md](cts602/compactn.md) |
| COMFORTn | 31 | [comfortn.md](cts602/comfortn.md) |
| VP18 M2 | 32 | [vp18-m2.md](cts602/vp18-m2.md) |
| COMBI 300 N | 33 | [combi-300-n.md](cts602/combi-300-n.md) |
| COMBI 302 | 35 | [combi-302.md](cts602/combi-302.md) |
| COMBI 302 T | 36 | [combi-302-t.md](cts602/combi-302-t.md) |
| VGU180 ek | 38 | [vgu180-ek.md](cts602/vgu180-ek.md) |
| VENTEC | 42 | [ventec.md](cts602/ventec.md) |
| CompactP (AIR/GEO) | 44 | [compactp.md](cts602/compactp.md) · [compact-p2.md](cts602/compact-p2.md) |

## CTS700 devices

| Model / map | Map / hardware years | Guide |
|---|---|---|
| CTS700 2015 legacy | PDF **20150826** (~2015; under 10000) | [legacy-2015.md](cts700/legacy-2015.md) |
| Compact P Nordic XL (hybrid) | LC drawings **2019**; fan **4747** = **101–104** | [compact-p-nordic-xl.md](cts700/compact-p-nordic-xl.md) |
| Compact P (2018+ Ethernet) | Protocol PDF **2018_04** (~2018–present) | [compact-p.md](cts700/compact-p.md) |
| GEO / slave 4 | Same CTS700 eras when fitted | [geo.md](cts700/geo.md) (dump-gated) |

## Contributing and license

- [Contributing](../CONTRIBUTING.md)
- [License](../LICENSE)
