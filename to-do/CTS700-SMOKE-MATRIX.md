# CTS700 / CTS602 smoke matrix (1.3.5)

Manual checklist after Nordic / era work. One poller per unit.

## Compatibility contract

| Board | Fan write | Setpoint | Must not load |
|---|---|---|---|
| CTS700_LEGACY | 4747 percent | 4746 | Nordic 101–104 writers |
| CTS700_NORDIC | 4747 steps 101–104 | 4746 | 2018+ 21771 as climate fan write |
| CTS700 (2018+) | 21771 percent | 20102 | Nordic 4747 step writers |
| CTS602 CompactP (44) | CTS602 map | CTS602 map | CTS700 addresses |

Probe order: CTS602 → Nordic → 2018+ → legacy.

## Checks

### 2018+ Compact P (your unit)

- [ ] Config entry board = `CTS700`
- [ ] Fan climate write changes holding **21771** percent (not 4747 steps)
- [ ] Room setpoint read/write via **20102**
- [ ] Room current via **20286**
- [ ] T8 / preheater sensor present if **20296** answers
- [ ] No Nordic-only entities broken (filter alarm 5168 not required)

### Nordic XL (mark007)

- [ ] Config entry board = `CTS700_NORDIC` (or Auto-detect picks it when 4747∈101..104)
- [ ] Fan steps write **101–104** on **4747**
- [ ] Setpoint **4746**, room current input **5154**
- [ ] Live humidity **4716**, average **20164**
- [ ] T1–T6 / T8 / T11–T12 present
- [ ] Filter days **20103**, filter alarm **5168**, anode **4233**
- [ ] Op mode **5432** maps to climate
- [ ] Fan power / supply / extract percent sensors present

### 2015 legacy

- [ ] Board = `CTS700_LEGACY`
- [ ] Fan **4747** percent (0/25/50/75/100), not 101–104
- [ ] If 4747 is 101–104, entry must be Nordic instead

### CTS602 CompactP type 44

- [ ] Board = `CTS602`, type 44 still loads
- [ ] No CTS700 20xxx / Nordic fan path used

### Cross rules

- [ ] YAML Modbus file from `modbus_yaml/` not active while Nilan integration polls same host
- [ ] Only one YAML file loaded if using Modbus package
- [ ] Week program note understood (no sync; can fight HA writes)
