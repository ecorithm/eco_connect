from collections import namedtuple

import pytest
import pandas as pd

from eco_connect.src.request_parser import RequestParser
from eco_connect.src.errors import RequestParserError


class TestResultParser:
    MODULE_PATH = 'eco_connect.src.request_parser'
    CLASS_PATH = MODULE_PATH + '.RequestParser'

    def test_json_parser_json(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {'mock': 'json'}
        result = RequestParser.json_parser(mock_response)
        assert result == {'mock': 'json'}

    def test_json_parser_parser_text(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.side_effect = ValueError
        mock_response.text = 'mock_response'
        result = RequestParser.json_parser(mock_response)
        assert result == 'mock_response'

    def test_tuple_parser(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {'mock': 'json'}
        result = RequestParser.tuple_parser(mock_response)
        expected_named_tuple = namedtuple('response_tuple', ['mock'])
        assert result == [expected_named_tuple(**{'mock': 'json'})]

    def test_tuple_parser_with_key(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {'data': {'mock': 'json'}}
        result = RequestParser.tuple_parser(mock_response, data_key='data')
        expected_named_tuple = namedtuple('response_tuple', ['mock'])
        assert result == [expected_named_tuple(**{'mock': 'json'})]

    def test_tuple_parser_list(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {'data': [{'mock': 'json'},
                                                    {'mock': 'json'}]}
        result = RequestParser.tuple_parser(mock_response, data_key='data')
        expected_named_tuple = namedtuple('response_tuple', ['mock'])
        assert result == [expected_named_tuple(**{'mock': 'json'}),
                          expected_named_tuple(**{'mock': 'json'})]

    def test_tuple_parser_dict(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {'data': [{'mock': 'json1',
                                                     'mock2': 'json2'},
                                                    {'mock': 'json3',
                                                     'mock2': 'json4'}]}
        result = RequestParser.tuple_parser(mock_response, data_key='data')
        expected_named_tuple = namedtuple('response_tuple', ['mock', 'mock2'])
        assert result == [expected_named_tuple(**{'mock': 'json1',
                                                  'mock2': 'json2'}),
                          expected_named_tuple(**{'mock': 'json3',
                                                  'mock2': 'json4'})]

    def test_tuple_parser_json_fail(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.side_effect = ValueError
        with pytest.raises(RequestParserError):
            RequestParser.tuple_parser(mock_response)

    def test_tuple_parser_key_error(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {'message': [{'mock': 'json1',
                                                        'mock2': 'json2'},
                                                       {'mock': 'json3',
                                                        'mock2': 'json4'}]}
        with pytest.raises(RequestParserError):
            RequestParser.tuple_parser(mock_response, data_key='data')

    def test_tuple_parser_unable_to_parse(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = 1
        with pytest.raises(RequestParserError):
            RequestParser.tuple_parser(mock_response)

    def test_pandas_parser(self, mocker):
        data_key = 'data'
        mock_response = mocker.Mock()
        tuple_parser = mocker.patch(self.CLASS_PATH + '.tuple_parser')

        expected_named_tuple = namedtuple('response_tuple', ['mock'])
        tuple_result = [expected_named_tuple(**{'mock': 'json'}),
                        expected_named_tuple(**{'mock': 'json'})]
        tuple_parser.return_value = tuple_result
        expected_result = pd.DataFrame(columns=['mock'], data=['json', 'json'])

        result = RequestParser.pandas_parser(mock_response, data_key)
        tuple_parser.assert_called_once_with(mock_response, data_key)

        pd.testing.assert_frame_equal(result, expected_result)

    def test_csv_parser(self, mocker):
        mock_response = mocker.Mock()
        mock_data_key = 'data'

        mock_df = mocker.Mock()
        pandas_parser = mocker.patch(self.CLASS_PATH + '.pandas_parser',
                                     return_value=mock_df)

        RequestParser.csv_parser(mock_response, data_key=mock_data_key)
        pandas_parser.assert_called_once_with(mock_response, data_key='data')
