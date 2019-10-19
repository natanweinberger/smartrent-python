''' Make HTTP requests to the Smartrent API. '''
from datetime import datetime
import logging
import os
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class SmartrentAPI:
    BASE_URLS = {
        'v1': 'https://control.smartrent.com/api/v1',
        'v2': 'https://control.smartrent.com/api/v2',
    }
    USER_AGENT = 'SmartRent/2.3.2 (com.smartrent.resident; build:2; iOS 12.4.1) Alamofire/4.6.0'


    def post(self, path, data={}, headers={}, api_version='v2'):
        ''' Make a POST request to the Smartrent API. '''
        default_headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': self.USER_AGENT,
        }
        headers = {**default_headers, **headers}  # default_headers will be overwritten if there is a collision

        url = os.path.join(self.BASE_URLS[api_version], path)
        response = requests.post(url,
                                 headers=headers,
                                 data=data)

        return response.json()


    def get(self, path, token, headers={}, api_version='v2'):
        ''' Make a GET request to the Smartrent API. '''
        default_headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip;q=1.0, compress;q=0.5',
            'accept-language': 'en-US;q=1.0, fr-CA;q=0.9',
            'user-agent': self.USER_AGENT,
            'authorization': f'Bearer {token}',
        }
        headers = {**default_headers, **headers}  # default_headers will be overwritten if there is a collision

        url = os.path.join(self.BASE_URLS[api_version], path)
        response = requests.get(url,
                                headers=headers)

        return response.json()


    def patch(self, path, token, data={}, headers={}, api_version='v2'):
        ''' Make a PATCH request to the Smartrent API. '''
        default_headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip;q=1.0, compress;q=0.5',
            'accept-language': 'en-US;q=1.0, fr-CA;q=0.9',
            'content-type': 'application/json',
            'user-agent': self.USER_AGENT,
            'authorization': f'Bearer {token}',
        }
        headers = {**default_headers, **headers}  # default_headers will be overwritten if there is a collision

        url = os.path.join(self.BASE_URLS[api_version], path)
        response = requests.patch(url,
                                  headers=headers,
                                  json=data)

        return response.json()
