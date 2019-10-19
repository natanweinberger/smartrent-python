''' Tests for the Smartrent client. '''
from datetime import datetime
import json
from mock import Mock
import pytest
import requests
from smartrent_python.client import Smartrent


@pytest.fixture(scope='function')
def client():
    client = Smartrent('username', 'password')
    client.api = Mock()

    return client


TOKEN_RESPONSE = {
    "data": {
        "access_token": "test",
        "expires": 1571512912,  # 2019-10-19 15:21:52 EDT
        "refresh_token": "test",
        "user_id":3172
    }
}

def test_get_token_using_credentials(client):
    ''' The client method `_get_token_using_credentials` should:
    - make a post request to the /sessions endpoint
    - send the username and password in the payload
    - return a dictionary containing the JSON response
    '''
    client.api.post.return_value = TOKEN_RESPONSE

    ret = client._get_token_using_credentials()

    # There should have been a call to /sessions with the username and password as the payload
    assert client.api.post.called is True
    assert client.api.post.call_args[0][0] == 'sessions'
    assert client.api.post.call_args[1]['data'] == {'username': 'username', 'password': 'password'}
    assert ret == TOKEN_RESPONSE


def test_get_token_using_refresh_token(client):
    ''' The client method `_get_token_using_refresh_token` should:
    - make a post request to the /tokens endpoint
    - send the refresh token in the header
    - return a dictionary containing the JSON response
    '''
    client.api.post.return_value = TOKEN_RESPONSE

    client.refresh_token = 'test_refresh_token'
    ret = client._get_token_using_refresh_token()

    # There should have been a call to /tokens with the refresh token as a header
    assert client.api.post.called is True
    assert client.api.post.call_args[0][0] == 'tokens'
    assert client.api.post.call_args[1]['headers'] == {'authorization-x-refresh': 'test_refresh_token'}
    assert ret == TOKEN_RESPONSE


def test_get_token_makes_appropriate_call_with_credentials(client):
    ''' When no refresh_token is present, `get_token` should call `_get_token_using_credentials`.
    The new token, refresh_token, and expiry timestamp should be copied into the instance.
    '''
    client._get_token_using_credentials = Mock()
    client._get_token_using_credentials.return_value = TOKEN_RESPONSE

    client.get_token()  # this should make a call to `_get_token_using_credentials`

    assert client._get_token_using_credentials.called

    # The returned JSON response should have been parsed and stored
    assert client.token == TOKEN_RESPONSE['data']['access_token']
    assert client.refresh_token == TOKEN_RESPONSE['data']['refresh_token']
    assert client.token_expire_timestamp == datetime.fromtimestamp(TOKEN_RESPONSE['data']['expires'])
    assert client.token_expire_timestamp == datetime(2019, 10, 19, 19, 21, 52)


def test_get_token_makes_appropriate_call_with_refresh_token(client):
    ''' When a refresh_token is present, `get_token` should call `_get_token_using_refresh_token`.
    The new token, refresh_token, and expiry timestamp should be copied into the instance.
    '''
    client._get_token_using_refresh_token = Mock()
    client._get_token_using_refresh_token.return_value = TOKEN_RESPONSE
    client.refresh_token = 'test_refresh_token'  # populate refresh_token

    client.get_token()  # this should make a call to `_get_token_using_refresh_token`

    assert client._get_token_using_refresh_token.called

    # The returned JSON response should have been parsed and stored
    assert client.token == TOKEN_RESPONSE['data']['access_token']
    assert client.refresh_token == TOKEN_RESPONSE['data']['refresh_token']
    assert client.token_expire_timestamp == datetime.fromtimestamp(TOKEN_RESPONSE['data']['expires'])
    assert client.token_expire_timestamp == datetime(2019, 10, 19, 19, 21, 52)

