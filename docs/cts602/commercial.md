# Commercial CTS602 path

Comfort 600 / 1200 / 5000, VR, VPR, and VPM commercial lines use **CTS602** with Modbus RS485 in Nilan product documentation.

## Setup

1. Prefer board **CTS602** or **Auto-detect** (Auto-detect tries CTS602 first).
2. Typical unit id **30**.
3. If the HMI type id is already in `CTS602_DEVICE_TYPES`, entities load like other CTS602 units.
4. Unknown type id: fail clearly and file a [dump](../../CONTRIBUTING.md#register-dump-checklist).

## Do not

- Select CTS700 Compact P maps for these units without a proving dump
- Assume bolig id `VPM/28EC` (26) covers VPM 120+ commercial

## Docs

- [Næring matrix](../catalog/naering-matrix.md)
- [Næring research](../naering/README.md)
- [CTS400](../naering/cts400.md) (not implemented)
