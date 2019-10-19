from mock import Mock
import pytest
from smartrent_python.client import Smartrent
from smartrent_python.device import DeviceValueException
from smartrent_python.devices.honeywell_thermostat import HoneywellThermostat


@pytest.fixture
def client():
    client = Smartrent(username=None, password=None)
    client.api = Mock()

    yield client


@pytest.fixture
def device(client):
    device = HoneywellThermostat(client, 1, 10, 'Honeywell Thermostat')

    yield device


def test_set_mode_to_off(client, device):
    device.set_state('mode', 'off')
    device.commit()

    assert client.api.patch.called
    assert client.api.patch.call_args[0][0] == 'hubs/1/devices/10'
    assert client.api.patch.call_args[0][1] == None
    assert client.api.patch.call_args[0][2]['attributes'] == [{'name': 'mode', 'state': 'off'}]


def test_set_fan_mode_to_on(client, device):
    device.set_state('fan_mode', 'on_low')
    device.commit()

    assert client.api.patch.called
    assert client.api.patch.call_args[0][0] == 'hubs/1/devices/10'
    assert client.api.patch.call_args[0][1] == None
    assert client.api.patch.call_args[0][2]['attributes'] == [{'name': 'fan_mode', 'state': 'on_low'}]


def test_set_cooling_setpoint(client, device):
    device.set_state('cooling_setpoint', '72')
    device.commit()

    assert client.api.patch.called
    assert client.api.patch.call_args[0][0] == 'hubs/1/devices/10'
    assert client.api.patch.call_args[0][1] == None
    assert client.api.patch.call_args[0][2]['attributes'] == [{'name': 'cooling_setpoint', 'state': '72'}]


def test_invalid_option_raises_exception(client, device):
    with pytest.raises(DeviceValueException):
        device.set_state('cooling_setpoint', 'on')
        device.commit()

    assert not device.client.api.patch.called
