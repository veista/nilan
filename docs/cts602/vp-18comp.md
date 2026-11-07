# VP 18comp (CTS602)

| Item | Value |
|---|---|
| Controller | CTS602 |
| HMI type name | VP 18comp |
| Control type id | 11 |
| Typical unit id | 30 |
| Config board choice | CTS602 |

## Hardware

Use a Modbus RTU↔TCP bridge or USB-RS485. See [hardware](../hardware.md).

## Setup in Home Assistant

1. Install the integration ([installation](../installation.md)).
2. Add **Nilan** → **TCP** or **Serial**.
3. Select board **CTS602**.
4. Set unit id (default **30** unless your unit differs).
5. Confirm the device model in HA matches **VP 18comp** (type id 11).

## Expected behaviour

- Climate, sensors, and related platforms load based on bus version and hardware options.
- From **1.3.12** (upstream [veista/nilan#234](https://github.com/veista/nilan/pull/234)): electric and compressor **water heater** entities appear (type **11** was missing from compressor DHW setpoint, which blocked both). Bypass flap and other verified sensors are enabled; disable optional ones you do not have fitted.
- Unsupported optional sensors (for example CO2 without a module) can be hidden in the UI.


## Troubleshooting

- Unsupported device during install: enable debug logging and attach HMI type / plate photos ([CONTRIBUTING.md](../../CONTRIBUTING.md)).
- Wrong unit id: try the id shown in your Modbus / HMI documentation.
- See [CTS602 overview](README.md) and [FAQ](../faq.md).
