## Summary

Briefly describe what this PR changes and why.

## Checklist

- [ ] CTS602 behavior unchanged unless this PR is explicitly about CTS602
- [ ] Docs updated under `docs/` when device support or setup steps change
- [ ] No secrets, credentials, or real LAN IPs (use `192.168.1.50` in examples)
- [ ] No em dash (U+2014) in user-facing docs or README copy for this fork
- [ ] Docs/strings reviewed for clarity; meaning is not conveyed by color alone
- [ ] Shared Lovelace under `dashboards/` stays **Nilan-only** if touched

## Test plan

- [ ] Config flow / auto-detect (if changed)
- [ ] Live or simulated Modbus read/write for affected entities
- [ ] Hassfest / validate workflows pass
