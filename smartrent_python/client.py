''' Access the Smartrent API. '''
from datetime import datetime
import logging
import os
from smartrent_python.api import SmartrentAPI
from smartrent_python.hub import Hub
from smartrent_python.schemas.hub import HubRawSchema, HubParsedSchema

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Smartrent:
    def __init__(self, username, password):
        self.api = SmartrentAPI()

        self.username = username
        self.password = password

        self.token = None
        self.refresh_token = None
        self.token_expire_timestamp = None

        self.hubs = {}
        

    def _get_token_using_credentials(self):
        ''' Retrieve a token by authenticating with username and password. '''
        logging.info('Retrieving token using credentials')
        path = 'sessions'
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.api.post(path, data=data, api_version='v1')

        return response


    def _get_token_using_refresh_token(self):
        ''' Retrieve a token using a refresh token. '''
        logging.info('Retrieving token using refresh token')
        path = 'tokens'
        headers = {
            'authorization-x-refresh': self.refresh_token
        }

        response = self.api.post(path, headers=headers, api_version='v1')

        return response


    def get_token(self):
        ''' Get a token. Use the refresh_token if available, fall back to username and password authentication if not.
        After retrieving the response, copy the new token, refresh_token, and expiry timestamp into the instance.
        '''
        if self.refresh_token:
            response = self._get_token_using_refresh_token()

        else:
            response = self._get_token_using_credentials()

        self.token = response['data']['access_token']
        self.refresh_token = response['data']['refresh_token']
        self.token_expire_timestamp = datetime.fromtimestamp(response['data']['expires'])


    def get_hubs(self):
        ''' Get a list of hubs from the /hubs endpoint. '''
        hubs = []
        response = self.api.get('hubs', self.token)
        loaded_hubs = HubRawSchema().load(response, many=True)
        dumped_hubs = HubParsedSchema().dump(loaded_hubs, many=True)
        hubs = [Hub(self, **hub) for hub in dumped_hubs]

        self.hubs = {hub.id: hub for hub in hubs}


    def __repr__(self):
        return f'''
        <Smartrent
        username={self.username}
        password={self.password}
        token={self.token}
        refresh_token={self.refresh_token}
        token_expire_timestamp={self.token_expire_timestamp}
        >
        '''
