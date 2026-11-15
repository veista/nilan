[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
# Nilan
Nilan integration for Home Assistant

CTS602 supported devices (as typed in HMI menu):

- Comfort light
- Comfort Polar
- VPL 15c
- CompactS
- VP18cCom
- COMFORT
- VP 18c
- VP 18ek
- VP 18cek
- VPL 25c
- VPM/28EC
- VP18cCoB
- COMPACTn
- COMFORTn
- COMBI 300 N
- COMBI 302
- COMBI 302 T
- VGU180 ek
- VENTEC
- CompactP (AIR/GEO)

Majority of functions are supported. If some critical is missing please leave an issue.

If you have CTS700 or another device you will have to help me with that.

## Installation
### Hardware
You must have one interface type installed on your Nilan device for this Integration to work 

#### Supported Interface Types
- ModBus RTU to Modbus TCP Bridge 
- USB to RS485 adaptor

#### Tested Known-to-work Bridge Devices
* USR-TCP232-410S
* Waveshare RS485 TO ETH (B)
* https://github.com/veista/modbus_bridge
* Elfin EW11 (WiFi), see [Elfin EW11 setup](#elfin-ew11-setup)

#### Elfin EW11 setup
Known-working configuration, tested with EW11 firmware 1.50.0 on a CTS602 unit (Modbus address 30).

**Serial Port Settings**

| Setting | Value |
|---|---|
| Baud Rate / Data Bit / Stop Bit / Parity | 19200 / 8 / 1 / Even |
| Buffer Size | 512 |
| Gap Time | 10 ms |
| Flow Control | Half Duplex |
| Protocol | Modbus |

**Communication Settings** (socket `netp`)

| Setting | Value |
|---|---|
| Protocol | Tcp Server |
| Local Port | 502 |
| Buffer Size | 512 |
| Keep Alive | 60 s |
| Timeout | 60 s |
| Max Accept | 3 |
| Route | Uart |

Notes:
- The serial-page Protocol must be **Modbus**. That is what makes the EW11 translate Modbus TCP to Modbus RTU; a plain transparent serial bridge will not work.
- Flow Control **Half Duplex** is needed for RS485.
- Gap Time 10 ms (default 50 ms) and socket Timeout 60 s (default 3 s) noticeably reduced "Not connected" errors in long-term use.
- If the connection stops responding after a Home Assistant restart, restart the EW11 from its web UI (Other tab).

### Software
#### Manually
- Copy the nilan folder into your custom_components folder
- Restart HA
- Add Nilan from Integrations

#### HACS
- This integration is available from HACS
- Add Nilan from Integrations

## Issues
1. Before submitting an issue, read the previous <a href="https://github.com/veista/nilan/issues?q=">issues</a>, <a href="https://github.com/veista/nilan/wiki">wiki</a>, <a href="https://github.com/veista/nilan/discussions">discussions</a> and <a href="https://github.com/veista/nilan/releases">release notes</a>.
2. If you have a CTS700 device, it is a long road to get it supported by this integration, open an issue and we will go forward there
3. If you have a CTS602 device and you get a device not supported error during installation:
  - Turn on debug logging for the integration and try installing the integration again. Take note of the debug log and submit it with the issue.
  - Take a picture of the device type plate and submit it with the issue.
  - If you have HMI350T - Touch screen HMI - installed on your device, take a picture of the device info page and submit it with the issue.
  - If you have CTS602 HMI, take a picture of "SHOW DATA" -> "TYPE" and submit it with the issue.
4. On other Issues:
  - Submit the following: Logs, Modbus Version, Device Type - as Shown in the Integration, Device Version - as Shown in the Integration

## Support
If you like the integration, please leave a star and concider donating or becoming a sponsor.

