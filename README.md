[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
# Nilan
Nilan integration for Home Assistant

Only CTS602/VP18C support at this time. If you have CTS700 or another device you will have to help me with that.

- Majority of functions are supported. If some critical is missing please leave an issue.

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

## Support
If you like the integration, please leave a star or concider donating at https://www.buymeacoffee.com/veista

