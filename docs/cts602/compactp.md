# CompactP (CTS602)

| Item | Value |
|---|---|
| Controller | CTS602 |
| HMI type name | CompactP |
| Control type id | 44 |
| Typical unit id | 30 |
| Config board choice | CTS602 |
| Variants | CompactP, CompactP AIR, CompactP GEO |

## Variants

CompactP, CompactP AIR, CompactP GEO (software probe). Marketing names such as Compact P Nordic / AIR / EK / XL and **Compact P2*** usually map here when the board is CTS602. Catalog Compact P XL Nordic: [../catalog/compact-p-xl-nordic.md](../catalog/compact-p-xl-nordic.md). See [compact-p2.md](compact-p2.md) and [../catalog/aliases.md](../catalog/aliases.md).

## Important

This guide is for Compact P units on a **CTS602** board (HMI type 44).

If your Compact P has a **CTS700** controller with Ethernet LAN and Modbus TCP on unit id 1:

- Fan **21771** percent / setpoint **20102**: [../cts700/compact-p.md](../cts700/compact-p.md)
- Fan **4747** steps **101–104**: [../cts700/compact-p-nordic-xl.md](../cts700/compact-p-nordic-xl.md)

Reference YAML for type 44: [`modbus_yaml/cts602_compactp.yaml`](../../modbus_yaml/cts602_compactp.yaml).

## Hardware

Use a Modbus RTU↔TCP bridge or USB-RS485 unless you have another supported interface. See [hardware](../hardware.md).

## Setup in Home Assistant

1. Install the integration ([installation](../installation.md)).
2. Add **Nilan** → **TCP** or **Serial**.
3. Select board **CTS602**.
4. Set unit id (default **30** unless your unit differs).
5. Confirm model shows as CompactP, CompactP AIR, or CompactP GEO.

## AIR / GEO

The integration probes CompactP software to distinguish AIR vs GEO where possible. GEO / heat-pump secondary maps use the HPS-oriented entity paths when available.

## Troubleshooting

- Unsupported device: debug log + plate / HMI type photos ([CONTRIBUTING.md](../../CONTRIBUTING.md)).
- See [CTS602 overview](README.md) and [FAQ](../faq.md).
