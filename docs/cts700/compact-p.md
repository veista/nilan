# Compact P (CTS700)

Community-tested MVP for **Compact P** with a **CTS700** controller over Ethernet Modbus TCP.

## Hardware

- Cable: Cat5e or better from CTS700 **LAN** port to your router
- Protocol: Modbus TCP
- Port: **502**
- Unit id: **1** (indoor; confirm on your unit)
- Example host in public docs only: `192.168.1.50`

No RS485 bridge is required for native Ethernet CTS700.

## Home Assistant setup

1. Install from **Marketplace** (HA 2026.11+) / **HACS** (older), or copy `custom_components/nilan` from this fork (`master`). See [installation.md](../installation.md).
2. Add **Nilan** integration.
3. Choose **TCP**.
4. Choose **CTS700 (2018+ / Compact P)**.
5. Enter IP, port `502`, unit id `1`.

Do **not** choose Nordic XL if fan is percent on **21771**. Nordic step fan (**4747 = 101–104**) is a different board: [compact-p-nordic-xl.md](compact-p-nordic-xl.md).

## Live-verified registers (Compact P)

| Function | Register | Notes |
|---|---|---|
| Room current | 20286 | Extract / room air. Do **not** use 20260 as current (~5 C wrong on installs like issue #19) |
| Room setpoint | 20102 | Live-verified |
| DHW setpoint | 20460 | Shared Compact P DHW dial |
| Electrical supplement heater | 20464 | R/W 0/1. Home Assistant **switch** (writable). DHW supplement only; not a bottom-tank 60 C command. Heat pump DHW still tops out around **55 C** at T12. Scalding protection is **20463**. |
| Outdoor | 20282 | Scale 0.1 |
| Supply | 20284 | Scale 0.1 |
| Extract | 20286 | Scale 0.1 |
| Humidity | 20164 | No 0.1 scale |
| Fan speed | 21771 | Percent 0-100 on Compact P (integration maps to climate levels 0-4) |
| After heat exchange | 20288 | |
| After heat pump | 20290 | |
| T8 before pre-heater | 20296 | Safe 20xxx extra (not Nordic input 5159) |

Protocol PDF (2018):  
https://www.en.nilan.dk/Files/Files/Engelsk/Downloads/7.%20Modbus%20-%20BACnet/2018_04_Modbus_CTS700_Modbus_protokol.pdf

## Live HA verification (04/08/2026)

Side-install from this fork `master` on Home Assistant OS, CTS700 Compact P over Modbus TCP (unit id 1, port 502). Existing Modbus YAML was paused for the test so only one poller ran.

| Check | Result |
|---|---|
| Room climate | Current ~24.5 C, setpoint 18 C |
| Humidity | 39% |
| DHW | Tank ~52 C |
| Outdoor / T1 | ~15.9 C |
| Fan (21771) | 75% (maps to climate fan level 3) |
| Config flow | TCP → CTS700 → create entry OK |

After the test, the Nilan config entry was removed and Modbus YAML restored as primary. Do not run YAML Modbus and this integration against the same unit at once.

Fixes from that pass (v1.3.1): climate HVAC mode no longer stuck on `unknown` for unmapped operating-mode values; fan percent mapped to levels 0-4 for the climate entity.

## MVP entities

- Room climate (current, setpoint, fan, on/off / mode where mapped)
- Outdoor, supply, extract, after HEX / HP, evaporator temps
- Humidity
- DHW setpoint and tank temperatures
- Electrical supplement heater switch (`switch.nilan_electrical_supplement_heater` when the device is named `Nilan`): holding **20464**
- Days to air filter change

## Caveats

- Slave 4 floor / GEO-style maps often unavailable on Compact P Air-only installs
- CO2 reads 0 without a CO2 module: hide unused entities
- Avoid multiple Home Assistant pollers against the same CTS700
- PDF labels can differ from live Compact P setpoints
- Operating mode register `20120` is not a full CTS602-style heat/cool/auto enum on every Compact P; UI may show Auto when the raw value is unmapped
- **20464** enables the electrical DHW supplement heater. It does not tell the heat pump to heat the tank bottom to 60 C. Scalding limit is **20463**. CTS602 still uses output **116** (`output_water_heat`) as status only.

## Not this guide

- Older CTS700 firmware with registers under 10000: use [legacy-2015.md](legacy-2015.md).
- Nordic XL hybrid (4747 steps 101–104): use [compact-p-nordic-xl.md](compact-p-nordic-xl.md).
- Compact P with a **CTS602** HMI / board (type id 44): use [../cts602/compactp.md](../cts602/compactp.md).

## Related

- [CTS700 era matrix](README.md)
- [Hardware](../hardware.md)
- [FAQ](../faq.md)
- Reference YAML: [`modbus_yaml/cts700_2018_compact_p.yaml`](../../modbus_yaml/cts700_2018_compact_p.yaml)
- Issue tracking: https://github.com/veista/nilan/issues/19
