from collections import namedtuple

import pytest
import pandas as pd

from eco_connect import FactsService
from eco_connect.src.errors import RequestParserError


class TestFactsService:
    MODULE_PATH = 'eco_connect.facts_service'
    CLASS_PATH = MODULE_PATH + '.FactsService'\


    @pytest.fixture
    def facts_service(self, mocker):
        facts_service = FactsService()
        facts_service.credentials = ('user', 'password')
        return facts_service

    def test__validate_env(self, mocker, facts_service):
        environment_name = 'PROD'
        result = facts_service._validate_env(environment_name)
        assert result == 'prod'

    def test__validate_env_fail(self, mocker, facts_service):
        environment_name = 'production'
        with pytest.raises(ValueError):
            facts_service._validate_env(environment_name)

    def test__init__(self, mocker):
        _validate_env = mocker.patch(self.CLASS_PATH + '._validate_env')
        _validate_env.return_value = 'prod'
        _get_credentials = mocker.patch(self.CLASS_PATH + '._set_credentials')

        facts_service = FactsService()
        assert facts_service.env == 'prod'
        assert facts_service.hostname == ('https://facts.prod.ecorithm.com'
                                          '/api/v1/')
        _validate_env.assert_called_once_with(environment_name='prod')
        _get_credentials.assert_called_once()

    def test_get_facts_json(self, mocker, facts_service):
        building_id = 1
        start_date = '2017-12-01 00:00'
        end_date = '2017-12-10 00:00'
        start_hour = '00:00'
        end_hour = '23:55'
        equipment_names = ['VAV_01']
        equipment_types = ['VAV']
        point_classes = ['SpaceAirTemperature']
        eco_point_ids = [1, 2]
        display_names = ['SpaceTemp']
        native_names = ['Native-Name-1']
        point_class_expression = ['VAV.* .*']
        native_name_expression = ['VAV.*']
        display_name_expression = ['AHU.* .*']
        result_format = 'json'

        expected_parser = mocker.patch(self.MODULE_PATH +
                                       '.RequestParser.json_parser')

        mock_response = mocker.Mock()
        mock_post = mocker.patch.object(facts_service, 'post',
                                        return_value=mock_response)

        mock_format_result = mocker.patch.object(facts_service,
                                                 '_format_response')

        mock_format_result.return_value = 'parsed_result'

        result = facts_service.get_facts(building_id,
                                         start_date,
                                         end_date,
                                         start_hour,
                                         end_hour,
                                         equipment_names,
                                         equipment_types,
                                         point_classes,
                                         eco_point_ids,
                                         display_names,
                                         native_names,
                                         point_class_expression,
                                         native_name_expression,
                                         display_name_expression,
                                         result_format=result_format)
        assert result == 'parsed_result'
        mock_format_result.assert_called_with(mock_response,
                                              expected_parser, {})
        mock_post.assert_called_with('https://facts.prod.ecorithm.com/api/v1/'
                                     'building/1/facts',
                                     data={'start_date': start_date,
                                           'end_date': end_date,
                                           'start_hour': start_hour,
                                           'end_hour': end_hour,
                                           'eco_point_ids': eco_point_ids,
                                           'equipment_names': equipment_names,
                                           'equipment_types': equipment_types,
                                           'point_classes': point_classes,
                                           'display_names': display_names,
                                           'native_names': native_names,
                                           'point_class_expression':
                                           point_class_expression,
                                           'display_name_expression':
                                           display_name_expression,
                                           'native_name_expression':
                                           native_name_expression})

    def test_get_facts_pandas(self, mocker, facts_service):
        building_id = 1
        start_date = '2017-12-01 00:00'
        end_date = '2017-12-10 00:00'
        start_hour = '00:00'
        end_hour = '23:55'
        equipment_names = ['VAV_01']
        equipment_types = ['VAV']
        point_classes = ['SpaceAirTemperature']
        eco_point_ids = [1, 2]
        display_names = ['SpaceTemp']
        native_names = ['Native-Name-1']
        point_class_expression = ['VAV.* .*']
        native_name_expression = ['VAV.*']
        display_name_expression = ['AHU.* .*']
        result_format = 'pandas'

        expected_parser = mocker.patch.object(facts_service,
                                              '_pandas_fact_parser')

        mock_response = mocker.Mock()
        mock_post = mocker.patch.object(facts_service, 'post',
                                        return_value=mock_response)

        mock_format_result = mocker.patch.object(facts_service,
                                                 '_format_response')

        mock_format_result.return_value = 'parsed_result'

        result = facts_service.get_facts(building_id,
                                         start_date,
                                         end_date,
                                         start_hour,
                                         end_hour,
                                         equipment_names,
                                         equipment_types,
                                         point_classes,
                                         eco_point_ids,
                                         display_names,
                                         native_names,
                                         point_class_expression,
                                         native_name_expression,
                                         display_name_expression,
                                         result_format=result_format)
        assert result == 'parsed_result'
        mock_format_result.assert_called_with(mock_response,
                                              expected_parser,
                                              {'data_key': 'data'})
        mock_post.assert_called_with('https://facts.prod.ecorithm.com/api/v1/'
                                     'building/1/facts',
                                     data={'start_date': start_date,
                                           'end_date': end_date,
                                           'start_hour': start_hour,
                                           'end_hour': end_hour,
                                           'eco_point_ids': eco_point_ids,
                                           'equipment_names': equipment_names,
                                           'equipment_types': equipment_types,
                                           'point_classes': point_classes,
                                           'display_names': display_names,
                                           'native_names': native_names,
                                           'point_class_expression':
                                           point_class_expression,
                                           'display_name_expression':
                                           display_name_expression,
                                           'native_name_expression':
                                           native_name_expression})

    def test_get_facts_tuple(self, mocker, facts_service):
        building_id = 1
        start_date = '2017-12-01 00:00'
        end_date = '2017-12-10 00:00'
        start_hour = '00:00'
        end_hour = '23:55'
        equipment_names = ['VAV_01']
        equipment_types = ['VAV']
        point_classes = ['SpaceAirTemperature']
        eco_point_ids = [1, 2]
        display_names = ['SpaceTemp']
        native_names = ['Native-Name-1']
        point_class_expression = ['VAV.* .*']
        native_name_expression = ['VAV.*']
        display_name_expression = ['AHU.* .*']
        result_format = 'tuple'

        expected_parser = mocker.patch.object(facts_service,
                                              '_tuple_fact_parser')

        mock_response = mocker.Mock()
        mock_post = mocker.patch.object(facts_service, 'post',
                                        return_value=mock_response)

        mock_format_result = mocker.patch.object(facts_service,
                                                 '_format_response')

        mock_format_result.return_value = 'parsed_result'

        result = facts_service.get_facts(building_id,
                                         start_date,
                                         end_date,
                                         start_hour,
                                         end_hour,
                                         equipment_names,
                                         equipment_types,
                                         point_classes,
                                         eco_point_ids,
                                         display_names,
                                         native_names,
                                         point_class_expression,
                                         native_name_expression,
                                         display_name_expression,
                                         result_format=result_format)
        assert result == 'parsed_result'
        mock_format_result.assert_called_with(mock_response,
                                              expected_parser,
                                              {'data_key': 'data'})
        mock_post.assert_called_with('https://facts.prod.ecorithm.com/api/v1/'
                                     'building/1/facts',
                                     data={'start_date': start_date,
                                           'end_date': end_date,
                                           'start_hour': start_hour,
                                           'end_hour': end_hour,
                                           'eco_point_ids': eco_point_ids,
                                           'equipment_names': equipment_names,
                                           'equipment_types': equipment_types,
                                           'point_classes': point_classes,
                                           'display_names': display_names,
                                           'native_names': native_names,
                                           'point_class_expression':
                                           point_class_expression,
                                           'display_name_expression':
                                           display_name_expression,
                                           'native_name_expression':
                                           native_name_expression})

    def test_get_facts_csv(self, mocker, facts_service):
        building_id = 1
        start_date = '2017-12-01 00:00'
        end_date = '2017-12-10 00:00'
        start_hour = '00:00'
        end_hour = '23:55'
        equipment_names = ['VAV_01']
        equipment_types = ['VAV']
        point_classes = ['SpaceAirTemperature']
        eco_point_ids = [1, 2]
        display_names = ['SpaceTemp']
        native_names = ['Native-Name-1']
        point_class_expression = ['VAV.* .*']
        native_name_expression = ['VAV.*']
        display_name_expression = ['AHU.* .*']
        result_format = 'csv'

        expected_parser = mocker.patch.object(facts_service,
                                              '_csv_fact_parser')

        mock_response = mocker.Mock()
        mock_post = mocker.patch.object(facts_service, 'post',
                                        return_value=mock_response)

        mock_format_result = mocker.patch.object(facts_service,
                                                 '_format_response')

        mock_format_result.return_value = 'parsed_result'

        result = facts_service.get_facts(building_id,
                                         start_date,
                                         end_date,
                                         start_hour,
                                         end_hour,
                                         equipment_names,
                                         equipment_types,
                                         point_classes,
                                         eco_point_ids,
                                         display_names,
                                         native_names,
                                         point_class_expression,
                                         native_name_expression,
                                         display_name_expression,
                                         result_format=result_format)
        assert result == 'parsed_result'
        mock_format_result.assert_called_with(mock_response,
                                              expected_parser,
                                              {'data_key': 'data'})
        mock_post.assert_called_with('https://facts.prod.ecorithm.com/api/v1/'
                                     'building/1/facts',
                                     data={'start_date': start_date,
                                           'end_date': end_date,
                                           'start_hour': start_hour,
                                           'end_hour': end_hour,
                                           'eco_point_ids': eco_point_ids,
                                           'equipment_names': equipment_names,
                                           'equipment_types': equipment_types,
                                           'point_classes': point_classes,
                                           'display_names': display_names,
                                           'native_names': native_names,
                                           'point_class_expression':
                                           point_class_expression,
                                           'display_name_expression':
                                           display_name_expression,
                                           'native_name_expression':
                                           native_name_expression})

    def test_get_facts_value_error(self, mocker, facts_service):
        building_id = 1
        start_date = '2017-12-01 00:00'
        end_date = '2017-12-10 00:00'
        with pytest.raises(ValueError):
            facts_service.get_facts(building_id,
                                    start_date,
                                    end_date,
                                    result_format='arrow')

    def test__tuple_fact_parser(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"data": {
                                           "1": {
                                               "data": {
                                                   "2017-08-01 00:00": 67.5,
                                                   "2017-08-01 00:05": 68.5},
                                               "meta": {
                                                   "display_name": "SpaceTemp",
                                                   "eco_point_id": 1,
                                                   "native_name":
                                                   "UCSB/275/VAV_301/"
                                                   "NAE11/N2-2.275-VAV-"
                                                   "301.ZN-T",
                                                   "equipment": "VAV-301",
                                                   "equipment_type": "VAV",
                                                   "point_class":
                                                   "SpaceAirTemperature"}},
                                           "2": {
                                               "data": {
                                                   "2017-08-01 00:00": 0,
                                                   "2017-08-01 00:05": 100},
                                               "meta": {
                                                   "display_name": "Cooling",
                                                   "eco_point_id": 2,
                                                   "native_name":
                                                   "UCSB/275/VAV_301/"
                                                   "NAE11/N2-2.275-VAV-301.CV",
                                                   "equipment": "VAV_301",
                                                   "equipment_type": "VAV",
                                                   "point_class":
                                                   "CoolingCoilUnitFeedback"}}
                                           }}
        tuple_names = ['fact_time', 'fact_value', 'display_name',
                       'eco_point_id',
                       'native_name', 'equipment', 'equipment_type',
                       'point_class']
        expected_named_tuple = namedtuple('response_tuple', tuple_names)

        expected_result = [
            expected_named_tuple(**{
                "display_name": "SpaceTemp",
                "eco_point_id": 1,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.ZN-T",
                "equipment": "VAV-301",
                "equipment_type": "VAV",
                "point_class":
                "SpaceAirTemperature"}, **{'fact_time': "2017-08-01 00:00",
                                           'fact_value': 67.5}),

            expected_named_tuple(**{
                "display_name": "SpaceTemp",
                "eco_point_id": 1,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.ZN-T",
                "equipment": "VAV-301",
                "equipment_type": "VAV",
                "point_class":
                "SpaceAirTemperature"}, **{'fact_time': "2017-08-01 00:05",
                                           'fact_value': 68.5}),

            expected_named_tuple(**{
                "display_name": "Cooling",
                "eco_point_id": 2,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.CV",
                "equipment": "VAV_301",
                "equipment_type": "VAV",
                "point_class": "CoolingCoilUnit"
                "Feedback"}, **{'fact_time': "2017-08-01 00:00",
                                'fact_value': 0}),

            expected_named_tuple(**{
                "display_name": "Cooling",
                "eco_point_id": 2,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.CV",
                "equipment": "VAV_301",
                "equipment_type": "VAV",
                "point_class": "CoolingCoilUnit"
                "Feedback"}, **{'fact_time': "2017-08-01 00:05",
                                'fact_value': 100})]
        result = facts_service._tuple_fact_parser(mock_response)
        assert len(result) == len(expected_result)
        assert result[0] == expected_result[0]

    def test__tuple_fact_parser_bad_json(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_response.json.side_effect = ValueError
        with pytest.raises(RequestParserError):
            facts_service._tuple_fact_parser(mock_response)

    def test__pandas_fact_parser(self, mocker, facts_service):
        mock__tuples_fact_parser = mocker.patch.object(facts_service,
                                                       '_tuple_fact_parser')
        tuple_names = ['fact_time', 'fact_value', 'display_name',
                       'eco_point_id',
                       'native_name', 'equipment', 'equipment_type',
                       'point_class']
        expected_named_tuple = namedtuple('response_tuple', tuple_names)

        expected_result = [
            expected_named_tuple(**{
                "display_name": "SpaceTemp",
                "eco_point_id": 1,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.ZN-T",
                "equipment": "VAV-301",
                "equipment_type": "VAV",
                "point_class":
                "SpaceAirTemperature"}, **{'fact_time': "2017-08-01 00:00",
                                           'fact_value': 67.5}),

            expected_named_tuple(**{
                "display_name": "SpaceTemp",
                "eco_point_id": 1,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.ZN-T",
                "equipment": "VAV-301",
                "equipment_type": "VAV",
                "point_class":
                "SpaceAirTemperature"}, **{'fact_time': "2017-08-01 00:05",
                                           'fact_value': 68.5}),

            expected_named_tuple(**{
                "display_name": "Cooling",
                "eco_point_id": 2,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.CV",
                "equipment": "VAV_301",
                "equipment_type": "VAV",
                "point_class": "CoolingCoilUnit"
                "Feedback"}, **{'fact_time': "2017-08-01 00:00",
                                'fact_value': 0}),

            expected_named_tuple(**{
                "display_name": "Cooling",
                "eco_point_id": 2,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.CV",
                "equipment": "VAV_301",
                "equipment_type": "VAV",
                "point_class": "CoolingCoilUnit"
                "Feedback"}, **{'fact_time': "2017-08-01 00:05",
                                'fact_value': 100})]
        mock__tuples_fact_parser.return_value = expected_result
        mock_response = mocker.Mock()
        result = facts_service._pandas_fact_parser(mock_response)
        expected_df = pd.DataFrame(columns=tuple_names,
                                   data=[[
                                       '2017-08-01 00:00', 67.5,
                                       'SpaceTemp', 1,
                                       'UCSB/275/VAV_301/NAE11/N2-2.'
                                       '275-VAV-301.ZN-T', 'VAV-301', 'VAV',
                                       'SpaceAirTemperature'],
                                       ['2017-08-01 00:05', 68.5,
                                        'SpaceTemp', 1,
                                        'UCSB/275/VAV_301/NAE11/N2-2.275'
                                        '-VAV-301.ZN-T', 'VAV-301', 'VAV',
                                        'SpaceAirTemperature'],
                                       ['2017-08-01 00:00', 0.0, 'Cooling', 2,
                                        'UCSB/275/VAV_301/NAE11/'
                                        'N2-2.275-VAV-301.CV',
                                        'VAV_301',
                                        'VAV',
                                        'CoolingCoilUnitFeedback'],
                                       ['2017-08-01 00:05', 100.0,
                                        'Cooling', 2,
                                        'UCSB/275/VAV_301/NAE11/N2-2.'
                                        '275-VAV-301.CV', 'VAV_301', 'VAV',
                                        'CoolingCoilUnitFeedback']])

        pd.testing.assert_frame_equal(result, expected_df)

    def test__csv_fact_parser(self, mocker, facts_service):
        mock_response = mocker.Mock()

        tuple_names = ['fact_time', 'fact_value', 'display_name',
                       'eco_point_id',
                       'native_name', 'equipment', 'equipment_type',
                       'point_class']
        expected_named_tuple = namedtuple('response_tuple', tuple_names)

        expected_result = [
            expected_named_tuple(**{
                "display_name": "SpaceTemp",
                "eco_point_id": 1,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.ZN-T",
                "equipment": "VAV-301",
                "equipment_type": "VAV",
                "point_class":
                "SpaceAirTemperature"}, **{'fact_time': "2017-08-01 00:00",
                                           'fact_value': 67.5}),

            expected_named_tuple(**{
                "display_name": "SpaceTemp",
                "eco_point_id": 1,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.ZN-T",
                "equipment": "VAV-301",
                "equipment_type": "VAV",
                "point_class":
                "SpaceAirTemperature"}, **{'fact_time': "2017-08-01 00:05",
                                           'fact_value': 68.5}),

            expected_named_tuple(**{
                "display_name": "Cooling",
                "eco_point_id": 2,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.CV",
                "equipment": "VAV_301",
                "equipment_type": "VAV",
                "point_class": "CoolingCoilUnit"
                "Feedback"}, **{'fact_time': "2017-08-01 00:00",
                                'fact_value': 0}),

            expected_named_tuple(**{
                "display_name": "Cooling",
                "eco_point_id": 2,
                "native_name": "UCSB/275/VAV_301/"
                "NAE11/N2-2.275-VAV-301.CV",
                "equipment": "VAV_301",
                "equipment_type": "VAV",
                "point_class": "CoolingCoilUnit"
                "Feedback"}, **{'fact_time': "2017-08-01 00:05",
                                'fact_value': 100})]

        mock_df = pd.DataFrame(expected_result)
        mock_df.to_csv = mocker.Mock()
        mocker.patch.object(facts_service, '_pandas_fact_parser',
                            return_value=mock_df)
        facts_service._csv_fact_parser(mock_response)

    def test_get_avg_facts_json(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_json_parser = mocker.patch(self.MODULE_PATH +
                                        '.RequestParser.json_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'json'
        mock_params = {
            'start_date': '2017-12-20 00:00',
            'end_date': '2017-12-21 00:00',
            'start_hour': '00:00',
            'end_hour': '23:55',
            'period': 'day',
            'aggregate': 'native_names',
            'eco_point_ids': [1, 2, 3],
            'equipment_names': ['VAV-01'],
            'equipment_types': ['VAV'],
            'point_classes': ['SpaceAirTemperature'],
            'display_names': ['SpaceTemp'],
            'native_names': ['native-name-1'],
            'point_class_expression': ['.* .*'],
            'display_name_expression': ['VAV.* .*'],
            'native_name_expression': ['AHU.* .*']}
        result = facts_service.get_avg_facts(building_id, **mock_params,
                                             result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/avg-facts'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_json_parser,
            parser_args={})

    def test_get_avg_facts_pandas(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_pandas_parser = mocker.patch.object(facts_service,
                                                 '_pandas_fact_avg_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'pandas'
        mock_params = {
            'start_date': '2017-12-20 00:00',
            'end_date': '2017-12-21 00:00',
            'start_hour': '00:00',
            'end_hour': '23:55',
            'period': 'day',
            'aggregate': 'native_names',
            'eco_point_ids': [1, 2, 3],
            'equipment_names': ['VAV-01'],
            'equipment_types': ['VAV'],
            'point_classes': ['SpaceAirTemperature'],
            'display_names': ['SpaceTemp'],
            'native_names': ['native-name-1'],
            'point_class_expression': ['.* .*'],
            'display_name_expression': ['VAV.* .*'],
            'native_name_expression': ['AHU.* .*']}
        result = facts_service.get_avg_facts(building_id, **mock_params,
                                             result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/avg-facts'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_pandas_parser,
            parser_args={'data_key': 'data'})

    def test_get_avg_facts_dqi_tuple(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_pandas_parser = mocker.patch.object(facts_service,
                                                 '_tuple_fact_avg_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'tuple'
        mock_params = {
            'start_date': '2017-12-20 00:00',
            'end_date': '2017-12-21 00:00',
            'start_hour': '00:00',
            'end_hour': '23:55',
            'period': 'day',
            'aggregate': 'native_names',
            'eco_point_ids': [1, 2, 3],
            'equipment_names': ['VAV-01'],
            'equipment_types': ['VAV'],
            'point_classes': ['SpaceAirTemperature'],
            'display_names': ['SpaceTemp'],
            'native_names': ['native-name-1'],
            'point_class_expression': ['.* .*'],
            'display_name_expression': ['VAV.* .*'],
            'native_name_expression': ['AHU.* .*']}
        result = facts_service.get_avg_facts(building_id, **mock_params,
                                             result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/avg-facts'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_pandas_parser,
            parser_args={'data_key': 'data'})

    def test_get_avg_facts_csv(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_pandas_parser = mocker.patch.object(facts_service,
                                                 '_csv_fact_avg_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'csv'
        mock_params = {
            'start_date': '2017-12-20 00:00',
            'end_date': '2017-12-21 00:00',
            'start_hour': '00:00',
            'end_hour': '23:55',
            'period': 'day',
            'aggregate': 'native_names',
            'eco_point_ids': [1, 2, 3],
            'equipment_names': ['VAV-01'],
            'equipment_types': ['VAV'],
            'point_classes': ['SpaceAirTemperature'],
            'display_names': ['SpaceTemp'],
            'native_names': ['native-name-1'],
            'point_class_expression': ['.* .*'],
            'display_name_expression': ['VAV.* .*'],
            'native_name_expression': ['AHU.* .*']}
        result = facts_service.get_avg_facts(building_id, **mock_params,
                                             result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/avg-facts'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_pandas_parser,
            parser_args={'data_key': 'data'})

    def test_get_avg_facts_invalid(self, mocker, facts_service):
        mocker.patch.object(facts_service, 'get')
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'arrows'
        mock_params = {
            'start_date': '2017-12-20 00:00',
            'end_date': '2017-12-21 00:00',
            'start_hour': '00:00',
            'end_hour': '23:55',
            'period': 'day',
            'aggregate': 'native_names',
            'eco_point_ids': [1, 2, 3],
            'equipment_names': ['VAV-01'],
            'equipment_types': ['VAV'],
            'point_classes': ['SpaceAirTemperature'],
            'display_names': ['SpaceTemp'],
            'native_names': ['native-name-1'],
            'point_class_expression': ['.* .*'],
            'display_name_expression': ['VAV.* .*'],
            'native_name_expression': ['AHU.* .*']}
        with pytest.raises(ValueError):
            facts_service.get_avg_facts(building_id,
                                        **mock_params,
                                        result_format=result_format)

    def test__tuple_fact_avg_parser(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"data": {"26": {
            "2017-12-20 00:00:00": 71.78,
            "2017-12-21 00:00:00": 72.78}}}
        tuple_names = ['aggregate', 'timestamp', 'fact_value']

        response_tuple = namedtuple('response_tuple', tuple_names)
        expected_result = [response_tuple(**{
                           'aggregate': "26",
                           'timestamp': "2017-12-20 00:00:00",
                           'fact_value': 71.78}),
                           response_tuple(**{'aggregate': "26",
                                             'timestamp':
                                             "2017-12-21 00:00:00",
                                             'fact_value': 72.78})]

        result = facts_service._tuple_fact_avg_parser(mock_response)
        assert result == expected_result

    def test__tuple_fact_avg_error(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_response.json.side_effect = ValueError
        mock_response.text = 'error'
        with pytest.raises(RequestParserError):
            facts_service._tuple_fact_avg_parser(mock_response)

    def test__pandas_fact_avg_parser(self, mocker, facts_service):
        tuple_names = ['aggregate', 'timestamp', 'fact_value']
        response_tuple = namedtuple('response_tuple', tuple_names)
        mock_tuples = [response_tuple(**{'aggregate': "26",
                                         'timestamp': "2017-12-20 00:00:00",
                                         'fact_value': 71.78}),
                       response_tuple(**{'aggregate': "26",
                                         'timestamp':
                                         "2017-12-21 00:00:00",
                                         'fact_value': 72.78})]
        mocker.patch.object(facts_service, '_tuple_fact_avg_parser',
                            return_value=mock_tuples)
        expected_data = [['26', "2017-12-20 00:00:00", 71.78],
                         ['26', "2017-12-21 00:00:00", 72.78]]
        expected_df = pd.DataFrame(columns=tuple_names, data=expected_data)
        mock_response = mocker.Mock()

        result = facts_service._pandas_fact_avg_parser(mock_response)
        pd.testing.assert_frame_equal(expected_df, result)

    def test__csv_fact_avg_parser(self, mocker, facts_service):
        tuple_names = ['aggregate', 'timestamp', 'fact_value']
        expected_data = [['26', "2017-12-20 00:00:00", 71.78],
                         ['26', "2017-12-21 00:00:00", 72.78]]
        expected_df = pd.DataFrame(columns=tuple_names, data=expected_data)
        mock_response = mocker.Mock()
        mocker.patch.object(facts_service, '_pandas_fact_avg_parser',
                            return_value=expected_df)

        result = facts_service._csv_fact_avg_parser(mock_response)
        assert result == ('aggregate,timestamp,fact_value\n'
                          '26,2017-12-20 00:00:00,71.78\n'
                          '26,2017-12-21 00:00:00,72.78\n')

    def test_put_facts(cls, mocker, facts_service):
        mock_put_facts = pd.DataFrame(columns=['native_name',
                                               'fact_value',
                                               'fact_time'],
                                      data=[['native_name-1',
                                             1,
                                             '2017-12-20 00:00'],
                                            ['native_name-2',
                                             2,
                                             '2017-12-21 00:00']])
        mock_response = mocker.Mock()
        mock_put = mocker.patch.object(facts_service, 'put',
                                       return_value=mock_response)
        mock__get_parser = mocker.patch.object(facts_service,
                                               '_get_parser',
                                               return_value={'parser':
                                                             'parser',
                                                             'parser_args':
                                                             'args'})
        mock_parse_result = mocker.patch.object(facts_service,
                                                '_format_response',
                                                return_value=mock_response)
        result = facts_service.put_facts(26, mock_put_facts)
        mock_put.assert_called_once_with(
            'https://facts.prod.ecorithm.com/api/v1/building/26/facts',
            data=[{'native_name': 'native_name-1',
                   'fact_value': 1,
                   'fact_time': '2017-12-20 00:00'},
                  {'native_name': 'native_name-2',
                   'fact_value': 2,
                   'fact_time': '2017-12-21 00:00'}],
            encode_type='json')
        assert result == mock_response
        mock__get_parser.assert_called()
        mock_parse_result.assert_called()

    def test_get_buildings(self, mocker, facts_service):
        building_id = 1
        is_active = True
        result_format = 'pandas'
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/buildings')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        params = {'building_id': building_id, 'is_active': is_active}
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_buildings(building_id, is_active,
                                             result_format)
        mock_get.assert_called_once_with(expected_url, data=params)
        mock__get_parser.assert_called_once_with('pandas', data_key='data')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_put_building(self, mocker, facts_service):
        mock_building_id = 51
        mock_building_name = 'test-building'
        mock_response = mocker.Mock()
        mock_parser = {'parser': 'mock_parser',
                       'parser_args': {}}
        mock_put = mocker.patch.object(facts_service, 'put',
                                       return_value=mock_response)
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value=mock_parser)
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parse_get_result'
        result = facts_service.put_building(building=mock_building_name,
                                            building_id=mock_building_id)
        assert result == 'parse_get_result'
        mock__get_parser.assert_called_once_with('json')
        mock_put.assert_called_once_with('https://facts.prod.ecorithm.com/'
                                         'api/v1/buildings',
                                         data={
                                             'building': mock_building_name,
                                             'building_id': mock_building_id})

    def test_delete_building(self, mocker, facts_service):
        mock_building_id = 51
        mock_response = mocker.Mock()
        mock_parser = {'parser': 'mock_parser',
                       'parser_args': {}}
        mock_delete = mocker.patch.object(facts_service, 'delete',
                                          return_value=mock_response)
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value=mock_parser)
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parse_get_result'
        result = facts_service.delete_building(building_id=mock_building_id)
        assert result == 'parse_get_result'
        mock__get_parser.assert_called_once_with('json')
        mock_delete.assert_called_once_with('https://facts.prod.ecorithm.com/'
                                            'api/v1/buildings',
                                            data={
                                                'building_id': mock_building_id
                                                })

    def test_get_point_classes(self, mocker, facts_service):
        point_class = 'SpaceAirTemperature'
        is_active = True
        result_format = 'pandas'
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/point-classes')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        params = {'point_class': point_class, 'is_active': is_active}
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_point_classes(point_class, is_active,
                                                 result_format)
        mock_get.assert_called_once_with(expected_url, data=params)
        mock__get_parser.assert_called_once_with('pandas', data_key='data')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_put_point_class(self, mocker, facts_service):
        mock_point_class_id = 51
        mock_point_class = 'test-point-class'
        mock_response = mocker.Mock()
        mock_parser = {'parser': 'mock_parser',
                       'parser_args': {}}
        mock_put = mocker.patch.object(facts_service, 'put',
                                       return_value=mock_response)
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value=mock_parser)
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parse_get_result'
        result = facts_service.put_point_class(
            point_class_id=mock_point_class_id,
            point_class=mock_point_class)
        assert result == 'parse_get_result'
        mock__get_parser.assert_called_once_with('json')
        mock_put.assert_called_once_with(
            'https://facts.prod.ecorithm.com/api/v1/point-classes',
            data={'point_class': mock_point_class,
                  'point_class_id': mock_point_class_id})

    def test_delete_point_class(self, mocker, facts_service):
        point_class = 'SpaceTemp'
        mock_response = mocker.Mock()
        mock_parser = {'parser': 'mock_parser',
                       'parser_args': {}}
        mock_delete = mocker.patch.object(facts_service, 'delete',
                                          return_value=mock_response)
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value=mock_parser)
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parse_get_result'
        result = facts_service.delete_point_class(point_class=point_class)
        assert result == 'parse_get_result'
        mock__get_parser.assert_called_once_with('json')
        mock_delete.assert_called_once_with('https://facts.prod.ecorithm.com/'
                                            'api/v1/point-classes',
                                            data={'point_class': point_class})

    def test_get_point_mapping(self, mocker, facts_service):
        building_id = 1
        equipment_names = ['VAV_01']
        equipment_types = ['VAV']
        point_classes = ['SpaceAirTemperature']
        eco_point_ids = [1, 2, 3]
        display_names = ['SpaceTemp']
        native_names = ['native-name-1']
        point_class_expression = ['VAV.* .*']
        native_name_expression = ['VAV.*']
        display_name_expression = ['AHU.* .*']
        is_active = True
        result_format = 'pandas'
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/1/point-mapping')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        data = {
            'is_active': is_active,
            'eco_point_id': eco_point_ids,
            'equipment_name': equipment_names,
            'equipment_type': equipment_types,
            'point_class': point_classes,
            'display_name': display_names,
            'native_name': native_names,
            'point_class_expression': point_class_expression,
            'display_name_expression': display_name_expression,
            'native_name_expression': native_name_expression}
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_point_mapping(
            building_id=building_id,
            equipment_names=equipment_names,
            equipment_types=equipment_types,
            point_classes=point_classes,
            eco_point_ids=eco_point_ids,
            display_names=display_names,
            native_names=native_names,
            point_class_expression=point_class_expression,
            native_name_expression=native_name_expression,
            display_name_expression=display_name_expression,
            is_active=is_active,
            result_format=result_format)
        mock_get.assert_called_once_with(expected_url, data=data)
        mock__get_parser.assert_called_once_with('pandas', data_key='data')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_delete_point_mapping(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/point-mapping')
        mock_get = mocker.patch.object(facts_service, 'delete',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_payload = {'eco_point_id': [1, 2, 3]}
        result = facts_service.delete_point_mapping(building_id=26,
                                                    eco_point_ids=[1, 2, 3])
        mock_get.assert_called_once_with(expected_url, data=mock_payload,
                                         encode_type='form')
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_put_point_mapping(self, mocker, facts_service):
        mock_data = [['VAV_01', "VAV",
                      "UCSB/275/VAV_301/NAE11/N2-2.275-VAV-301.ZN-T",
                      3,
                      "SpaceAirTemperature",
                      "2017-11-17T17:44:04Z",
                      "SpaceTemp"],
                     ['VAV_02', "VAV",
                      "UCSB/275/VAV_301/NAE11/N2-2.275-VAV-302.ZN-T",
                      4,
                      "SpaceAirTemperature",
                      "2017-11-17T17:44:04Z",
                      "SpaceTemp"]]
        mock_columns = ['equipment_name', 'equipment_type', 'native_name',
                        'eco_point_id', 'point_class', 'last_updated',
                        'display_name']
        mock_put = mocker.patch.object(facts_service, 'put',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_df = pd.DataFrame(data=mock_data, columns=mock_columns)

        result = facts_service.put_point_mapping(building_id=26,
                                                 point_mapping=mock_df)
        put_input = [{
            'equipment_name': 'VAV_01',
            'equipment_type': "VAV",
            'native_name': "UCSB/275/VAV_301/NAE11/N2-2.275-VAV-301.ZN-T",
            'eco_point_id': 3,
            'point_class': "SpaceAirTemperature",
            'last_updated': "2017-11-17T17:44:04Z",
            'display_name': "SpaceTemp"},
            {'equipment_name': 'VAV_02',
             'equipment_type': "VAV",
             'native_name': "UCSB/275/VAV_301/NAE11/N2-2.275-VAV-302.ZN-T",
             'eco_point_id': 4,
             'point_class': "SpaceAirTemperature",
             'last_updated': "2017-11-17T17:44:04Z",
             'display_name': "SpaceTemp"}]
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/point-mapping')
        mock_put.assert_called_once_with(expected_url, data=put_input,
                                         encode_type='json')
        assert result == 'formated-result'
        mock__format_response.assert_called()
        mock__get_parser.assert_called()

    def test_get_equipment_types(self, mocker, facts_service):
        equipment_type = 'VAV'
        is_active = True
        result_format = 'pandas'
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/equipment-types')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        params = {'equipment_type': equipment_type, 'is_active': is_active}
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_equipment_types(equipment_type, is_active,
                                                   result_format)
        mock_get.assert_called_once_with(expected_url, data=params)
        mock__get_parser.assert_called_once_with('pandas', data_key='data')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_delete_equipment_type(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/equipment-types')
        mock_get = mocker.patch.object(facts_service, 'delete',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_payload = {'equipment_type': 'name-1'}
        result = facts_service.delete_equipment_type(equipment_type='name-1')
        mock_get.assert_called_once_with(expected_url, data=mock_payload,
                                         encode_type='form')
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_put_equipment_type(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/equipment-types')
        mock_get = mocker.patch.object(facts_service, 'put',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_payload = {'equipment_type': 'name-1',
                        'equipment_type_id': 123}
        result = facts_service.put_equipment_type(equipment_type='name-1',
                                                  equipment_type_id=123)
        mock_get.assert_called_once_with(expected_url, data=mock_payload,
                                         encode_type='form')
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_get_equipment(self, mocker, facts_service):
        building_id = 1
        equipment_name = ['VAV_01']
        equipment_type = ['VAV']
        is_active = True
        result_format = 'pandas'
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/1/equipment')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        params = {'equipment_name': equipment_name,
                  'equipment_type': equipment_type,
                  'is_active': is_active}
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_equipment(building_id=building_id,
                                             equipment_name=equipment_name,
                                             equipment_type=equipment_type,
                                             is_active=is_active,
                                             result_format=result_format)
        mock_get.assert_called_once_with(expected_url, data=params)
        mock__get_parser.assert_called_once_with('pandas', data_key='data')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_delete_equipment(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/equipment')
        mock_get = mocker.patch.object(facts_service, 'delete',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_payload = {'equipment_name': ['name-1', 'name-2']}
        result = facts_service.delete_equipment(building_id=26,
                                                equipments=['name-1',
                                                            'name-2'])
        mock_get.assert_called_once_with(expected_url, data=mock_payload,
                                         encode_type='form')
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_put_equipment(self, mocker, facts_service):
        mock_data = [['VAV_01',
                      'VAV',
                      3],
                     ['AHU_01',
                      'AHU',
                      4]]
        mock_columns = ['equipment_name',
                        'equipment_type',
                        'equipment_id']
        mock_put = mocker.patch.object(facts_service, 'put',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_df = pd.DataFrame(data=mock_data, columns=mock_columns)

        result = facts_service.put_equipment(building_id=26,
                                             equipments=mock_df)
        put_input = [{
            'equipment_name': 'VAV_01',
            'equipment_type': 'VAV',
            'equipment_id': 3},
            {'equipment_name': 'AHU_01',
             'equipment_type': 'AHU',
             'equipment_id': 4}]
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/equipment')
        mock_put.assert_called_once_with(expected_url, data=put_input,
                                         encode_type='json')
        assert result == 'formated-result'
        mock__format_response.assert_called()
        mock__get_parser.assert_called()

    def test_get_native_names(self, mocker, facts_service):
        building_id = 1
        native_name = 'VAV'
        is_active = True
        result_format = 'pandas'
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/1/native-names')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        params = {'native_name': native_name, 'is_active': is_active}
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_native_names(building_id, native_name,
                                                is_active,
                                                result_format)
        mock_get.assert_called_once_with(expected_url, data=params)
        mock__get_parser.assert_called_once_with('pandas', data_key='data')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_put_native_names(self, mocker, facts_service):
        mock_data = [['VAV_01',
                      True,
                      "Client",
                      3,
                      "COV",
                      "5 minutes"],
                     ['VAV_02',
                      True,
                      "Client",
                      4,
                      "COV",
                      "5 minutes"]]
        mock_columns = ['native_name', 'expecting_data', 'origin',
                        'native_name_id', 'trend_type', 'trend_period']
        mock_put = mocker.patch.object(facts_service, 'put',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_df = pd.DataFrame(data=mock_data, columns=mock_columns)

        result = facts_service.put_native_names(building_id=26,
                                                native_names=mock_df)
        put_input = [{
            'native_name': 'VAV_01',
            'expecting_data': True,
            'origin': "Client",
            'native_name_id': 3,
            'trend_type': "COV",
            'trend_period': "5 minutes"},
            {'native_name': 'VAV_02',
             'expecting_data': True,
             'origin': "Client",
             'native_name_id': 4,
             'trend_type': "COV",
             'trend_period': "5 minutes"}]
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/native-names')
        mock_put.assert_called_once_with(expected_url, data=put_input,
                                         encode_type='json')
        assert result == 'formated-result'
        mock__format_response.assert_called()
        mock__get_parser.assert_called()

    def test_delete_native_names(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/native-names')
        mock_get = mocker.patch.object(facts_service, 'delete',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        mock_payload = {'native_name': ['name-1', 'name-2']}
        result = facts_service.delete_native_names(building_id=26,
                                                   native_names=['name-1',
                                                                 'name-2'])
        mock_get.assert_called_once_with(expected_url, data=mock_payload,
                                         encode_type='form')
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_get_native_names_history(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/native-name-history')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_native_names_history(building_id=26)
        mock_get.assert_called_once_with(expected_url)
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_get_unamapped_native_names(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/unmapped-native-names')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_unamapped_native_names(building_id=26)
        mock_get.assert_called_once_with(expected_url)
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_get_etl_process_history(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/etl-process-history')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_etl_process_history(building_id=26,
                                                       return_limit=10)
        mock_get.assert_called_once_with(expected_url,
                                         data={'return_limit': 10})
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_get_unstored_native_names(self, mocker, facts_service):
        expected_url = ('https://facts.prod.ecorithm.com/api/'
                        'v1/building/26/unstored-native-names')
        mock_get = mocker.patch.object(facts_service, 'get',
                                       return_value='mock-response')
        mock__get_parser = mocker.patch.object(facts_service, '_get_parser',
                                               return_value={'parser':
                                                             'mock-parser',
                                                             'parser_args':
                                                             {'arg': 1}})
        mock__format_response = mocker.patch.object(facts_service,
                                                    '_format_response',
                                                    return_value=('formated'
                                                                  '-result'))
        result = facts_service.get_unstored_native_names(building_id=26)
        mock_get.assert_called_once_with(expected_url)
        mock__get_parser.assert_called_once_with('json')
        mock__format_response.assert_called_once_with('mock-response',
                                                      parser='mock-parser',
                                                      parser_args={'arg': 1})
        assert result == 'formated-result'

    def test_get_building_dqi_json(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_json_parser = mocker.patch(self.MODULE_PATH +
                                        '.RequestParser.json_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'json'
        mock_params = {'start_date': '2017-12-20',
                       'end_date': '2017-12-21',
                       'dqi_aggregate': 'building_id',
                       'period': 'day',
                       'native_name_expression': '.*'}
        result = facts_service.get_building_dqi(building_id, **mock_params,
                                                result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/dqi'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_json_parser,
            parser_args={})

    def test_get_building_dqi_pandas(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_pandas_parser = mocker.patch.object(facts_service,
                                                 '_pandas_dqi_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'pandas'
        mock_params = {'start_date': '2017-12-20',
                       'end_date': '2017-12-21',
                       'dqi_aggregate': 'building_id',
                       'period': 'day',
                       'native_name_expression': '.*'}
        result = facts_service.get_building_dqi(building_id, **mock_params,
                                                result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/dqi'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_pandas_parser,
            parser_args={'data_key': 'data'})

    def test_get_building_dqi_tuple(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_pandas_parser = mocker.patch.object(facts_service,
                                                 '_tuple_dqi_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'tuple'
        mock_params = {'start_date': '2017-12-20',
                       'end_date': '2017-12-21',
                       'dqi_aggregate': 'building_id',
                       'period': 'day',
                       'native_name_expression': '.*'}
        result = facts_service.get_building_dqi(building_id, **mock_params,
                                                result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/dqi'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_pandas_parser,
            parser_args={'data_key': 'data'})

    def test_get_building_dqi_csv(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_pandas_parser = mocker.patch.object(facts_service,
                                                 '_csv_dqi_parser')
        mock_get = mocker.patch.object(facts_service, 'get')
        mock_get.return_value = mock_response
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'csv'
        mock_params = {'start_date': '2017-12-20',
                       'end_date': '2017-12-21',
                       'dqi_aggregate': 'building_id',
                       'period': 'day',
                       'native_name_expression': '.*'}
        result = facts_service.get_building_dqi(building_id, **mock_params,
                                                result_format=result_format)
        assert result == 'parsed_result'
        mock_get.assert_called_once_with(
            ('https://facts.prod.ecorithm.com/api/v1/building/26/dqi'),
            data=mock_params
            )
        mock_format_response.assert_called_once_with(
            mock_response, parser=mock_pandas_parser,
            parser_args={'data_key': 'data'})

    def test_get_building_dqi_invalid(self, mocker, facts_service):

        mocker.patch.object(facts_service, 'get')
        mock_format_response = mocker.patch.object(facts_service,
                                                   '_format_response')
        mock_format_response.return_value = 'parsed_result'
        building_id = 26
        result_format = 'arrows'
        mock_params = {'start_date': '2017-12-20',
                       'end_date': '2017-12-21',
                       'dqi_aggregate': 'building_id',
                       'period': 'day',
                       'native_name_expression': '.*'}
        with pytest.raises(ValueError):
            facts_service.get_building_dqi(building_id,
                                           **mock_params,
                                           result_format=result_format)

    def test__tuple_dqi_parser(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"data": {"26": {
            "2017-12-20 00:00:00": 71.78,
            "2017-12-21 00:00:00": 72.78}}}
        tuple_names = ['aggregate', 'timestamp', 'dqi']

        response_tuple = namedtuple('response_tuple', tuple_names)
        expected_result = [response_tuple(**{
                           'aggregate': "26",
                           'timestamp': "2017-12-20 00:00:00",
                           'dqi': 71.78}),
                           response_tuple(**{'aggregate': "26",
                                             'timestamp':
                                             "2017-12-21 00:00:00",
                                             'dqi': 72.78})]

        result = facts_service._tuple_dqi_parser(mock_response)
        assert result == expected_result

    def test__tuple_dqi_error(self, mocker, facts_service):
        mock_response = mocker.Mock()
        mock_response.json.side_effect = ValueError
        mock_response.text = 'error'
        with pytest.raises(RequestParserError):
            facts_service._tuple_dqi_parser(mock_response)

    def test__pandas_dqi_parser(self, mocker, facts_service):
        tuple_names = ['aggregate', 'timestamp', 'dqi']
        response_tuple = namedtuple('response_tuple', tuple_names)
        mock_tuples = [response_tuple(**{'aggregate': "26",
                                         'timestamp': "2017-12-20 00:00:00",
                                         'dqi': 71.78}),
                       response_tuple(**{'aggregate': "26",
                                         'timestamp':
                                         "2017-12-21 00:00:00",
                                         'dqi': 72.78})]
        mocker.patch.object(facts_service, '_tuple_dqi_parser',
                            return_value=mock_tuples)
        expected_data = [['26', "2017-12-20 00:00:00", 71.78],
                         ['26', "2017-12-21 00:00:00", 72.78]]
        expected_df = pd.DataFrame(columns=tuple_names, data=expected_data)
        mock_response = mocker.Mock()

        result = facts_service._pandas_dqi_parser(mock_response)
        pd.testing.assert_frame_equal(expected_df, result)

    def test__csv_dqi_parser(self, mocker, facts_service):
        tuple_names = ['aggregate', 'timestamp', 'dqi']
        expected_data = [['26', "2017-12-20 00:00:00", 71.78],
                         ['26', "2017-12-21 00:00:00", 72.78]]
        expected_df = pd.DataFrame(columns=tuple_names, data=expected_data)
        mock_response = mocker.Mock()
        mocker.patch.object(facts_service, '_tuple_dqi_parser',
                            return_value=expected_df)

        result = facts_service._csv_dqi_parser(mock_response)
        assert result == ('aggregate,timestamp,dqi\n'
                          '26,2017-12-20 00:00:00,71.78\n'
                          '26,2017-12-21 00:00:00,72.78\n')
