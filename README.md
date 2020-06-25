# smartrent-python

This is a wrapper around the Smartrent home automation API.

- [Example](#example)
- [API](#api)

## Example

```python
> from smartrent_python.client import Smartrent

> client = Smartrent(username='natan', password='password')
> client.get_token()

# Now that we're authenticated, let's see which hubs we have access to
> client.get_hubs()
> client.hubs
[<Hub (123)>]

# Let's see which devices are linked to this hub
> hub = client.hubs[0]
> hub.get_devices()
> hub.devices
[<Honeywell Thermostat (12345)>, <Yale Door Lock (34567)>, <Zipato Water Sensor (56789)>]

# Let's interact with the thermostat - each device's settings are available in the devices directory
> thermostat = hub.devices[0]
> thermostat.set_state('mode', 'heat')
> thermostat.commit()
# Thermostat is now in heat mode

> thermostat.set_state('mode', 'cool')
> thermostat.set_state('cooling_setpoint', '72')
> thermostat.commit()
# Thermostat is now in cool mode and the cooling setpoint has been set to 72
```

## API

This repo also includes an example API that uses `smartrent-python` to interact with your smarthome devices. In order to run it, you should first try the example above to get a listing of your available hubs and devices. Once you know the IDs of the devices that you want to target, spin up the API by running:

```bash
FLASK_APP=api/index.py USERNAME=<smartrent username> PASSWORD=<smartrent password> flask run
```

From another shell, you'll be able to run
```bash
curl 'http://127.0.0.1:5000/cool/72?hub_id=<hub_id>&device_id=<device_id>'
```

I'd encourage you to customize this! You can take out the hub and device IDs as request parameters and instead hard code them into your API.

Once you have it ready to deploy, you can deploy the API to [Vercel](vercel.com). The included [vercel.json](./vercel.json) contains all the configuration you'll need.

```bash
> vercel
```
