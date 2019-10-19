import json
import os
from flask import Flask, request
from smartrent_python.client import Smartrent
from smartrent_python.devices.honeywell_thermostat import HoneywellThermostat

app = Flask(__name__)

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

client = Smartrent(username, password)
client.get_token()
client.get_hubs()

for hub in client.hubs.values():
    hub.get_devices()


def send_state_updates(request, state_updates):
    ''' Given a request and a dict of state updates, get the device, set the states, and commit.
    Return a message indicating success or error.
    '''
    hub_id = int(request.args.get('hub_id'))
    device_id = int(request.args.get('device_id'))

    hub = client.hubs.get(hub_id)

    if not hub:
        return 'Error: hub not found'

    device = hub.devices.get(device_id)

    if not device:
        return 'Error: device not found'

    for name, state in state_updates.items():
        device.set_state(name, state)

    device.commit()

    return 'ok'


@app.route('/cool/<temp>')
def cool(temp):
    state_updates = {'mode': 'cool', 'cooling_setpoint': temp}

    message = send_state_updates(request, state_updates)

    return json.dumps({'message': message})


@app.route('/heat/<temp>')
def heat(temp):
    state_updates = {'mode': 'heat', 'heating_setpoint': temp}

    message = send_state_updates(request, state_updates)

    return json.dumps({'message': message})


@app.route('/mode/<mode>')
def set_mode(mode):
    state_updates = {'mode': mode}

    message = send_state_updates(request, state_updates)

    return json.dumps({'message': message})


@app.route('/fan/<mode>')
def set_fan_mode(mode):
    state_updates = {'fan_mode': mode}

    message = send_state_updates(request, state_updates)

    return json.dumps({'message': message})
