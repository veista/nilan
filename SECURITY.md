# Security Policy

## Supported versions

Security fixes are applied on the default branch of this fork (`master`) and released when practical. Prefer the latest release or default branch when testing.

| Version | Supported |
|---|---|
| Latest release / `master` | Yes |
| Older releases | Best effort |

Upstream project: https://github.com/veista/nilan

## Reporting a vulnerability

**Do not** open a public GitHub issue or public pull request for security-sensitive findings.

Prefer one of these private channels:

1. **GitHub Private Vulnerability Reporting** on this repository (Security → Advisories → Report a vulnerability), when enabled.
2. Contact the fork maintainer via GitHub: [@master3395](https://github.com/master3395)

Please include:

- Affected version or commit
- Home Assistant version
- Board type (CTS602 / CTS700) and how you connect (TCP / Serial)
- Steps to reproduce
- Impact (what an attacker could do)

You can expect an initial response within **7 days** when possible. Fixes may take longer depending on severity and available maintainer time.

## Threat model (summary)

This is a Home Assistant **custom integration** that talks to a Nilan unit over **local Modbus TCP or RTU**.

### Trust assumptions

- The home LAN and serial bus are trusted.
- Anyone who can reach the Modbus port can already read and write HVAC registers without this integration.

### In scope

- Secrets, tokens, or credentials committed to the repository or written into logs
- Unsafe handling of dependencies (for example `pymodbus`) with known advisories
- Malicious changes merged to the default branch without review
- Debug logging that leaks install passwords or similar secrets

### Out of scope (typical)

- Treating LAN Modbus access itself as remote code execution
- Attacks that require physical or already-privileged access to the Home Assistant host
- Issues that only affect unsupported or undocumented register maps without a clear security impact

## Incident response (lightweight checklist)

1. **Triage:** confirm severity and affected versions; keep discussion private until a fix is ready.
2. **Mitigate:** revoke leaked secrets; pin or bump vulnerable dependencies; disable risky code paths if needed.
3. **Fix:** develop on a private fork or private advisory branch when available.
4. **Release:** publish a fixed version / tag; note the issue in release notes without unnecessary exploit detail.
5. **Disclose:** publish or update the advisory after users have a reasonable path to upgrade.

## Maintainer notes

- Enable MFA on GitHub accounts with write access.
- Keep the default branch protected with required checks when collaborators are added.
- Never commit Home Assistant secrets, real LAN IPs in examples beyond placeholders like `192.168.1.50`, or Nilan installer passwords.
