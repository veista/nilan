# Changelog (this fork)

Release history for [master3395/veista-nilan](https://github.com/master3395/veista-nilan).

GitHub Releases: https://github.com/master3395/veista-nilan/releases

| Version | Date | Summary | Notes |
|---|---|---|---|
| [1.3.19](1.3.19.md) | 07/11/2026 | Docs: Marketplace UI for HA 2026.11+ | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.19) |
| [1.3.18](1.3.18.md) | 06/11/2026 | HA 2026.11 Nordic bypass status + AI context | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.18) |
| [1.3.17](1.3.17.md) | 04/11/2026 | Fix blank Add Hub board menu labels (#6) | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.17) |
| [1.3.16](1.3.16.md) | 04/10/2026 | Compact P 20464 electrical supplement switch | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.16) |
| [1.3.15](1.3.15.md) | 03/09/2026 | Filter alarm logging + binary/switch last-good | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.15) |
| [1.3.14](1.3.14.md) | 02/09/2026 | CTS700 Nordic Modbus read stability + manual links | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.14) |
| [1.3.13](1.3.13.md) | 16/08/2026 | Setup register probe + Nordic filter days | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.13) |
| [1.3.12](1.3.12.md) | 14/08/2026 | VP 18comp (type 11) entity mapping (#234) | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.12) |
| [1.3.11](1.3.11.md) | 14/08/2026 | Non-blocking setup + multi-unit unique IDs | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.11) |
| [1.3.10](1.3.10.md) | 10/08/2026 | Config UX, hub coexistence, firmware field | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.10) |
| [1.3.9](1.3.9.md) | 10/08/2026 | Nordic room/DHW setpoints via Modbus FC6 | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.9) |
| [1.3.8](1.3.8.md) | 10/08/2026 | Nordic HVAC Auto/Off only; heat/cool as status | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.8) |
| [1.3.7](1.3.7.md) | 09/08/2026 | Nordic UX: fan 1-4, HVAC, DHW Off, sensor names | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.7) |
| [1.3.6](1.3.6.md) | 09/08/2026 | Polar/Nordic/Arctic XL hardware + T7/T9 | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.6) |
| [1.3.5](1.3.5.md) | 09/08/2026 | CTS700 Nordic XL era + `modbus_yaml/` | [Release](https://github.com/master3395/veista-nilan/releases/tag/v1.3.5) |
| [1.3.4](1.3.4.md) | 08/08/2026 | Full bolig + næring catalog matrices | Tag `1.3.4` |
| [1.3.3](1.3.3.md) | 08/08/2026 | CTS700 2015 legacy Modbus map | Tag `1.3.3` |
| [1.3.2](1.3.2.md) | 07/08/2026 | Auto-detect, issue fixes, HACS docs | Tag `1.3.2` |
| [1.3.1](1.3.1.md) | 04/08/2026 | Compact P live-test HVAC/fan fixes | Fork commit |
| [1.3.0](1.3.0.md) | 04/08/2026 | CTS700 Compact P 2018+ MVP | Fork commit |

Upstream baseline before this fork’s 1.3.x line: **1.2.28** ([veista/nilan](https://github.com/veista/nilan)).

## How to add a release

1. Bump `custom_components/nilan/manifest.json` version.
2. Add `changelog/X.Y.Z.md` and a row in this table.
3. Commit as **master3395**, tag `vX.Y.Z` (or `X.Y.Z`), push, create GitHub Release.

## Related docs

- [CTS700 era matrix](../docs/cts700/README.md)
- [Installation](../docs/installation.md)
- [Smoke matrix (1.3.5)](../to-do/CTS700-SMOKE-MATRIX.md)
