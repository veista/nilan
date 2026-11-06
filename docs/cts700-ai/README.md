# CTS700 AI packages (optional)

Reusable Home Assistant **packages** for a Nilan **CTS700 Compact P Nordic** example site. They add preference helpers and a rule-based 24/7 autotune loop. They are **not** part of the Python integration and are **not** installed by HACS.

Example Modbus host in this folder: `192.168.1.50` (port 502, unit id 1). Replace entity ids if your device name is not `Nilan CTS700 Nordic`.

## What you get

| Piece | Entity / file |
|---|---|
| Memory package | [`packages/cts700_ai.yaml`](packages/cts700_ai.yaml) |
| Autotune package | [`packages/cts700_ai_autotune.yaml`](packages/cts700_ai_autotune.yaml) |
| Master switch | `input_boolean.cts700_ai_enabled` (CTS700 AI 24/7) |
| Write gate | `input_boolean.cts700_ai_allow_writes` (CTS700 AI auto-skriv) |
| Last action | `input_text.cts700_ai_last_action` |
| Last advice | `input_text.cts700_ai_last_advice` |
| Autotune script | `script.cts700_ai_autotune_once` |
| Periodic sense | every 20 minutes (`automation.cts700_ai_autotune_periodic`) |
| Assist prompt | [`system-prompt.md`](system-prompt.md) |
| Runtime context (date / HA version) | [`packages/cts700_ai_context.yaml`](packages/cts700_ai_context.yaml) |
| Lovelace card | [`lovelace-card.yaml`](lovelace-card.yaml) |
| Settings view | [`lovelace-settings-view.yaml`](lovelace-settings-view.yaml) |

## Install

1. Enable packages in `/config/configuration.yaml`:

   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```

2. Copy the YAML files into `/config/packages/` on Home Assistant (`cts700_ai.yaml`, `cts700_ai_autotune.yaml`, and optionally `cts700_ai_context.yaml` for date/HA version injection).
3. Check configuration, then reload helpers, scripts, automations, and template entities (or restart once for new helpers).
4. Confirm states for `input_boolean.cts700_ai_enabled`, `input_boolean.cts700_ai_allow_writes`, `input_text.cts700_ai_last_action`, `input_text.cts700_ai_last_advice`. With context package: `sensor.cts700_ai_runtime_context` and run `script.cts700_ai_refresh_runtime_context` once.
5. Paste [`lovelace-card.yaml`](lovelace-card.yaml) onto a Nilan dashboard. Optional: add [`lovelace-settings-view.yaml`](lovelace-settings-view.yaml) as a view. Example dashboard path: `/nilan-compact-p/`.
6. Optional Assist: paste [`system-prompt.md`](system-prompt.md) into a conversation agent. Prefer Assist tools on when you need live temps/date from entities. Local OpenAI-compatible example: `http://192.168.1.50:1235/v1`. Put tokens only in `/config/secrets.yaml` ([`secrets.example.yaml`](secrets.example.yaml)). Never commit real keys.
7. Do **not** fine-tune the local model for calendar date or HA version. Inject via runtime context + system prompt + (when enabled) Assist entity tools. RAG-lite notes can live under `/config/cts700-docs/`.

## Behaviour (keep this)

- **Off** (`CTS700 AI 24/7` = av): no autotune actions, no CTS writes.
- **On** + auto-skriv **av**: updates `last_advice` / `last_action` only.
- **On** + auto-skriv **på**: may change allowlisted CTS settings toward preference helpers, unless write-hold is active.

Allowlist:

- Room setpoint: `climate.set_temperature` on `climate.nilan_cts700_nordic_hvac` (register **4746** via the integration).
- Fan percent: `input_number.nilan_fan_percent` (your existing write-to-CTS automation). Skip fan writes while `input_boolean.nilan_auto_mode` is on.

Never auto-write DHW over Ethernet dial, cameras, locks, installer auth, or invented Modbus registers.

Compact P **2018** electrical supplement heater (`switch.nilan_electrical_supplement_heater`, holding **20464**) is **not** on this Nordic board path. Do not auto-write 20464 from these packages.

Thermal lag defaults: **3 h** sense-ahead, **2.5 h** write hold, example flat **60 m2**, preferred room **22 to 23 C** (mål 22.5).

## Requirements

- Nilan integration on this fork (`master`, CTS700 Compact P Nordic XL board).
- Optional helpers used by autotune: `input_number.nilan_fan_percent`, `input_boolean.nilan_auto_mode`, `input_boolean.nilan_cts_write_busy` (omit or stub if you do not have the last one).
- One Modbus client to the unit. Example docs host: `192.168.1.50:502`.
- Home Assistant OS reference stack for these packages: Core **2026.11.0**, Supervisor **2026.11.0**, OS **18.5.rc1**, Frontend **20261028.4**.

If `nilan_cts_write_busy` sticks **on** after an interrupted self-test, autotune exits immediately. Clear the helper, or rely on the 10-minute watchdog automation in `cts700_ai_autotune.yaml`.

## Privacy

Do not put street names, personal dashboard slugs, or live LAN addresses in git. This folder uses generic Compact P / CTS700 names only.
