# smartrent-python

This is a wrapper around the Smartrent home automation API.

## Example

```python
> from smartrent_python.client import Smartrent

> client = Smartrent(username='natan', password='password')
> client.get_token()

# Now that we're authenticated, let's see which hubs we have access to
> client.get_hubs()
> client.hubs
[<Hub>]

# Let's see which devices are linked to this hub
> hub = client.hubs[0]
> hub.get_devices()
> hub.devices
[<Honeywell Thermostat>, <Yale Door Lock>, <Zipato Water Sensor>]

# Let's interact with the thermostat - each device's settings are available in the devices directory
> thermostat = hub.devices[0]
> thermostat.set_state('mode', 'heat')
> thermostat.commit()
# Thermostat is now in heat mode

> thermostat.set_state('mode', 'cool')
> thermostat.set_state('cooling_setpoint', '72')
> thermostat.commit()
# Thermostat is now in cool mode and the cooling setpoint has been set to 72
