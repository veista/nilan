[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

# Nilan

Modbus TCP/RTU integration for Nilan ventilation and Compact units in Home Assistant.

[Docs](docs/README.md) · [Changelog](changelog/README.md) · [Installation](docs/installation.md) · [Dashboards](docs/dashboards.md) · [Contributing](CONTRIBUTING.md) · [Contributors](CONTRIBUTORS.md) · [Security](SECURITY.md) · [Accessibility](ACCESSIBILITY.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [License](LICENSE)

## Vision (this fork)

Ship CTS700 Compact P eras (2015 / Nordic XL / 2018+) beside stable CTS602, document the full [nilan.no/produkter](https://www.nilan.no/produkter) catalog (bolig + næring) via coverage matrices, fix community CTS602 bugs, and keep shared Lovelace **Nilan-only**. GEO / slave 4 and CTS400 stay dump-gated until maps exist.

## Quick start

1. Install via [Marketplace / HACS](docs/installation.md) (default upstream, or this fork as a custom repository while testing). On Home Assistant **2026.11+** the store UI is labeled **Marketplace** (`/marketplace/...`); older Core still shows **HACS**.
2. Add **Nilan** → **TCP** or **Serial** → **Auto-detect** (or choose **CTS602** / **CTS700 2018+** / **CTS700 Nordic XL** / **CTS700 2015** manually).
3. Confirm the detected board and unit id, or override manually.
4. Typical unit ids: CTS602 **30**, Compact P CTS700 **1** (TCP port **502**).

**Is my model supported?** See the catalog matrices:

- [Bolig matrix](docs/catalog/bolig-matrix.md)
- [Næring matrix](docs/catalog/naering-matrix.md)
- [Marketing aliases](docs/catalog/aliases.md)
- [Compact P XL Nordic hub](docs/catalog/compact-p-xl-nordic.md)

**CTS700 maps:** era matrix in [cts700 README](docs/cts700/README.md). **2018+** 20xxx ([compact-p](docs/cts700/compact-p.md)), **Nordic XL** hybrid ([compact-p-nordic-xl](docs/cts700/compact-p-nordic-xl.md)), **2015** under 10000 ([legacy-2015](docs/cts700/legacy-2015.md)). Per-board Modbus YAML: [`modbus_yaml/`](modbus_yaml/). **Compact P2** prefers CTS602 ([compact-p2](docs/cts602/compact-p2.md)). Optional lag-aware 24/7 helpers: [CTS700 AI packages](docs/cts700-ai/README.md).

### Install from this fork (Marketplace / HACS custom repository)

Until CTS700 and related fixes are merged upstream:

1. **Marketplace** (HA 2026.11+) or **HACS** (older) → three-dot menu → **Custom repositories**
2. URL: `https://github.com/master3395/veista-nilan` (Marketplace custom repository id **1323343841**; deep link `/marketplace/repository/1323343841`)
3. Category: **Integration**
4. Download **Nilan** → restart Home Assistant
5. If you already had veista/nilan installed, remove the old integration entry first (same domain)

Fork: https://github.com/master3395/veista-nilan (`master`) · full steps: [docs/installation.md](docs/installation.md)

## Controllers

Years below are **document / map eras** (Nilan Modbus PDFs, drawings, current product guides), not exact factory “first unit built” dates. Many SKUs ship for years across controller generations.

| Controller | Approx. years in use | Status | Overview |
|---|---|---|---|
| CTS400 | Older residential Comfort (still named on some gateway / App docs alongside CTS602) | Not implemented | [docs/naering/cts400.md](docs/naering/cts400.md) |
| CTS602 | **~2008–present** (Modbus PDF created 12/09/2008; still used on Compact P2 and commercial Comfort / VPM / VPR in 2025 guides) | Stable | [docs/cts602](docs/cts602/README.md) |
| CTS700 | **~2015–present** Compact P Ethernet eras (2015 map PDF, 2018 protocol PDF, Nordic LC drawings **2019**) | MVP | [docs/cts700](docs/cts700/README.md) |

Catalog: [docs/catalog](docs/catalog/bolig-matrix.md) · Commercial research: [docs/naering](docs/naering/README.md)

Shared: [Hardware](docs/hardware.md) · [Installation](docs/installation.md) · [Dashboards](docs/dashboards.md) · [FAQ](docs/faq.md)

## CTS602 models

All rows are **CTS602 HMI type ids** on the CTS602 board path (~**2008–present**). Nilan does not publish a clean per-SKU “introduced in year X” table for these names; use the plate / HMI type, not the calendar year, to pick the model. Compact P2 and current Comfort / VP / Combi lines still land here unless a dump proves CTS700 Ethernet.

| Model | Type id | Era (controller) | Guide |
|---|---|---|---|
| Comfort light | 2 | CTS602 ~2008–present | [comfort-light](docs/cts602/comfort-light.md) |
| Comfort Polar | 3 | CTS602 ~2008–present | [comfort-polar](docs/cts602/comfort-polar.md) |
| VPL 15c | 4 | CTS602 ~2008–present | [vpl-15c](docs/cts602/vpl-15c.md) |
| CompactS | 10 | CTS602 ~2008–present | [compacts](docs/cts602/compacts.md) |
| VP 18comp | 11 | CTS602 ~2008–present | [vp-18comp](docs/cts602/vp-18comp.md) |
| VP18cCom | 12 | CTS602 ~2008–present | [vp18ccom](docs/cts602/vp18ccom.md) |
| COMFORT | 13 | CTS602 ~2008–present | [comfort](docs/cts602/comfort.md) |
| VP 18c | 19 | CTS602 ~2008–present | [vp-18c](docs/cts602/vp-18c.md) |
| VP 18ek | 20 | CTS602 ~2008–present | [vp-18ek](docs/cts602/vp-18ek.md) |
| VP 18cek | 21 | CTS602 ~2008–present | [vp-18cek](docs/cts602/vp-18cek.md) |
| VPL 25c | 25 | CTS602 ~2008–present | [vpl-25c](docs/cts602/vpl-25c.md) |
| VPM/28EC | 26 | CTS602 ~2008–present | [vpm-28ec](docs/cts602/vpm-28ec.md) |
| VP18cCoB | 28 | CTS602 ~2008–present | [vp18ccob](docs/cts602/vp18ccob.md) |
| COMPACTn | 30 | CTS602 ~2008–present | [compactn](docs/cts602/compactn.md) |
| COMFORTn | 31 | CTS602 ~2008–present | [comfortn](docs/cts602/comfortn.md) |
| VP18 M2 | 32 | CTS602 ~2008–present (M2 line) | [vp18-m2](docs/cts602/vp18-m2.md) |
| COMBI 300 N | 33 | CTS602 ~2008–present | [combi-300-n](docs/cts602/combi-300-n.md) |
| COMBI 302 | 35 | CTS602 ~2008–present | [combi-302](docs/cts602/combi-302.md) |
| COMBI 302 T | 36 | CTS602 ~2008–present | [combi-302-t](docs/cts602/combi-302-t.md) |
| VGU180 ek | 38 | CTS602 ~2008–present | [vgu180-ek](docs/cts602/vgu180-ek.md) |
| VENTEC | 42 | CTS602 ~2008–present | [ventec](docs/cts602/ventec.md) |
| CompactP (AIR/GEO) | 44 | CTS602 Compact P / **P2** (current manuals) | [compactp](docs/cts602/compactp.md) · [compact-p2](docs/cts602/compact-p2.md) |

## CTS700 models

| Model / map | Map / hardware years | Guide |
|---|---|---|
| CTS700 2015 legacy map | Register PDF **20150826** (~**2015** era; addresses mostly under 10000; fan **4747** percent) | [legacy-2015](docs/cts700/legacy-2015.md) |
| Compact P Køl Polar/Nordic/Arctic XL (hybrid) | CTS700 LC drawings **2019** (produktliste 07/01/2019, rev 06/03/2019); fan **4747** steps **101–104** | [compact-p-nordic-xl](docs/cts700/compact-p-nordic-xl.md) · [hardware](docs/cts700/hardware/) |
| Compact P (2018+ Ethernet map) | Protocol PDF **2018_04** (~**2018–present** Compact P Ethernet; fan **21771**, setpoint **20102**) | [compact-p](docs/cts700/compact-p.md) |
| GEO / slave 4 | Same CTS700 eras when fitted; dump-gated | [geo](docs/cts700/geo.md) |

MVP covers room climate, fan, temps, humidity, and DHW setpoint. Not full CTS700 family support yet. On 2018+ Compact P, do not use register **20260** as room current; keep fan on **21771** (never Nordic **4747** steps). Tracking: [veista/nilan#19](https://github.com/veista/nilan/issues/19).

Full SKU coverage: [docs/catalog/bolig-matrix.md](docs/catalog/bolig-matrix.md) · [docs/catalog/naering-matrix.md](docs/catalog/naering-matrix.md).

## Contributors

GitHub’s About sidebar on this fork may show “No contributors” even though commit authors are present (API / Insights still list them). Avatars below come from the public contributors API via [contrib.rocks](https://contrib.rocks).

[![Contributors](https://contrib.rocks/image?repo=master3395/veista-nilan)](https://github.com/master3395/veista-nilan/graphs/contributors)

Named credits (including feedback that is not in git history): [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Support

If you like the integration, please leave a star and consider donating or becoming a sponsor.
