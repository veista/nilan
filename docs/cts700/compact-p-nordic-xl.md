# Compact P Køl Polar/Nordic/Arctic (XL) — CTS700 hybrid

Community-proven **CTS700** hybrid Modbus map for Compact P **Køl** Polar / Nordic / Arctic **(XL)** units on **CTS700 LC** boards (Ethernet). Fan user step on **4747** may be classic **101–104** or **percent 0–100** (same as **21771** on some firmwares); the integration maps percent to steps 1–4 via nearest of **20140/42/44/46**.

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
| Fan step | 4747 holding | **101–104** = steps 1–4, or **percent 0–100** (map via 20140/42/44/46) |
| Fan step % targets | 20140 / 20142 / 20144 / 20146 | Supply percents for steps 1–4 |
| Live humidity (RH) | 4716 input | 0–100 |
| Average humidity | 20164 holding | 0–100 |
| Ventilation pause | 20100 holding | Switch |
| Humidity strategy | 20160–20163 | Low RH %, fan steps, timeout |
| Allow active cooling | 20180 holding | Switch |
| Frost / preheat | 20300 / 20340 / 20341 | Polar frost enable + thresholds |
| DHW pause / days | 20440 / 20441 | Switch + days |
| El-supplement below / scalding / el switch | 20462 / 20463 / 20464 | Numbers + switch (scale 0.1 on temps) |
| Anti-legionella | 20480–20483 | Manual / auto / day / time |
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
| Op / panel mode | 5432 holding | **Panel text match:** 0 Off, 1 Cooling, 2 Heating, 3 Dehumidification, 4 Hot water production. Exposed as `panel_operating_mode` (always) and drives `control_state` when compressor effort **4706 > 0** (7 Heating / 8 Cooling / 9 Hot water production). |
| Anode | 4233 holding | |
| Fan power % | 21771 holding | Readout; climate fan writes use 4747 steps |
| Bypass damper % / state | 21773 / 4704 / 4705 holding | **Status only** in the integration (Ethernet writes unreliable) |
| Main compressor effort % | 4706 holding | 0 when heat pump off; positive % when running (mark007 / community) |
| Heat pump on | derived from 4706 | Binary: effort > 0 |
| Heater control bit | 4701 holding | Optional discrete heater; used with 4706 for hvac_action |
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
- **HVAC mode (holding 5432):** treated as **status** (active cool/heat/dehum/DHW), not a user setpoint. Climate selectable modes are **Auto** and **Off** only. This is the register that answers “is compressor effort for DHW, air heating, or cooling?” when **4706 > 0**. Use sensor **Panel operating mode** for the live panel value even while effort is 0 (hysteresis).
- **HVAC action hysteresis (mark007):** do **not** keep `hvac_action=heating` for the whole thermostat call / mode=heat window. Report room **heating** only while compressor effort **4706 > 0** (and/or heater bit **4701**) and **5432** is heat (not DHW or cool). When mode is heat but effort is 0, action is **idle** (fans may still run). Smart-plug correlation on Compact P: idle about **40 W**, active heat about **500-700 W**. El-supplement **20464** is a separate DHW switch, not room `hvac_action`.
- **Water vs air priority:** CTS602 select **Hot Water Priority** (holding **1702**, Water/Inlet) is **illegal address** on Compact P Nordic Ethernet. Holding **20184** (`cooling_priority_to_hot_water`) reads on Nordic (live value seen as 1) but enum / HMI “water priority” mapping is **not verified**; do not treat it as a confirmed writable priority select yet.
- **Fan steps:** climate offers **1–4** only. **4747** may be 101–104 or percent; percent maps via nearest step table / **21771**. No fan-off via step 0.
- **DHW Off:** top/bottom water heaters share setpoint **20460**. Off via setpoint 0 is not reliable, so Nordic entities expose temperature only (no Off operation mode).
- **Electrical supplement heater (20464):** writable switch on Nordic (live R/W validated). Numbers **20463** (scalding) and **20462** (el-supplement below) exposed.
- **Sensor names:** follow Nilan wiring (T1 outdoor, T6 evaporator, T7 after after-heater, T8 preheater path). T5/T6/T7/T8/T9 are diagnostic; T7 is disabled by default when unused (often reads 0.0).
- **T1 vs T8:** different registers (input **5152** vs **5159**; optional holding **20296**). On Polar/Nordic both are outdoor / preheater-path NTCs, so equal readings with preheater idle are normal, not a double-map bug. If 5159 mirrors T1 but **20296** differs, the integration prefers **20296**.
- **Extra percent sensors:** main compressor effort is holding **4706** (binary heat-pump-on when effort > 0). Configured max DHW effort and AI-guessed per-filter % stay out of the default entity set. Secondary compressor stages **4707–4711** stay unused until field-verified during a heating event.
- **Setpoint writes:** room **4746** and DHW **20460** use Modbus **FC6** (`write_register`) first, same as HA YAML climate. Fan step **4747** may use FC16. If air/water temp UI snaps back, check HA logs for `CTS700 Nordic temp write`.

## Related

- [Hardware drawings](hardware/README.md)
- [CTS700 era matrix](README.md)
- [Catalog hub](../catalog/compact-p-xl-nordic.md)
- [2018+ Compact P](compact-p.md)
- [2015 legacy](legacy-2015.md)
- Dashboard: [`dashboards/cts700_compact_p_nordic_xl.yaml`](../../dashboards/cts700_compact_p_nordic_xl.yaml)
