## Issue #3: probe + dual-path resolution (CTS700 Nordic example)

Validated on live **CTS700 Nordic** Modbus TCP (unit id 1).

### Filter registers (verified on one Nordic unit)

| Register | Value | Meaning |
|----------|-------|---------|
| 1326 | 165 | Inlet interval |
| 1328 | 155 | Inlet remaining |
| 1327 | 180 | Exhaust interval |
| 1329 | 0 | Exhaust remaining |
| 20103 | 155 | Mirrors 1328 on this firmware |

Days since inlet change: **165 - 155 = 10**.

### Repo changes (v1.3.13)

- Setup-time register probe, Nordic inlet/exhaust filter entities, `dead_registers` persistence
- **modbus_yaml/** synced: 1326-1329 filter sensors, DHW 5548 primary, dual-path README
- Probe script: `to-do/probe_registers.ps1`
- Migration guide: `to-do/dual-path-migration-guide.md`

### Dual-path sites (YAML + integration)

For sites with existing YAML Modbus: upgrade to 1.3.13, trim or disable overlapping YAML polls, add config entry so integration probe handles dead 20xxx on firmware that lacks them.

Units with **both** 1326-1329 and live 20103 should prefer 1326-1329 for inlet/exhaust split; exhaust at 0 days remaining is correct per 1329.
