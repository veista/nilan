# CTS700

Support for Nilan **CTS700** controllers over Modbus (Ethernet TCP or Serial).

## Era matrix (how boards coexist)

All eras share Home Assistant platforms (`climate`, `sensor`, …) and the same config flow, but **each board owns its fan and setpoint writers**. Only one `board_type` is stored per config entry.

| Era | Doc / hardware years | Board choice in HA | Fan write | Room setpoint | Room current | Guide |
|---|---|---|---|---|---|---|
| **2015** legacy | PDF **20150826** | CTS700 (2015 legacy map) | **4747** percent 0–100 | **4746** | classic T3 / master | [legacy-2015.md](legacy-2015.md) |
| **Nordic** hybrid | LC drawings **2019** | CTS700 Compact P Nordic XL | **4747** steps **101–104** | **4746** | input **5154** | [compact-p-nordic-xl.md](compact-p-nordic-xl.md) |
| **2018+** Compact P | Protocol PDF **2018_04** | CTS700 (2018+ / Compact P) | **21771** percent | **20102** | **20286** | [compact-p.md](compact-p.md) |

Catalog Compact P XL Nordic may also be **CTS602** type 44: [../catalog/compact-p-xl-nordic.md](../catalog/compact-p-xl-nordic.md).

**Auto-detect probe order:** CTS602 → CTS700 Nordic (4747∈101..104) → CTS700 2018+ (20282) → CTS700 2015 (5152+4746).

**Regression rule:** 2018+ units must keep fan **21771** and setpoint **20102**. Nordic units must keep **4747** steps. Never merge Nordic step encoding into the 2018+ device class.

## Week programs

This integration does **not** sync week/year programs. HA climate writes can fight a week program still active on the controller. Pause conflicting slots while testing fan or setpoint from Home Assistant.

## Connection defaults

- Indoor unit id: typically **1**
- TCP port: **502**
- Native LAN: Cat5e (or better) from CTS700 LAN to router; no RS485 bridge required for Ethernet

## Status

- **2018+ Compact P:** live-checked (04/08/2026). See [compact-p.md](compact-p.md).
- **Nordic XL hybrid:** community parity (mark007 map). See [compact-p-nordic-xl.md](compact-p-nordic-xl.md).
- **2015 legacy:** MVP from the 20150826 PDF; percent fan on 4747 (not 101–104).

Current integration version: **1.3.18**.

Ethernet / dual-path limits (bypass status-only, DHW dial vs tank, YAML coils): [ethernet-limits.md](ethernet-limits.md). Validated on HA Core **2026.11.0** / OS **18.5.rc1**.

Hardware drawings for Compact P Køl Polar/Nordic/Arctic XL: [hardware/](hardware/).

Official Nilan PDF manuals are not stored in this repo. Download links: [../manuals.md](../manuals.md).

Optional Home Assistant 24/7 helpers (packages, not HACS): [../cts700-ai/README.md](../cts700-ai/README.md).

## Modbus YAML reference

Per-board Home Assistant Modbus YAML (not universal): [`modbus_yaml/`](../../modbus_yaml/). Prefer the Nilan integration in production. Never run YAML and the integration on the same unit.

## Still out of scope

- Full GEO / floor slave 4 feature set ([geo.md](geo.md))
- Full feature parity with CTS602 (alarms, week programs, all selects)
- Installer auth at register 7777
- CTS400

Help wanted: register dumps and entity pass/fail reports. See [CONTRIBUTING.md](../../CONTRIBUTING.md) and issue [#19](https://github.com/veista/nilan/issues/19).
