# Hardware and connection

## CTS700 Ethernet (native LAN)

Cat5e (or better) from the CTS700 LAN port to your router is enough for Modbus TCP. No RS485 bridge is required for native Ethernet CTS700.

- TCP port: **502**
- Typical indoor unit id: **1**
- Example host in docs/issues only: `192.168.1.50`

## CTS602 (and RTU-style) installs

You need one of:

- Modbus RTU to Modbus TCP bridge
- USB to RS485 adaptor

### Tested bridges

- USR-TCP232-410S
- Waveshare RS485 TO ETH (B)
- https://github.com/veista/modbus_bridge

Typical CTS602 unit id is **30** (confirm on your unit).

## Notes

- Prefer a single Home Assistant poller on CTS700; multiple pollers can overload the controller.
- Hide unused entities in the UI when a feature (CO2, GEO / slave 4, floor heating) is not installed.
