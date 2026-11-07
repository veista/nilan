# CTS700 2015 legacy map

MVP support for older CTS700 firmware that uses the Modbus layout from Nilan’s **20150826** register PDF (addresses mostly **under 10000**).

## When to use this

Choose **CTS700 (2015 legacy map)** in the config flow (or let auto-detect fall through after CTS602, Nordic, and the 2018+ map fail).

Use this if:

- Your CTS700 rejects or returns nonsense on 20xxx registers (2018+ Compact P map)
- Live values match addresses like setpoint **4746**, fan **4747 percent 0–100**, T1 **5152**, humidity **4716**, DHW **5548**
- Holding **4747** is **not** in **101–104** (those values mean Nordic step encoding; use [compact-p-nordic-xl.md](compact-p-nordic-xl.md))

Do **not** use this for modern Compact P Ethernet units that match the [2018 PDF](https://www.en.nilan.dk/Files/Files/Engelsk/Downloads/7.%20Modbus%20-%20BACnet/2018_04_Modbus_CTS700_Modbus_protokol.pdf) / [compact-p.md](compact-p.md) (20xxx registers). Your 2018 Compact P should stay on **CTS700 (2018+)**.

## Typical connection

| Setting | Value |
|---|---|
| Protocol | Modbus TCP (or Serial if applicable) |
| Port | **502** (TCP) |
| Unit id | often **1** (confirm on device) |

## Live registers used (MVP)

| Function | Register | Notes |
|---|---|---|
| Room / user setpoint | 4746 | Scale 0.1 |
| Fan speed | 4747 | Percent 0-100, mapped to climate 0-4 (never write 101-104 here) |
| Humidity | 4716 | 0-100, no 0.1 scale |
| Master sensor | 5088 | Preferred room current when present |
| T1…T6 | 5152…5157 | Common Compact P labeling (outdoor…evaporator) |
| Pause | 4727 | 0 = running |
| Operation type | 2402 | PDF 0 auto / 1 cool / 2 heat (translated for HA climate) |
| DHW setpoint | 5548 | Scale 0.1 |
| Filter days | 1326 − 1328 | Threshold minus passed days (inlet) |
| Heater control | 4701 | Used as electric heater “running” hint |

Temperatures use scale **0.1** (245 → 24.5 C), same as the 2015 PDF limits.

## Caveats

- DHW **tank current** temperatures are not uniquely named in the 2015 PDF, so water heater current temp may be unavailable; setpoint still works
- Sensor roles for T1–T6 can differ by product; report dumps if labels are wrong on your unit
- Installer/admin registers that need authentication at **7777** are out of scope
- Week/year programs are not synced; HA writes can fight an active week program
- Full DI/DO maps are out of MVP scope

## Related

- [CTS700 era matrix](README.md)
- [Compact P Nordic XL](compact-p-nordic-xl.md)
- [Compact P 2018+ map](compact-p.md)
- FAQ: why PDFs disagree
- Reference YAML: [`modbus_yaml/cts700_2015_legacy.yaml`](../../modbus_yaml/cts700_2015_legacy.yaml)
