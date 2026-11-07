# Contributing

Thank you for helping improve the Nilan Home Assistant integration.

Please also read:

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Accessibility](ACCESSIBILITY.md)

## Branch targets (this fork)

Working fork: https://github.com/master3395/veista-nilan

- Day-to-day CTS700 Compact P work lives on fork **`master`**
- Upstream project: https://github.com/veista/nilan
- Open a pull request to `veista/nilan` only when the change is ready and tested
- Prefer public issues/PRs for non-security topics; use private vulnerability reporting for security

Do not open drive-by PRs against unrelated branches.

### Maintainer expectations (fork)

- Default branch should stay protected with required CI checks when collaborators are added
- Accounts with write access should use MFA
- Keep shared Lovelace under `dashboards/` **Nilan-only**

## Register changes

When adding or changing Modbus registers, update **all** of:

1. [`custom_components/nilan/registers.py`](custom_components/nilan/registers.py)
2. Matching device getter in `device*.py`
3. [`register_probe.py`](custom_components/nilan/register_probe.py) `PROBE_SPECS` when the register is optional per firmware
4. Matching [`modbus_yaml/`](modbus_yaml/) example file

## Before you open an issue

1. Read previous [issues](https://github.com/veista/nilan/issues), [wiki](https://github.com/veista/nilan/wiki), [discussions](https://github.com/veista/nilan/discussions), and [release notes](https://github.com/veista/nilan/releases).
2. Check device docs under [`docs/`](docs/README.md) for your controller and model.

## Reporting CTS700 issues

CTS700 Compact P MVP is developed on this fork first. Still needed: GEO / slave 4 dumps and confirmation of edge firmware maps.

Please include:

- Device plate photo
- Firmware / software version
- Slave / unit id map
- Register dump (or Modbus YAML) for the registers you care about
- Which entities work or fail
- Example host only in public posts: `192.168.1.50` (never paste real LAN IPs)

Tracking: https://github.com/veista/nilan/issues/19

## Reporting CTS602 issues

If install fails with unsupported device:

1. Enable debug logging for the integration and try again; attach the log.
2. Photo of the device type plate.
3. HMI350T: photo of the device info page.
4. CTS602 HMI: photo of `SHOW DATA` -> `TYPE`.

For other bugs, include: logs, Modbus version, device type and device version as shown in the integration.

## Register dump checklist

Use this when asking to mark a [catalog](docs/catalog/bolig-matrix.md) SKU as `supported`, or when install fails with an unknown type id.

### Required

1. **Segment:** bolig or næring (commercial)
2. **Marketing model** from the plate (e.g. Comfort 600, Compact P2 AIR, VPM 240 M2)
3. **Controller** if known: CTS602, CTS700, CTS400, unknown
4. **Modbus unit id** and TCP vs serial / bridge
5. **CTS602 `control_type`** (holding 1000) or debug log line `Device Type = …`
6. **20–30 key register reads** with labels (temps, fan, humidity, DHW, alarms)
7. Photos: plate + HMI type page (no personal home details)
8. Example host only: `192.168.1.50`

### Nice to have

- Software / bus version
- AIR vs GEO / Polar / EK options
- Whether CTS700 20xxx or 2015 under-10000 map responds
- Commercial: airflow setpoints and alarm words

Open a GitHub issue with the **Unsupported device / register dump** template.

### Want your SKU marked supported?

1. File the dump issue above.
2. Maintainers map marketing name → HMI type id / board in `docs/catalog/`.
3. Only then are new type ids added to `CTS602_DEVICE_TYPES` (no invented maps).

## Pull requests

1. Fork and create a topic branch from the branch you intend to improve.
2. Keep CTS602 behavior unchanged unless the PR is explicitly about CTS602.
3. Prefer small, focused commits with a clear why.
4. Update [`docs/`](docs/README.md) when you add or change device support.
5. Do not put secrets, real LAN IPs, or credentials in commits or issue text.
6. Do not use em dash characters (Unicode U+2014) in user-facing docs or README copy for this fork.

## Code notes

- Secrets belong in Home Assistant config / secrets, never in this repository.
- CTS602 and CTS700 use different register maps and typical unit ids.
- Keep modules readable; large device I/O belongs in dedicated modules (for example `device_cts700.py`).
- Capability profiles live in `capabilities.py`; optional entity key `requires_capabilities`.

## License

By contributing, you agree that your contributions are licensed under the same [Apache License 2.0](LICENSE) as the project.

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for people who shipped code or high-signal testing on this fork (including [Martsola](https://github.com/Martsola) and [mark007](https://github.com/mark007)).

