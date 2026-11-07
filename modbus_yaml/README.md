# Per-board Modbus YAML (2015 and up)

Reference / fallback Home Assistant **Modbus** YAML aligned with this fork’s Python maps. **Not** one file for every board: fan encodings differ.

## Pick one file

| File | Board | Use when |
|---|---|---|
| [`cts700_2015_legacy.yaml`](cts700_2015_legacy.yaml) | `CTS700_LEGACY` | Fan **4747** percent; classic under-10000 map |
| [`cts700_nordic_xl.yaml`](cts700_nordic_xl.yaml) | `CTS700_NORDIC` | Compact P Køl Polar/Nordic/Arctic (XL); fan **4747** = **101–104** |
| [`cts700_2018_compact_p.yaml`](cts700_2018_compact_p.yaml) | `CTS700` | Fan **21771**; setpoint **20102**; room **20286** |
| [`cts602_compactp.yaml`](cts602_compactp.yaml) | `CTS602` CompactP (44) | Catalog Compact P XL Nordic / type 44 RS485 (unit 30) |

## Rules

1. Replace `YOUR_HOST_IP` (and unit id if needed) before use.
2. Load **only one** of these files for a given unit.
3. Do **not** poll the same register from YAML Modbus and the **Nilan** integration on one unit. See **Dual-path guide** below.
4. Prefer the Nilan board menu / Auto-detect in production; YAML is for bring-up, custom CTS tooling, or comparison.
5. Keep YAML in sync with the matching Python register map and `register_probe.PROBE_SPECS` when you change entities.

## Dual-path guide (integration + YAML)

Use **one register truth** from a live probe (see `to-do/probe_registers.ps1` or integration setup probe):

| Path | Best for |
|------|----------|
| **Nilan integration** (v1.3.13+) | Standard entities, auto probe, `dead_registers` persistence |
| **YAML Modbus** | Custom automations, selftest scripts, registers not in the integration map |

**Migration split (recommended on an existing YAML site):**

1. Probe the unit once (PowerShell script in `to-do/` or add Nilan config entry).
2. Upgrade Nilan via Marketplace (HA 2026.11+) or HACS (older) to **1.3.13+**.
3. **Comment out** YAML Modbus sensors/climates that duplicate integration entities (room, filter, fan, temps, DHW).
4. Add Nilan config entry (TCP, board CTS700 Nordic or auto-detect). Probe stores `dead_registers`.
5. Keep YAML for CTS Log selftest, event-log dump (10000+), and other custom reads only.
6. Optional: `!include modbus_yaml/nilan_filter_templates.yaml` if you stay YAML-only for filters.

**Filter registers (Nordic / hybrid firmware):** prefer **1326-1329** (interval + remaining). Template days-since = interval minus remaining. Register **20103** may mirror remaining on some units but is absent on others (issue #3).

## Era docs

- [CTS700 era matrix](../docs/cts700/README.md)
- [Catalog Compact P XL Nordic hub](../docs/catalog/compact-p-xl-nordic.md)
