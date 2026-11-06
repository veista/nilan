# Lovelace dashboards (Nilan only)

These examples live in [`dashboards/`](../dashboards/) and contain **only Nilan** cards and entities. They are not installed automatically by Marketplace / HACS.

## Before you import

1. Install and configure the Nilan integration.
2. Confirm entities exist under Settings → Devices → Nilan.
3. Entity ids follow the **device name**. Nordic example dashboard assumes `Nilan CTS700 Nordic` (`nilan_cts700_nordic_…`). Search-replace that prefix if yours differs. Do not point cards at disabled YAML Modbus switches (bypass write, etc.).

## Import (UI)

1. Settings → Dashboards → **Add dashboard**.
2. Open the new dashboard → three-dot menu → **Raw configuration editor**.
3. Paste the contents of:
   - [`dashboards/cts700_compact_p.yaml`](../dashboards/cts700_compact_p.yaml) for CTS700 Compact P 2018+,
   - [`dashboards/cts700_compact_p_nordic_xl.yaml`](../dashboards/cts700_compact_p_nordic_xl.yaml) for Nordic XL, or
   - [`dashboards/cts602_overview.yaml`](../dashboards/cts602_overview.yaml) for CTS602
4. Save. Fix any unknown entities (hide or remove cards your unit does not expose).

## Import (YAML mode)

Advanced users can include the view YAML under a Lovelace dashboard configuration. Prefer the UI raw editor if you use storage mode dashboards.

Optional 24/7 comfort helpers (not required for the integration): [CTS700 AI](cts700-ai/README.md). Lovelace snippets there use generic dashboard paths such as `/nilan-compact-p/`.

## Scope rules

- Nilan ventilation, DHW, filters, setpoints, and related integration entities only
- No energy tariffs, cameras, weather, or other house dashboards
- Stock Home Assistant cards only (no required custom Marketplace / HACS cards)
