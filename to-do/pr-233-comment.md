Thanks @Martsola for the CompactPC GEO XL + Comfort CT200 report, and thanks also to mark007 for the parallel Compact P Nordic / Polar feedback on the fork.

### Martsola (this PR)

1. **Blank Select Controller Board / Confirm menus**  
   Confirmed. A YAML Modbus hub named bare `nilan` conflicts with this integration domain and can blank those step labels. Rename the hub (e.g. `nilan_compactpc`), reload Modbus / restart HA, then open setup again. Upstream CTS602-only flows did not show these new board/confirm steps, so the clash was less visible there.

2. **Control State Ventilation ↔ Unknown**  
   Confirmed. Many Compact P / CTS700 boards do not like overlapping Modbus sessions. Pause or remove YAML Modbus for that unit while using the Nilan integration (or the reverse). One client at a time.

3. **Outdoor temperature in the Firmware field**  
   Fixed on the fork: Firmware / software is now a map label only (e.g. `CTS700 2015 map`). Outdoor stays on the normal T1 / outdoor sensor.

Happy to take CompactPC GEO XL dumps or feature ideas when you have them.

### mark007 (Nordic / Polar XL)

1. **T1 and T8 identical**  
   Not a double-map bug: Nordic uses input **5152** (T1) vs **5159** (T8). On Polar/Nordic both are outdoor / preheater-path NTCs, so equal values with preheater idle are normal. From **1.3.10**, if **5159** mirrors T1 we also try holding **20296**, and T8 is marked diagnostic.

2. **Extra sensors (HP effort %, max DHW effort, filter %)**  
   Agree with your ranking: live **heat-pump effort %** is worth adding if you can share the register address from a dump. Configured max DHW effort and per-filter % are lower value when filter **days** already exist, so we are not adding those to the default entity set.

### Fork release

These fixes (plus clearer config-flow warnings / Accept–Manual confirm menu, and unique internal hub names `nilan_hub_<entry_id>`) are in:

https://github.com/master3395/veista-nilan/releases/tag/v1.3.10

Backwards compatible with existing config entries; reload Nilan after upgrade.
