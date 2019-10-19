''' Device implementation for Honeywell Thermostat. '''
from smartrent_python.device import create_device

SETTINGS = {
    'mode': ['cool', 'heat', 'off'],
    'fan_mode': ['on_low', 'auto_low'],
    'cooling_setpoint': [str(value) for value in range(30, 90)],
    'heating_setpoint': [str(value) for value in range(30, 90)],
}


HoneywellThermostat = create_device(SETTINGS)
