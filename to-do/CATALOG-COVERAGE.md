# Catalog coverage tracking

**Goal:** Cover every SKU on [nilan.no/produkter](https://www.nilan.no/produkter) via controller maps and capability profiles (not one device class per name).

**Fork:** https://github.com/master3395/veista-nilan  
**Version target for matrices:** 1.3.4

## Docs

| File | Purpose |
|---|---|
| [docs/catalog/bolig-matrix.md](../docs/catalog/bolig-matrix.md) | All bolig SKUs |
| [docs/catalog/naering-matrix.md](../docs/catalog/naering-matrix.md) | All næring SKUs |
| [docs/catalog/aliases.md](../docs/catalog/aliases.md) | Marketing → HMI |
| [docs/naering/README.md](../docs/naering/README.md) | Commercial research |
| [docs/naering/cts400.md](../docs/naering/cts400.md) | CTS400 dump-gated |
| [docs/cts700/geo.md](../docs/cts700/geo.md) | GEO / slave 4 |
| [docs/cts602/compact-p2.md](../docs/cts602/compact-p2.md) | Compact P2 on CTS602 |

## Code

| Item | Path |
|---|---|
| Capability profiles | `custom_components/nilan/capabilities.py` |
| CTS602 types | `custom_components/nilan/device_map.py` |
| Probe / auto-detect | `custom_components/nilan/modbus_probe.py` |

## Phase checklist

- [x] Phase A: full matrices
- [x] Capability module wired
- [x] CTS602 marketing aliases (docs + Python)
- [x] Compact P2 CTS602 guide
- [x] GEO dump-gated docs + dashboard stub notes
- [x] Næring research notes (CTS602 commercial; CTS400 gated)
- [x] Commercial path: use CTS602 when type known; no fake CTS400 map
- [x] Dump templates / CONTRIBUTING checklist
- [ ] Broader type ids after community dumps (ongoing)

## Release notes draft (1.3.4)

- Full bolig + næring catalog matrices
- Capability profiles for entity filtering
- Compact P2 documented on CTS602
- GEO / CTS400 explicitly dump-gated
- Dump checklist for bolig and næring
