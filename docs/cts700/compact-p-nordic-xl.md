# Compact P Køl Polar/Nordic/Arctic (XL) — CTS700 hybrid

Community-proven **CTS700** hybrid Modbus map for Compact P **Køl** Polar / Nordic / Arctic **(XL)** units on **CTS700 LC** boards (Ethernet). Fan user step is **4747 = 101–104**, not percent.

## Hardware match

Nilan drawings (varenr **75124xx**, CTS700 LC Board **v4.0**, styreprint **#237501**) label:

**Compact P Køl (Sol) Polar/Nordic/Arctic (XL)** · CTS700 Styring

Photos of **NCS-700 LC board** (v4.0 / v4.1) with Ethernet J8 fit this family. Schematics and produktliste: [hardware/](hardware/).

Catalog pages may still say CTS602 for some Compact P XL Nordic SKUs. If your unit is RS485 / HMI type **44**, use [../cts602/compactp.md](../cts602/compactp.md). If Modbus shows Nordic step fan on **4747**, use this board.

## When to use

Choose **CTS700 Compact P Nordic XL** in the config flow, or Auto-detect when holding **4747** is in **101–104**.

Use this if:

- Plate / wiring: Compact P Køl Polar / Nordic / Arctic (XL) with CTS700 LC
- Fan writes as steps **101–104** on register **4747**
- Room setpoint is **4746**, room current is input **5154**
- Live humidity on input **4716**, average humidity on **20164**

Do **not** use this map on 2018+ Compact P units that use fan **21771** percent and setpoint **20102**. That path is [compact-p.md](compact-p.md).

## Connection defaults

| Setting | Value |
|---|---|
| Protocol | Modbus TCP (native Ethernet) |
| Port | **502** (TCP) |
| Unit id | often **1** |

## Registers (YAML + integration parity)

| Function | Register | Notes |
|---|---|---|
| Room setpoint | 4746 holding | Scale 0.1 |
| Fan step | 4747 holding | **101–104** = steps 1–4 |
| Live humidity (RH) | 4716 input | 0–100 |
| Average humidity | 20164 holding | 0–100 |
| T1 outdoor | 5152 input | Scale 0.1 |
| T2 supply | 5153 input | Scale 0.1 |
| T3 extract / room | 5154 input | Scale 0.1 |
| T4 after HEX | 20288 holding | |
| T5 condenser | 20290 holding | Cooling path |
| T6 evaporator | 20292 holding | Cooling path |
| T7 supply after heater | 20294 holding | |
| T8 preheater path | 5159 input | Polar/Nordic |
| T9 water surface | 20298 holding | |
| T11 / T12 DHW | 5162 / 5163 input | Scale 0.1 |
| Filter alarm | 5168 input | Binary (Filtervagt) |
| Filter interval inlet / exhaust | 1326 / 1327 holding | Service interval days |
| Filter remaining inlet / exhaust | 1328 / 1329 holding | Days until change |
| Filter days (alternate) | 20103 holding | May mirror 1328 on some firmware; **absent** on others (see issue #3) |
| Days since change | 1326 − 1328 (inlet), 1327 − 1329 (exhaust) | Matches HMI "days since filter change" |
| Op mode | 5432 holding | 0 off, 1 cool, 2 heat, 3 dehum, 4 DHW |
| Anode | 4233 holding | |
| Fan power % | 21771 holding | Readout; climate fan writes use 4747 steps |
| Bypass damper % / state | 21773 / 4704 / 4705 holding | **Status only** in the integration (Ethernet writes unreliable) |
| Supply / extract fan % | 4699 / 4700 | |
| DHW setpoint | 5548 holding (legacy/hybrid), 20460 (2018+ map) | Ethernet dial often caps near ~25.5 C; tank current is T11/T12 (**5162** / **5163**), not the dial |

External CO2 (accessory on SG A/B) stays out of this bus map unless you add a separate sensor.

## Bring-up with YAML

1. Copy [`modbus_yaml/cts700_nordic_xl.yaml`](../../modbus_yaml/cts700_nordic_xl.yaml)
2. Set `host:` to the CTS Ethernet IP
3. Include **only** that file (never with another board YAML)
4. Pause YAML before enabling the Nilan custom integration on the same unit

## Caveats

- **Ethernet limits:** [ethernet-limits.md](ethernet-limits.md) (bypass status-only, DHW dial vs tank, YAML coils when hub disabled). Tested on HA Core **2026.11.0** / OS **18.5.rc1**.
- **Week programs** are not synced. HA writes can fight a week program still active on the controller.
- Active cooling (compressor M6) depends on outdoor conditions and unit alarms; mode **Kjøling** alone does not guarantee compressor run.
- Never copy Nordic step fan writes onto a 2018+ Compact P entry.
- **HVAC mode (holding 5432):** treated as **status** (active cool/heat/dehum/DHW), not a user setpoint. Climate selectable modes are **Auto** and **Off** only; heat/cool still show under HVAC *action* when the unit is doing that. Steer comfort with room setpoint (**4746**) and fan step.
- **Fan steps:** climate offers **1–4** only (4747 = 101–104). There is no fan-off via step 0 on these boards.
- **DHW Off:** top/bottom water heaters share setpoint **20460**. Off via setpoint 0 is not reliable, so Nordic entities expose temperature only (no Off operation mode).
- **Electrical supplement heater (20464):** Compact P **2018** map only (writable HA switch). This Nordic hybrid path has **no** dedicated el-supplement holding in the community map; `get_electric_water_heater_state` stays False and writes are refused. Do not map 20464 onto Nordic.
- **Sensor names:** follow Nilan wiring (T1 outdoor, T6 evaporator, T7 after after-heater, T8 preheater path). T5/T6/T7/T8/T9 are diagnostic; T7 is disabled by default when unused (often reads 0.0).
- **T1 vs T8:** different registers (input **5152** vs **5159**; optional holding **20296**). On Polar/Nordic both are outdoor / preheater-path NTCs, so equal readings with preheater idle are normal, not a double-map bug. If 5159 mirrors T1 but **20296** differs, the integration prefers **20296**.
- **Extra percent sensors:** heat-pump effort % is useful if the unit exposes a live register (share address to add). Configured max DHW effort and per-filter % are low value when filter **days** already exist; keep those out of the default entity set.
- **Setpoint writes:** room **4746** and DHW **20460** use Modbus **FC6** (`write_register`) first, same as HA YAML climate. Fan step **4747** may use FC16. If air/water temp UI snaps back, check HA logs for `CTS700 Nordic temp write`.

## Related

- [Hardware drawings](hardware/README.md)
- [CTS700 era matrix](README.md)
- [Catalog hub](../catalog/compact-p-xl-nordic.md)
- [2018+ Compact P](compact-p.md)
- [2015 legacy](legacy-2015.md)
- Dashboard: [`dashboards/cts700_compact_p_nordic_xl.yaml`](../../dashboards/cts700_compact_p_nordic_xl.yaml)
