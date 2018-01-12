from collections import namedtuple
from operator import attrgetter
import os

import pandas as pd


from eco_connect.src.base_request import BaseRequest
from eco_connect.src.request_parser import RequestParser
from eco_connect.src.errors import RequestParserError


class FactsService(BaseRequest):

    def __init__(self, environment_name='prod', version='v1'):
        self.env = self._validate_env(environment_name=environment_name)
        self.hostname = f'https://facts.{self.env}.ecorithm.com/api/{version}/'
        super().__init__()

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
                  file_name='facts.csv'):

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
            fact_parser = RequestParser.json_parser
            parser_args = {}
        elif result_format.lower() == 'tuple':
            fact_parser = self._tuple_fact_parser
            parser_args = {}
        elif result_format.lower() == 'csv':
            fact_parser = self._csv_fact_parser
            parser_args = {'download_folder': download_folder,
                           'file_name': file_name}
        else:
            raise ValueError(f'{result_format} is not valid!')

        response = self.post(url, data=data)

        return self._format_response(response, fact_parser, parser_args)

    def _tuple_fact_parser(self, response):
        try:
            result = response.json()
        except (ValueError):
            raise RequestParserError('Unable to parse the response.',
                                     response.text)

        result = result['data']

        tuple_names = ['fact_time', 'fact_value'] +\
            list(list(result.values())[0]['meta'].keys())

        response_tuple = namedtuple('response_tuple', tuple_names)
        parsed_result = []
        for dpoint_id, data in result.items():
            meta = data['meta']
            fact_data = data['data']
            for fact_time, fact_value in fact_data.items():
                row = {'fact_time': fact_time, 'fact_value': fact_value}
                row.update(meta)
                parsed_result.append(response_tuple(**row))
        return sorted(parsed_result, key=attrgetter('eco_point_id'))

    def _pandas_fact_parser(self, response):
        tuple_response = self._tuple_fact_parser(response)
        return pd.DataFrame(tuple_response)

    def _csv_fact_parser(self, response,
                         download_folder,
                         file_name):
        result_df = self._pandas_fact_parser(response)
        try:
            os.makedirs(download_folder, exist_ok=True)
        except OSError:
            raise ValueError(f'{download_folder} is not a valid folder path!')
        result_df.to_csv(download_folder + file_name, index=None)
        return result_df.to_csv

    def put_facts(self, building_id, data):
        url = self.hostname + f'building/{building_id}/facts'
        input_data = list(data.T.to_dict().values())
        return self.put(url, data=input_data,
                        encode_type='json')

    def get_avg_facts(cls):
        raise NotImplementedError()

    def get_buildings(self, building_id=None,
                      is_active=True, result_format='pandas',
                      download_folder=os.path.expanduser('~') + '/downloads/',
                      file_name='building.csv'):
        url = self.hostname + f'buildings'
        params = {'building_id': building_id, 'is_active': is_active}
        reponse = self.get(url, data=params)
        parser = self._get_parser(result_format, data_key='data',
                                  download_folder=download_folder,
                                  file_name=file_name)

        parsed_result = self._format_response(reponse,
                                              **parser)
        return parsed_result

    def put_building(cls):
        raise NotImplementedError()

    def delete_building(cls):
        raise NotImplementedError()

    def get_point_classes(self, point_class=None,
                          is_active=True, result_format='pandas',
                          download_folder=(os.path.expanduser('~') +
                                           '/downloads/'),
                          file_name='point-classes.csv'):
        url = self.hostname + f'point-classes'
        params = {'point_class': point_class, 'is_active': is_active}
        reponse = self.get(url, data=params)
        parser = self._get_parser(result_format, data_key='data',
                                  download_folder=download_folder,
                                  file_name=file_name)

        parsed_result = self._format_response(reponse,
                                              **parser)
        return parsed_result

    def put_point_class(cls):
        raise NotImplementedError()

    def delete_point_class(cls):
        raise NotImplementedError()

    def get_point_mapping(self,
                          building_id,
                          equipment_names=[],
                          equipment_types=[],
                          point_classes=[],
                          eco_point_ids=[],
                          display_names=[],
                          native_names=[],
                          point_class_expression=[],
                          native_name_expression=[],
                          display_name_expression=[],
                          is_active=True,
                          result_format='pandas',
                          download_folder=(os.path.expanduser('~') +
                                           '/downloads/'),
                          file_name='point-mapping.csv'):
        url = self.hostname + f'building/{building_id}/point-mapping'
        data = {
            'is_active': is_active,
            'eco_point_ids': eco_point_ids,
            'equipment_names': equipment_names,
            'equipment_types': equipment_types,
            'point_classes': point_classes,
            'display_names': display_names,
            'native_names': native_names,
            'point_class_expression': point_class_expression,
            'display_name_expression': display_name_expression,
            'native_name_expression': native_name_expression}
        reponse = self.get(url, data=data)
        parser = self._get_parser(result_format, data_key='data',
                                  download_folder=download_folder,
                                  file_name=file_name)

        parsed_result = self._format_response(reponse,
                                              **parser)
        return parsed_result

    def delete_point_mapping(cls):
        raise NotImplementedError()

    def put_point_mapping(cls):
        raise NotImplementedError()

    def get_equipment_types(self, equipment_type=None,
                            is_active=True, result_format='pandas',
                            download_folder=(os.path.expanduser('~') +
                                             '/downloads/'),
                            file_name='equipment_types.csv'):
        url = self.hostname + f'equipment-types'
        params = {'equipment_type': equipment_type, 'is_active': is_active}
        reponse = self.get(url, data=params)
        parser = self._get_parser(result_format, data_key='data',
                                  download_folder=download_folder,
                                  file_name=file_name)

        parsed_result = self._format_response(reponse,
                                              **parser)
        return parsed_result

    def delete_equipment_type(cls):
        raise NotImplementedError()

    def put_equipment_type(cls):
        raise NotImplementedError()

    def get_equipment(self, building_id, equipment_name=None,
                      equipment_type=None,
                      is_active=True, result_format='pandas',
                      download_folder=os.path.expanduser('~') + '/downloads/',
                      file_name='equipment.csv'):
        url = self.hostname + f'building/{building_id}/equipment'
        params = {'equipment_type': equipment_type,
                  'is_active': is_active,
                  'equipment_name': equipment_name}
        reponse = self.get(url, data=params)
        parser = self._get_parser(result_format, data_key='data',
                                  download_folder=download_folder,
                                  file_name=file_name)

        parsed_result = self._format_response(reponse,
                                              **parser)
        return parsed_result

    def delete_equipment(cls):
        raise NotImplementedError()

    def put_equipment(cls):
        raise NotImplementedError()

    def get_native_names(self, building_id,
                         native_name=None,
                         is_active=True, result_format='pandas',
                         download_folder=(os.path.expanduser('~') +
                                          '/downloads/'),
                         file_name='native_names.csv'):
        url = self.hostname + f'building/{building_id}/native-names'
        params = {'native_name': native_name,
                  'is_active': is_active}
        reponse = self.get(url, data=params)
        parser = self._get_parser(result_format, data_key='data',
                                  download_folder=download_folder,
                                  file_name=file_name)

        parsed_result = self._format_response(reponse,
                                              **parser)
        return parsed_result

    def put_native_names(cls):
        raise NotImplementedError()

    def delete_native_names(cls):
        raise NotImplementedError()

    def get_native_names_history(cls):
        raise NotImplementedError()

    def get_unamapped_native_names(cls):
        raise NotImplementedError()

    def get_etl_process_history(cls):
        raise NotImplementedError()

    def get_unstored_native_names(cls):
        raise NotImplementedError()

    def get_building_dqi(cls):
        raise NotImplementedError()
