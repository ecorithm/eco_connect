import pytest

from eco_connect.connectors.facts_service import FactsService


class TestFactsService:
    MODULE_PATH = 'eco_connect.connectors.facts_service'
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

    def test__tuple_fact_parser(self):
        pass

    def test__tuple_fact_parser_bad_json(self):
        pass

    def test__tuple_fact_parser_bad_key(self):
        pass

    def test__pandas_fact_parser(self):
        pass

    def test__csv_fact_parser(self):
        pass
