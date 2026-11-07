# CTS700 LC hardware (Compact P Køl Polar/Nordic/Arctic XL)

Community-supplied Nilan drawings for units that match **CTS700_NORDIC** (and related CTS700 Ethernet Compact P).

## Product identity

| Field | Value |
|---|---|
| Model | **Compact P Køl (Sol) Polar/Nordic/Arctic (XL)** |
| Controller | **CTS700 Styring** |
| Board | **CTS700 LC Board Version 4.0** (NCS-700 family; photos may show v4.1) |
| Styreprint | **#237501** |
| Varenr. | **75124xx** |
| Drawing | Rev 1.34, 06/03/2019 · produktliste 07/01/2019 |

Active cooling hardware is listed (compressor M6, bypass M7, 4-way valve Y2). Polar/Nordic/Arctic variants include preheat (E10 / K10) wiring notes.

## Schematics in this folder

| File | Content |
|---|---|
| [cts700-lc-v4-wiring-1.png](cts700-lc-v4-wiring-1.png) | LC board overview, Ethernet, RS485, relays |
| [cts700-lc-v4-wiring-2.png](cts700-lc-v4-wiring-2.png) | T1–T12 sensors, DHW, SmartGrid |
| [cts700-lc-v4-wiring-3.png](cts700-lc-v4-wiring-3.png) | XL fans, bypass, Polar/Nordic preheat |
| [produktliste-1.png](produktliste-1.png) | Parts: CTS700 LC, compressor, fans, RH |
| [produktliste-2.png](produktliste-2.png) | Parts: T1–T12 NTC list, valves Y2/Y8/Y9 |

## Physical T sensors (wiring)

| Probe | Role (Danish / English) |
|---|---|
| T1 | Udetemperatur / outdoor (not the same role as T8) |
| T2 | Tilluft før eftervarme / supply before after-heat |
| T3 | Fraluft / extract |
| T4 | Afgang veksler / after heat exchanger |
| T5 | Kondensator (diagnostic in HA) |
| T6 | Fordamper / evaporator (diagnostic in HA) |
| T7 | Tilluft efter eftervarme (optional; often unused) |
| T8 | Udetemperatur / outdoor (preheat path on Polar/Nordic; often matches T1 when preheater idle) |
| T9 | Vandflade / water surface |
| T10 | Ext. rumføler (accessory) |
| T11 / T12 | Brugsvand top / bund |

Modbus addresses for the hybrid map are in [../compact-p-nordic-xl.md](../compact-p-nordic-xl.md) and [`modbus_yaml/cts700_nordic_xl.yaml`](../../../modbus_yaml/cts700_nordic_xl.yaml).

## Which HA board?

1. Ethernet + fan **4747 = 101–104** → **CTS700 Compact P Nordic XL**
2. Ethernet + fan **21771** percent / setpoint **20102** → **CTS700 (2018+)**
3. CTS602 HMI type 44 / unit id 30 only → **CTS602**

Do not run YAML Modbus and the Nilan integration on the same unit.
