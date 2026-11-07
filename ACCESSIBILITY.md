# Accessibility

This project is a Home Assistant **custom integration** (backend + config flow strings). Most of the visual UI is Home Assistant core. We still treat documentation, translations, and entity naming as accessibility-relevant.

## Goals

- Keep README and docs readable: clear headings, descriptive links, plain language.
- Ship translations so users can run Home Assistant in their language (see `custom_components/nilan/translations/`).
- Use clear entity and config-flow names so screen readers announce accurate labels.
- Prefer text status over color-only meaning in shared Lovelace examples.

## Known limits

- Lovelace card layout and keyboard focus are largely controlled by Home Assistant.
- Not every Nilan register or language is translated yet.
- Shared dashboards under `dashboards/` are examples; entity ids may need adjusting after install.

## Reporting accessibility issues

Please open a GitHub issue with the **accessibility** label (or the accessibility issue template when available) and include:

- What you tried to do
- What happened instead
- OS, browser or HA companion app, and assistive technology (if any)
- Severity: Critical (blocked), High, Medium, or Low

Thank you for reports that help more people use the integration and docs.
