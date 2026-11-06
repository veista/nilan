# Installation

## Supported Home Assistant stack (this fork)

Validated on **Home Assistant OS** with:

| Component | Version |
|---|---|
| Installation | Home Assistant OS |
| Core | 2026.11.0 |
| Supervisor | 2026.11.0 |
| Operating System | 18.5.rc1 |
| Frontend | 20261028.4 |

`hacs.json` `homeassistant` minimum stays lower so older Core installs can still install the package. Prefer Core **2025.9.1+**; use the table above as the current CTS700 Nordic dual-path reference.

### Marketplace vs HACS (UI name)

Home Assistant **2026.11+** shows the former HACS store UI as **Marketplace** (sidebar / deep links under `/marketplace/...`). The package metadata still lives in [`hacs.json`](../hacs.json); older Core builds still label the same flow **HACS**. Steps below use **Marketplace** first, with HACS notes for pre-2026.11.

CTS700 Compact P Nordic: pause overlapping YAML Modbus for the same unit, then use the Nilan hub. Bypass is status-only over Ethernet; see [cts700/ethernet-limits.md](cts700/ethernet-limits.md).

## Marketplace / HACS (upstream / default store)

1. Open **Marketplace** (HA 2026.11+) or **HACS** (older Core).
2. Install **Nilan** from the default store (upstream release).
3. Restart Home Assistant.
4. Settings → Devices & services → Add integration → **Nilan**.
5. Choose **TCP** or **Serial**.
6. Choose **Auto-detect**, or board type **CTS602** / **CTS700 (2018+)** / **CTS700 Compact P Nordic XL** / **CTS700 (2015 legacy)** manually.
7. Enter host, port, and unit id (see device docs). For auto-detect you may leave unit id empty (tries **1** then **30**).

## Important: do not fight for the bus

- Pause YAML Modbus for the same unit before adding Nilan (one Modbus client at a time on many Compact P boards).
- Do not name a YAML Modbus hub `nilan` (use `nilan_compactpc` or similar). That name blanks some setup menu labels.
- You can keep YAML for a *different* unit with a different hub name while Nilan manages another.

## Marketplace / HACS (this fork, custom repository)

Use while testing CTS700 MVP and fork fixes before upstream merge.

**HA 2026.11+ (Marketplace):**

1. Marketplace → three-dot menu → **Custom repositories** (or open the repo page at `/marketplace/repository/1323343841` on your HA host)
2. Repository: `https://github.com/master3395/veista-nilan` (custom repository id **1323343841**)
3. Category: **Integration**
4. Find **Nilan** → Download → restart Home Assistant
5. Add the integration as above
6. If an older veista/nilan install exists, remove its config entry first (same `nilan` domain)

**Pre-2026.11 (HACS):**

1. HACS → three-dot menu → **Custom repositories**
2. Repository: `https://github.com/master3395/veista-nilan`
3. Category: **Integration**
4. Find **Nilan** → Download → restart Home Assistant
5. Add the integration as above
6. If an older veista/nilan install exists, remove its config entry first (same `nilan` domain)

Example deep link shape (replace host with your HA): `http://192.168.1.50/marketplace/repository/1323343841`

## Manual

1. Copy `custom_components/nilan` into your Home Assistant `custom_components` folder.
2. Restart Home Assistant.
3. Add the integration as above.

## Defaults

| Board | Port | Unit id |
|---|---|---|
| CTS602 | 502 (TCP) | 30 |
| CTS700 Compact P | 502 | 1 |

## Dashboards

Optional Nilan-only Lovelace examples: [dashboards.md](dashboards.md).

See [hardware.md](hardware.md) and the guide for your model under [README.md](../README.md).
