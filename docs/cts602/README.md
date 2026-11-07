# CTS602

Stable support for Nilan units with the **CTS602** controller board.

## Setup summary

1. Connect via Modbus TCP bridge or USB-RS485 (see [hardware](../hardware.md)).
2. Install the integration ([installation](../installation.md)).
3. Choose interface **TCP** or **Serial**, then **Auto-detect** or board **CTS602**.
4. Default unit id: **30** (confirm on your unit; auto-detect may try **1** then **30**).
5. During validation the integration reads the CTS602 control type register and matches it to a known HMI device name.

## Device guides

See the index table in [docs/README.md](../README.md).

## Coverage

Most climate, sensor, water heater, select, number, and switch entities are supported when your bus version and hardware options allow them. Missing critical features: open an issue with logs and HMI type photos ([CONTRIBUTING.md](../../CONTRIBUTING.md)).

Commercial Comfort 600+ / VR / VPR / VPM: see [commercial.md](commercial.md). Compact P2: see [compact-p2.md](compact-p2.md).

## CompactP note

HMI type **CompactP** (id 44) may appear as CompactP, CompactP AIR, or CompactP GEO depending on software. That is still the **CTS602** board path, not CTS700 Ethernet. For Compact P with a **CTS700** controller, use [../cts700/compact-p.md](../cts700/compact-p.md).
