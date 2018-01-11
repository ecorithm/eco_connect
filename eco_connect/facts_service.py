from eco_connect.credentials_factory import CredentialsFactory

from eco_connect.base_request import BaseRequest
from eco_connect.result_parser import RequestParser


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
                  result_format='pandas'):

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
            fact_parser = self._pandas_fact_parser
        elif result_format.lower() == 'json':
            fact_parser = RequestParser.raw_parser
        elif result_format.lower() == 'tuple':
            fact_parser = self._tuple_fact_parser
        elif result_format.lower() == 'csv':
            fact_parser = self._csv_fact_parser
        else:
            raise ValueError(f'{fact_parser} is not valid!')

        result = self.post(url, data=data, auth=self.credentials)

        return self._format_result(result, fact_parser)
