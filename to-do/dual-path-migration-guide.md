# Dual-path HA migration (YAML Modbus + Nilan integration)

Generic operator guide for sites running both YAML Modbus and the Nilan custom integration.

## Prerequisites

- Nilan fork **1.3.13+** (register probe, Nordic filter entities)
- Modbus TCP to the unit (typical port **502**, unit id **1** for CTS700, **30** for CTS602)

## Step 1: Upgrade Nilan

1. HACS → Custom repositories → `https://github.com/master3395/veista-nilan`
2. Update **Nilan** to latest release
3. Restart Home Assistant
4. Do **not** add hub until YAML overlap is trimmed or entities disabled

## Step 2: Avoid double-polling

Only one path should poll each register.

**Option A:** Comment out overlapping sensors/climates in Modbus YAML packages.

**Option B:** Disable duplicate entities in Settings → Entities (Modbus platform).

Typical overlaps to remove from YAML when integration is active:

- Room setpoint / climate (**4746** on Nordic)
- Filter sensors on wrong registers (use **1326 to 1329** on Nordic)
- Fan, temp, humidity, DHW sensors the integration provides

**Keep in YAML:**

- CTS selftest writes (**20148**, **20181**, etc.)
- Event log dump (**10000+**)
- Custom automations not in the integration map

## Step 3: Add Nilan config entry

1. Settings → Integrations → Nilan → Add hub
2. TCP, host (example `192.168.1.50`), port `502`, unit id per board
3. Board: **CTS700 Compact P Nordic XL**, **CTS700 2018+**, **CTS700 2015**, or **CTS602**
4. Setup probe runs once; `dead_registers` saved in config entry

## Step 4: Dashboard entity mapping

Entity ids follow the **device name** you set in the config flow (example below assumes `Nilan CTS700 Nordic`). Search-replace the prefix if yours differs.

| Card role | Integration entity (Nordic example) | Do **not** keep (YAML hub disabled) |
|-----------|-------------------------------------|-------------------------------------|
| Filter inlet remaining | `sensor.nilan_cts700_nordic_days_to_inlet_filter_change` | YAML filter sensors on wrong regs |
| Filter exhaust remaining | `sensor.nilan_cts700_nordic_days_to_exhaust_filter_change` | |
| Days since change | `sensor.nilan_cts700_nordic_days_since_*_filter_change` | |
| Room climate | `climate.nilan_cts700_nordic_hvac` | YAML `climate.room_temperature` if overlapping |
| Fan | `sensor.nilan_cts700_nordic_fan_speed_percent` | |
| Control / system mode | `sensor.nilan_cts700_nordic_control_state` | YAML `sensor.system_state` |
| Bypass status | `binary_sensor.nilan_cts700_nordic_bypass_flap` + `sensor.nilan_cts700_nordic_bypass_damper_percent` | `switch.bypass_damper` (unavailable / write unreliable) |
| DHW tank | `water_heater.nilan_cts700_nordic_top_water_heater` (current temp) | Ethernet dial alone as “tank target” |

Hardware limits (bypass write, DHW dial cap, installer auth): [docs/cts700/ethernet-limits.md](../docs/cts700/ethernet-limits.md).

## Step 5: Validate

1. Confirm Nilan entry healthy
2. Compare filter values to CTS700 HMI
3. Run custom selftest scripts if used
4. System log: no repeating Modbus ERROR for removed addresses (30 min watch)
5. Confirm `dead_registers` in config entry data after probe

## YAML-only filter fix (integration not used)

```yaml
# Include from modbus_yaml/cts700_nordic_xl.yaml (1326-1329 sensors)
# !include modbus_yaml/nilan_filter_templates.yaml
```
