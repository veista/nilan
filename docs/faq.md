# FAQ

## CTS602 vs CTS700?

Different controller boards, register maps, and typical unit ids.

- CTS602: often unit id **30**, RTU bridge or serial common
- CTS700 Compact P: often unit id **1**, native Ethernet Modbus TCP on port **502**

## Can YAML Modbus and this integration run together?

**Not on the same unit.** Compact P / CTS700 often allow only one overlapping Modbus session. If both poll, you can see Control State flicker (Ventilation ↔ Unknown) or failed setpoint writes. Pause or remove the YAML Modbus file for that host before enabling Nilan (or the reverse).

When the YAML hub is disabled, YAML coils/switches (for example `switch.bypass_damper`) stay **unavailable**. Use Nordic integration entities instead. Bypass is **status-only** over Ethernet (binary + percent sensors from 1.3.18+). DHW dial is not tank temperature. Details: [cts700/ethernet-limits.md](cts700/ethernet-limits.md).

Also: do **not** name a YAML Modbus hub bare `nilan`. That name matches this integration’s domain and can blank config-flow menu labels. Use something like `nilan_compactpc` or `nilan_cts700` instead. The integration’s internal hub is always prefixed (`nilan_hub_…`) so it does not fight your YAML hub name.

## Why were Select Controller Board labels blank?

Usually a YAML Modbus hub named `nilan`. Rename the hub and reload Modbus / restart HA, then open Add hub again. Upstream CTS602-only flows did not show the new board/confirm menus, so the clash was less visible there.

From **1.3.17** the board / TCP / confirm menus always pass explicit labels (not translation-only), so the five board choices stay readable even if that hub-name clash is still present. You should still rename a YAML hub named `nilan` so coexistence warnings and other strings load correctly.

## Compact P GEO / NCS-700: which board option?

Prefer **Auto-detect**. If you choose manually: Nordic / Polar / Arctic XL uses fan holding **4747** steps **101–104**; 2018+ Compact P uses fan **21771** as percent. GEO extras may still be dump-gated: [cts700/geo.md](cts700/geo.md).

## Does an offline Nilan block Home Assistant startup?

Older builds waited forever for Modbus `event_connected` during setup, so HA looked stuck if the unit was unreachable. From **1.3.11** connect wait is capped (~15s), then the entry raises `ConfigEntryNotReady` and HA continues; Nilan retries in the background when the network/unit is back.

## Can I run two Nilan units in one Home Assistant?

Yes from **1.3.11**. Entity `unique_id` values are scoped per config entry (hub name), so sensors like `hvac` / `control_state` no longer collide across units. Give each unit a clear device name in the config flow. Do not point two integrations (or YAML Modbus + this integration) at the same Modbus TCP session.

## Why does Firmware show outdoor temperature?

Older fork builds put a probe reading into the device software string. From **1.3.10** the Firmware field is a map label only (for example `CTS700 2015 map`). Outdoor temperature stays on the normal T1 / outdoor sensor.

## Can the integration auto-detect my board?

Yes. After TCP or Serial, choose **Auto-detect**. Probe order: CTS602 `control_type` (1000), then CTS700 Nordic (holding **4747** in **101–104**), then CTS700 2018+ outdoor temp (20282), then CTS700 2015 T1+setpoint (5152 / 4746). Unit id **1** then **30** if you leave unit id empty. Confirm the result before the entry is created. You can still pick CTS602, CTS700 Nordic XL, CTS700 2018+, or CTS700 2015 manually.

## Why can the CTS700 PDF disagree with live values?

Firmware eras differ:

- **2015 map** (PDF 20150826): registers mostly under 10000 (setpoint 4746, fan **4747 percent**, …). Use board **CTS700 (2015 legacy map)**. Guide: [cts700/legacy-2015.md](cts700/legacy-2015.md).
- **Nordic XL hybrid**: fan **4747 = 101–104**, mixed classic + 20xxx. Use **CTS700 Compact P Nordic XL**. Guide: [cts700/compact-p-nordic-xl.md](cts700/compact-p-nordic-xl.md).
- **2018+ / Compact P map**: 20xxx registers (fan **21771** percent, setpoint **20102**). Use board **CTS700 (2018+ / Compact P)**. Guide: [cts700/compact-p.md](cts700/compact-p.md).

Compact P live installs may also disagree with some PDF labels. Prefer live-verified tables in those guides. Era matrix: [cts700/README.md](cts700/README.md).

## Compact P XL Nordic: CTS602 or CTS700?

Catalog pages often say CTS602. If HMI type is **44** / unit id **30**, choose **CTS602**. If Modbus shows Nordic step fan on **4747**, choose **CTS700 Compact P Nordic XL**. Hub: [catalog/compact-p-xl-nordic.md](catalog/compact-p-xl-nordic.md).

## Unsupported device on CTS602?

Confirm the HMI type string / type id against [cts602/README.md](cts602/README.md). Attach debug logs and plate photos as described in [CONTRIBUTING.md](../CONTRIBUTING.md). Type **32** (VP18 M2) is included on this fork; see [vp18-m2.md](cts602/vp18-m2.md).

## CO2 always 0?

No CO2 module installed, or the entity is not applicable. Hide the entity in the UI. On older Modbus versions the integration now probes CO2 presence instead of requiring bus version 10 or higher.

## Norwegian language (bokmål) missing strings?

Use Home Assistant language **Norsk bokmål** (`nb`). This fork ships `translations/nb.json` (renamed from `no.json`).

## Danish language missing setup strings?

Use Home Assistant language **Dansk** (`da`). From **1.3.17** this fork ships `translations/da.json` for config-flow menus (entity names fall back to English when not translated).

## Slave 4 / floor / GEO missing on Compact P?

Often unavailable on Air-only Compact P installs. Documented as dump-gated: [cts700/geo.md](cts700/geo.md).

## Compact P2: CTS602 or CTS700?

Current Nilan Compact P2 manuals list **CTS602**. Use board **CTS602** (unit id 30). See [cts602/compact-p2.md](cts602/compact-p2.md). Only use CTS700 if a dump shows 20xxx Ethernet registers.

## Commercial Comfort 600 / VPM / VR / VPR?

Product pages and gateway docs point to **CTS602** Modbus RS485 (default unit id 30). Choose **CTS602** or Auto-detect. If the HMI type id is unknown to the integration, share a dump. Full list: [catalog/naering-matrix.md](catalog/naering-matrix.md). Do not pick CTS700 Compact P maps for commercial units unless proven.

## Where are the dashboards?

Optional Nilan-only Lovelace YAML lives under [`dashboards/`](../dashboards/). See [dashboards.md](dashboards.md). They are not auto-installed by Marketplace / HACS.
