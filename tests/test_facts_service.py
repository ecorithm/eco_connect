from collections import namedtuple

import pytest
import pandas as pd

from eco_connect import FactsService
from eco_connect.src.errors import RequestParserError


class TestFactsService:
    MODULE_PATH = 'eco_connect'
    CLASS_PATH = MODULE_PATH + '.FactsService'\


    @pytest.fixture
    def facts_service(self, mocker):
        facts_service = FactsService()
        facts_service.credentials = ('user', 'password')
        return facts_service

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

    def test__validate_env(self, mocker, facts_service):
        environment_name = 'PROD'
        result = facts_service._validate_env(environment_name)
        assert result == 'prod'

    def test__validate_env_fail(self, mocker, facts_service):
        environment_name = 'production'
        with pytest.raises(ValueError):
            facts_service._validate_env(environment_name)

    def test__set_credentials(self, mocker, facts_service):
        get_eco_credentials = mocker.patch(
            self.MODULE_PATH + '.CredentialsFactory.get_eco_credentials')
        get_eco_credentials.return_value = 1
        mocker.patch(self.CLASS_PATH, )
        facts_service._set_credentials()
        get_eco_credentials.assert_called_once()
        assert facts_service.credentials == 1

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
                                           native_name_expression},
                                     auth=('user', 'password'))

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
                                           native_name_expression},
                                     auth=('user', 'password'))

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
                                           native_name_expression},
                                     auth=('user', 'password'))

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
                                         result_format=result_format,
                                         download_folder='/downloads/',
                                         file_name='data.csv')
        assert result == 'parsed_result'
        mock_format_result.assert_called_with(mock_response,
                                              expected_parser,
                                              {'download_folder':
                                               '/downloads/',
                                               'file_name': 'data.csv'})
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
                                           native_name_expression},
                                     auth=('user', 'password'))

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
        download_folder = '/'
        file_name = 'data.csv'
        make_dirs = mocker.patch(self.MODULE_PATH + '.os.makedirs')

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
        facts_service._csv_fact_parser(mock_response,
                                       download_folder, file_name)
        make_dirs.assert_called_once_with('/', exist_ok=True)

    def test_get_avg_facts(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_avg_facts()

    def test_put_facts(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.put_facts()

    def test_get_buildings(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_buildings()

    def test_put_buildings(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.put_buildings()

    def test_delete_buildings(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.delete_buildings()

    def test_get_point_classes(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_point_classes()

    def test_put_point_class(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.put_point_class()

    def test_delete_point_class(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.delete_point_class()

    def test_get_point_mapping(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_point_mapping()

    def test_delete_point_mapping(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.delete_point_mapping()

    def test_put_point_mapping(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.put_point_mapping()

    def test_get_equipment_types(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_equipment_types()

    def test_delete_equipment_type(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.delete_equipment_type()

    def test_put_equipment_type(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.put_equipment_type()

    def test_get_equipment(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_equipment()

    def test_delete_equipment(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.delete_equipment()

    def test_put_equipment(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.put_equipment()

    def test_get_native_names(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_native_names()

    def test_put_native_names(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.put_native_names()

    def test_delete_native_names(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.delete_native_names()

    def test_get_native_names_history(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_native_names_history()

    def test_get_unamapped_native_names(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_unamapped_native_names()

    def test_get_etl_process_history(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_etl_process_history()

    def test_get_unstored_antive_names(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_unstored_antive_names()

    def test_get_building_dqi(cls, facts_service):
        with pytest.raises(NotImplementedError):
            facts_service.get_building_dqi()
