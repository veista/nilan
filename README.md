[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
# Nilan
Nilan integration for Home Assistant

Only CTS602/HMI350T support at this time.
Supported devices (as typed in HMI menu):
- VP 18c
- COMBI 302

Supports co2 sensor as well. After-heater support in the works.
- Majority of functions are supported. If some critical is missing please leave an issue.

If you have CTS700 or another device you will have to help me with that.

## Installation
### Hardware
You must have a ModBus RTU to Modbus TCP Bridge installed on your Nilan device for this integration to work.

The easiest way is to purchase one, but you can also build one easily with an ESP8266/ESP32 https://github.com/veista/modbus_bridge

### Software
#### Manually
- Copy the nilan folder into your custom_components folder
- Restart HA
- Add Nilan from Integrations

#### HACS
- This integration is available from HACS

## Issues
1. Before submitting an issue, read the previous issues.
2. If you have a CTS700 device, it is a long road to get it supported by this integration, open an issue and we will go forward there
3. If you have a CTS602 device and you get a device not supported error during installation:
  - Turn on debug logging for the integration and try installing the integration again. Take note of the debug log and submit it with the issue.
  - Take a picture of the device type plate and submit it with the issue.
  - If you have HMI350T - Touch screen HMI - installed on your device, take a picture of the device info page and submit it with the issue.

## Support
If you like the integration, please leave a star and concider donating at https://www.buymeacoffee.com/veista

