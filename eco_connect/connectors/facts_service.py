from collections import namedtuple
import os

import pandas as pd


from eco_connect.src.credentials_factory import CredentialsFactory
from eco_connect.src.base_request import BaseRequest
from eco_connect.src.result_parser import RequestParser
from eco_connect.src.errors import ResultParserError


class FactsService(BaseRequest):

    def __init__(self, environment_name='prod', version='v1'):
        self.env = self._validate_env(environment_name=environment_name)
        self.hostname = f'https://facts.{self.env}.ecorithm.com/api/{version}/'
        self._get_credentials()

    def _validate_env(self, environment_name):
        environment_name = environment_name.lower()
        if environment_name in ['prod', 'qa']:
            return environment_name
        else:
            raise ValueError(f'`{environment_name}` is invalid!')

    def _get_credentials(self):
        if not hasattr(self, 'credentials'):
            self.credentials = CredentialsFactory().get_eco_credentials()

    def get_facts(self,
                  building_id,
                  start_date,
                  end_date,
                  start_hour='00:00',
                  end_hour='23:55',
                  equipment_names=[],
                  equipment_types=[],
                  point_classes=[],
                  eco_point_ids=[],
                  display_names=[],
                  native_names=[],
                  point_class_expression=[],
                  native_name_expression=[],
                  display_name_expression=[],
                  result_format='pandas',
                  download_folder=os.path.expanduser('~') + '/downloads/',
                  file_name='data.csv'):

        url = self.hostname + f'building/{building_id}/facts'

        data = {
            'start_date': start_date,
            'end_date': end_date,
            'start_hour': start_hour,
            'end_hour': end_hour,
            'eco_point_ids': eco_point_ids,
            'equipment_names': equipment_names,
            'equipment_types': equipment_types,
            'point_classes': point_classes,
            'display_names': display_names,
            'native_names': native_names,
            'point_class_expression': point_class_expression,
            'display_name_expression': display_name_expression,
            'native_name_expression': native_name_expression}

        if result_format.lower() == 'pandas':
            parser_args = {}
            fact_parser = self._pandas_fact_parser
        elif result_format.lower() == 'json':
            fact_parser = RequestParser.raw_parser
            parser_args = {}
        elif result_format.lower() == 'tuple':
            fact_parser = self._tuple_fact_parser
            parser_args = {}
        elif result_format.lower() == 'csv':
            fact_parser = self._csv_fact_parser
            parser_args = {'download_folder': download_folder,
                           'file_name': file_name}
        else:
            raise ValueError(f'{fact_parser} is not valid!')

        response = self.post(url, data=data, auth=self.credentials)

        return self._format_result(response, fact_parser, parser_args)

    def _tuples_fact_parser(self, response):
        result = response.json()
        try:
            result = response.json()
        except (ValueError):
            raise ResultParserError('Unable to parse the response.',
                                    response.text)

        try:
            result = result['data']
        except KeyError:
            raise ResultParserError('Unable to parse the response.',
                                    result)

        tuple_names = list(result[0].values()['data'].keys()) +\
            list(result[0].values()['meta'].keys())

        response_tuple = namedtuple('response_tuple', tuple_names)
        parsed_result = []
        for dpoint_id, data in result.items():
            meta = data['meta']
            fact_data = data['data']
            for fact in fact_data:
                row = {'datetime': fact.keys(), 'fact_value': fact.values()}
                row.update(meta)
                parsed_result.append(response_tuple(**row))
        return parsed_result

    def _pandas_fact_parser(self, response):
        tuple_response = self._tuples_fact_parser(response)
        return pd.DataFrame(tuple_response)

    def _csv_fact_parser(cls, response,
                         download_folder,
                         file_name):
        result_df = cls._pandas_fact_parser(response)
        os.makedirs(download_folder, exist_ok=True)
        result_df.to_csv(file_name, index=None)
        return result_df
