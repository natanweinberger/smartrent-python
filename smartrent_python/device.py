''' Generic device class.
Example implmentation of a device:

SETTINGS = {
    'mode': ['on', 'off'],
}

'''
class DeviceValueException(Exception):
    pass


class Device:
    def __init__(self, client, hub_id, id, name, settings=None):
        '''
        :param Smartrent client:
        :param int hub_id: ID of the corresponding Hub
        :param int id: Device ID
        :param str name: Device name
        '''
        self.client = client
        self.hub_id = hub_id
        self.id = id
        self.name = name
        self.settings = settings or {}

        self.pending_states = {}

    def set_state(self, name, state):
        if state not in self.settings[name]:
            raise DeviceValueException(f'{state} is not a valid state for {name}')

        self.pending_states[name] = state

    def generate_actions(self):
        ''' Create a list of attributes and desired states that the API can parse. '''
        actions = [{'name': key, 'state': value} for key, value in self.pending_states.items()]
        self.pending_states = {}

        return actions

    def commit(self):
        ''' Send a patch request to apply the pending states using the client. '''
        actions = self.generate_actions()
        data = {'attributes': actions}

        path = f'hubs/{self.hub_id}/devices/{self.id}'
        self.client.api.patch(path, self.client.token, data)

    def __repr__(self):
        return f'{self.name} ({self.id})'


def create_device(settings):
    ''' Pre-populate a Device with settings.
    :param dict settings: Each key is an attribute of a device, each value is an iterable of acceptable values

    Example:
        fan = create_device({'mode': ['on', 'off']})
    '''
    def _create_device(*args, **kwargs):
        return Device(*args, **kwargs, settings=settings)

    return _create_device
