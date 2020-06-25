gimport logging
from smartrent_python.device import Device
from smartrent_python.devices.honeywell_thermostat import HoneywellThermostat
from smartrent_python.schemas.device import DeviceRawSchema, DeviceParsedSchema

DEVICE_NAME_TO_MODEL = {
    'Honeywell Thermostat': HoneywellThermostat,
}


class Hub:
    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.devices = []

    def get_devices(self):
        ''' Get a list of devices from the /hubs/{hub_id}/devices endpoint. '''
        devices = []
        response = self.client.api.get(f'hubs/{self.id}/devices', self.client.token)

        loaded_dicts = DeviceRawSchema().load(response, many=True)
        dumped_dicts = DeviceParsedSchema().dump(loaded_dicts, many=True)

        for device_dict in dumped_dicts:
            if device_dict['name'] in DEVICE_NAME_TO_MODEL:
                device_model = DEVICE_NAME_TO_MODEL[device_dict['name']]
            else:
                logging.warning('Unknown device: %s', device_dict['name'])
                device_model = Device

            device = device_model(client=self.client, hub_id=self.id, **device_dict)
            devices.append(device)

        self.devices = {device.id: device for device in devices}

    def __repr__(self):
        return f'Hub ({self.id})'
