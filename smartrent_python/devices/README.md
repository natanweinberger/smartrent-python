# Devices

The devices in this directory are implementations of the generic [Device](../device.py) class.

To create a new device, add a file and use the following template from [Honeywell Thermostat](./honeywell_thermostat.py).

```python
''' Device implementation for Honeywell Thermostat. '''
from smartrent_python.device import create_device

SETTINGS = {
    'mode': ['cool', 'heat', 'off'],
    'fan_mode': ['on_low', 'auto_low'],
    'cooling_setpoint': [str(value) for value in range(30, 90)],
    'heating_setpoint': [str(value) for value in range(30, 90)],
}


HoneywellThermostat = create_device(SETTINGS)

```
