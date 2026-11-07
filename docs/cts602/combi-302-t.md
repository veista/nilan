# COMBI 302 T (CTS602)

| Item | Value |
|---|---|
| Controller | CTS602 |
| HMI type name | COMBI 302 T |
| Control type id | 36 |
| Typical unit id | 30 |
| Config board choice | CTS602 |

## Hardware

Use a Modbus RTU↔TCP bridge or USB-RS485. See [hardware](../hardware.md).

## Setup in Home Assistant

1. Install the integration ([installation](../installation.md)).
2. Add **Nilan** → **TCP** or **Serial**.
3. Select board **CTS602**.
4. Set unit id (default **30** unless your unit differs).
5. Confirm the device model in HA matches **COMBI 302 T** (type id 36).

## Expected behaviour

- Climate, sensors, and related platforms load based on bus version and hardware options.
- Unsupported optional sensors (for example CO2 without a module) can be hidden in the UI.

## Notes

Often used with domestic hot water tank features when fitted. Water heater entities appear when the unit exposes the required registers for your bus version.

## Troubleshooting

- Unsupported device during install: enable debug logging and attach HMI type / plate photos ([CONTRIBUTING.md](../../CONTRIBUTING.md)).
- Wrong unit id: try the id shown in your Modbus / HMI documentation.
- See [CTS602 overview](README.md) and [FAQ](../faq.md).
