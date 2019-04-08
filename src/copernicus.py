from datetime import datetime
from xml.etree import ElementTree
from pathlib import Path

import requests


class API:
    VERSION = '2.0.1'
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    TOKEN_URL = ('https://geoservices.regional.atmosphere.copernicus.eu/'
                 'services/GetAPIKey')
    DATA_URL = ('https://geoservices.regional.atmosphere.copernicus.eu/'
                'services/')

    SERVICES = {
        'ENSEMBLE-FORECAST': 'CAMS50-ENSEMBLE-FORECAST-01-EUROPE-WCS',
        'ENSEMBLE-ANALYSIS': 'CAMS50-ENSEMBLE-ANALYSIS-01-EUROPE-WCS',
    }
    SPECIES = {
        'CO': 'CO__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND',
        'NH3': 'NH3__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND',
        'NO': 'NO__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND',
        'NO2': 'NO2__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND',
        'O3': 'O3__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND',
    }
    LEVELS = (0, 50, 250, 500, 1000, 2000, 3000, 5000)
    AREAS = {
        'Ukraine': {
            'lat_min': 44.41886,
            'lat_max': 52.18903,
            'long_min': 22.20555,
            'long_max': 40.13222
        }
    }

    def __init__(self, email=None, password=None):
        if not all((email, password)):
            print('Please, provide credentials')
            email = input('Email: ')
            password = input('Password: ')

        self.token = self._get_token(email, password)

    def _get_token(self, email, password):
        payload = {'username': email, 'password': password}
        response = requests.get(self.TOKEN_URL, params=payload)

        if response.status_code != 200:
            raise ValueError(f'Wrong credentials: {response.content}')

        tree = ElementTree.fromstring(response.content)

        return tree.text

    def get_data(self, service, specie, validity_time,
                 level, area, run_base_time=None):
        # Validate params
        if service not in self.SERVICES:
            raise ValueError(
                f'"service" param should be one of {self.SERVICES.keys()}'
            )
        if specie not in self.SPECIES:
            raise ValueError(
                f'"specie" param should be one of {self.SPECIES.keys()}'
            )

        if 'FORECAST' in service and run_base_time is None:
            raise ValueError(
                f'"run_base_time" param should be set for FORECAST service'
            )
        elif 'ANALYSIS' in service and run_base_time:
            raise ValueError(
                f'"run_base_time" param should not be set for ANALYSIS service'
            )
        if run_base_time is not None:
            datetime.strptime(run_base_time, self.DATE_FORMAT)

        datetime.strptime(validity_time, self.DATE_FORMAT)

        if level not in self.LEVELS:
            raise ValueError(
                f'"specie" param should be one of {self.LEVELS}'
            )

        if area not in self.AREAS:
            raise ValueError(
                f'"area" param should be one of {self.AREAS}'
            )

        # Get data
        payload = (
            ('service', 'WCS'),
            ('token', self.token),
            ('request', 'GetCoverage'),
            ('version', self.VERSION),
            ('coverageId', f'{self.SPECIES[specie]}___'
                           f'{run_base_time or validity_time}'),
            ('subset', f'time({validity_time})'),
            ('subset', f'height({level})'),
            ('subset', (f'lat({self.AREAS[area]["lat_min"]},'
                        f'{self.AREAS[area]["lat_max"]})')),
            ('subset', (f'long({self.AREAS[area]["long_min"]},'
                        f'{self.AREAS[area]["long_max"]})')),
        )
        response = requests.get(
            f'{self.DATA_URL}{self.SERVICES[service]}', params=payload
        )
        if response.status_code == 200:
            file_name = (f'{service}_{specie}_{run_base_time}-{validity_time}_'
                         f'{level}_{area}.grib')
            path = Path('.')
            with open(path / 'data' / file_name, 'wb') as file_:
                file_.write(response.content)
            print(f'File saved: {file_name}')
        else:
            print('Something went wrong')
            print(response.content)
        return response
