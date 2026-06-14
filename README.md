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
- COMFORTn
- COMBI 300 N
- COMBI 302
- COMBI 302 T
- VGU180 ek
- VENTEC
- CompactP (AIR/GEO)

Majority of functions are supported. If some critical is missing please leave an issue.

If you have CTS700 or another device you will have to help me with that.

## CTS400 / ES1077 (Comfort 250 Top)

Experimental support for the **CTS400** controller (also labelled **ES1077**),
as used in the **Nilan Comfort 250 Top**, is available as a separate board
family. The CTS400 uses a completely different Modbus register space from the
CTS602 above, so it is selected explicitly rather than auto-detected.

- **Pick the board during setup.** The config flow first asks which controller
  board you have (CTS602 or CTS400). CTS400 cannot be auto-detected because it
  has no `control_type` register, so the integration would otherwise reject it
  as an unsupported device.
- **Tested hardware.** Verified live on a Comfort 250 Top (CTS400, firmware 1.0)
  over Modbus RTU (slave 30, 19200 8E1) through a Waveshare RS485 TO ETH (B)
  bridge.
- **CO2 / VOC are optional.** Those sensors appear only if the unit reports a
  fitted extra sensor (holding register 48); on a base unit they are hidden.
- **Ventilation control.** The unit is exposed as a `fan` entity with four speed
  levels, and as a `climate` entity (FAN_ONLY) that combines the wanted room
  temperature, run/stop and fan level into one thermostat card. A run/stop
  switch and a fan-level number are also provided but disabled by default.
- **Setpoints.** The wanted room temperature, the summer/winter switch-over
  threshold, and the filter-change interval are exposed as adjustable numbers.
  Note the season threshold is hysteretic: the unit leaves winter mode slowly
  after the threshold is lowered.
- **Alarms.** Raw alarm codes are exposed as diagnostic sensors; a code-to-name
  mapping has not been confirmed for this controller and is therefore not
  provided.

This support is a work in progress tracked in
[discussion #165](https://github.com/veista/nilan/discussions/165). If you have a
CTS400 / ES1077 unit, a debug log and a type-plate photo are very welcome.

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

