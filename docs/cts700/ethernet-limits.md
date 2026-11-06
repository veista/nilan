# Compact P / CTS700 Ethernet limits

Hardware and firmware limits when talking to Compact P (Nordic XL / hybrid) over **Modbus TCP**. These are not fixed by raising the integration version alone.

Validated against Home Assistant OS installs including **Core 2026.11.0**, **Supervisor 2026.11.0**, **OS 18.5.rc1**, and **Frontend 20261028.4**.

## Prefer the Nilan integration (Nordic dual-path)

When the Nilan custom component hub is active for a unit, **pause or disable** the overlapping YAML Modbus hub for that same host. Compact P Ethernet often allows only one overlapping Modbus client.

| Source | Use for |
|---|---|
| Nilan integration (CTS700 Compact P Nordic XL) | Room climate, fan steps, temps, humidity, filters, DHW water heaters, bypass **status** |
| YAML Modbus (`modbus_yaml/cts700_nordic_xl.yaml`) | Bring-up / dump tooling only, or a *different* unit with another hub name |

YAML Modbus **coils / switches** (bypass write, DHW pause, supplement coils, filter reset, slave-4 cooling) stay **unavailable** while that YAML hub is disabled. That is expected. Remap Lovelace and templates to Nordic entities instead of `switch.bypass_damper` and similar YAML ids.

Do **not** name a YAML hub bare `nilan` (use `nilan_cts700_nordic` or similar). See [faq.md](../faq.md).

## Status-only / unreliable over Ethernet

| Control | Ethernet behaviour | Integration behaviour |
|---|---|---|
| Bypass damper (holding **21773**, discrete **4704** / **4705**) | Writes often do not stick | **Read-only** binary + percent sensors from Nordic map. No writable switch. |
| Main compressor effort (holding **4706**) | Read-only status | Nordic sensor + derived heat-pump binary (effort > 0). Not a write target. |
| DHW “dial” (**5548** / sometimes **20460**) | Often capped near ~25.5 C | Setpoint entity is not tank temperature. Use water heater **current** (T11/T12, inputs **5162** / **5163**) for tank. |
| DHW min/max (**2828** / **3935**) | May return Modbus exception when stuck | Fix on CTS panel; do not hammer restores from HA |
| Installer auth (**7777**) | Auth over Ethernet often fails | Panel only |
| Electrical supplement (**20464**) | Compact P **2018** map | Nordic hybrid path does **not** write 20464 |
| Slave 4 (floor / air / central heat) | Often absent on Air Compact P | Leave disabled / dump-gated |

## Room and fan (reliable)

| Register | Notes |
|---|---|
| Room setpoint **4746** | Primary comfort write (about 5-40 C) |
| Fan step **4747** | Nordic values **101-104** = steps 1-4 |
| Op mode **5432** | Status of cool/heat/dehum/DHW; climate Auto/Off only |

## AI / write-busy

Optional AI packages under [cts700-ai](../cts700-ai/README.md) may gate on `input_boolean.nilan_cts_write_busy`. If a self-test is interrupted, that helper can stick **on** and block autotune. Clear it, or use the optional watchdog in `cts700_ai_autotune.yaml` (auto-off after 10 minutes).

## Privacy

Do not commit street names, personal dashboard slugs, or live LAN addresses into this repository. Docs use generic examples (`192.168.1.50`, `/nilan-compact-p/`).
