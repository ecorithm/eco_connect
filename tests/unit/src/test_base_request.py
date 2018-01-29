import pytest
import tempfile

from ecp_connect.src.base_request import BaseRequest
from ecp_connect.src.errors import InvalidRequest
from ecp_connect.src.request_parser import RequestParser


class TestBaseRequest():
    MODULE_PATH = 'ecp_connect.src.base_request'
    CLASS_PATH = MODULE_PATH + '.BaseRequest'

    @pytest.fixture
    def base_request(self, mocker):
        mocker.patch(self.CLASS_PATH + '._set_credentials')
        base_request = BaseRequest()
        base_request.credentials = ('username', 'password')
        return base_request

    def test_get(self, mocker, base_request):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_get = mocker.patch(self.MODULE_PATH + '.requests.get',
                                        return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}

        result = base_request.get(mock_url, data)
        mock_format_kwargs.assert_called_once_with(data=data,
                                                   encode_type='querystring')
        mock_request_get.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test_put(self, mocker, base_request):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_put = mocker.patch(self.MODULE_PATH + '.requests.put',
                                        return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}

        result = base_request.put(url=mock_url,
                                  data=data,
                                  encode_type='querystring')
        mock_format_kwargs.assert_called_once_with(data=data,
                                                   encode_type='querystring')
        mock_request_put.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test_post(self, mocker, base_request):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_post = mocker.patch(self.MODULE_PATH + '.requests.post',
                                         return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}

        result = base_request.post(url=mock_url,
                                   data=data,
                                   encode_type='querystring')
        mock_format_kwargs.assert_called_once_with(data=data,
                                                   files={},
                                                   encode_type='querystring')
        mock_request_post.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test_delete(self, mocker, base_request):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_delete = mocker.patch(
            self.MODULE_PATH + '.requests.delete',
            return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}

        result = base_request.delete(url=mock_url,
                                     data=data,
                                     encode_type='querystring')
        mock_format_kwargs.assert_called_once_with(data=data,

                                                   encode_type='querystring')
        mock_request_delete.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test__format_kwargs_querystring(self, mocker, base_request):
        mock_data = {'item1': 1, 'item2': 2}
        files = {}
        auth = ('username', 'password')
        encode_type = 'querystring'
        result = base_request._format_kwargs(mock_data, encode_type, files)
        assert result == {'auth': auth, 'params': mock_data}

    def test__format_kwargs_form(self, mocker, base_request):
        mock_data = {'item1': 1, 'item2': 2}
        files = {}
        auth = ('username', 'password')
        encode_type = 'form'
        result = base_request._format_kwargs(mock_data, encode_type, files)
        assert result == {'auth': auth, 'data': mock_data}

    def test__format_kwargs_json(self, mocker, base_request):
        mock_data = {'item1': 1, 'item2': 2}
        files = {}
        auth = ('username', 'password')
        encode_type = 'json'
        result = base_request._format_kwargs(mock_data, encode_type, files)
        assert result == {'auth': auth, 'json': mock_data}

    def test__format_kwargs_file(self, mocker, base_request):
        mock_data = {'item1': 1, 'item2': 2}
        image = tempfile.NamedTemporaryFile(suffix=".jpg")
        filerecord = open(image.name, 'rb')
        files = {'filerecord': filerecord}
        auth = ('username', 'password')
        encode_type = 'form'
        result = base_request._format_kwargs(mock_data, encode_type, files)
        assert result == {'auth': auth, 'data': mock_data, 'files': files}

    def test__format_kwargs_exception(self, mocker, base_request):
        mock_data = {}
        files = {}
        encode_type = 'invalid'
        with pytest.raises(ValueError):
            base_request._format_kwargs(mock_data, encode_type, files)

    def test__format_response_200(self, mocker, base_request):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 200

        result = base_request._format_response(
            mock_response,
            parser=mock_result_parser,
            parser_args=parser_args)
        mock_result_parser.assert_called_once_with(mock_response,
                                                   arg1=1,
                                                   arg2=2)

        assert result == 'parsed_result'

    def test__format_response_201(self, mocker, base_request):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 200

        result = base_request._format_response(
            mock_response,
            parser=mock_result_parser,
            parser_args=parser_args)
        mock_result_parser.assert_called_once_with(mock_response,
                                                   arg1=1,
                                                   arg2=2)

        assert result == 'parsed_result'

    def test__format_response_400_json(self, mocker, base_request):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_response.json.return_value = {'error': 'bad request'}
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 400

        base_request._format_response(
            mock_response,
            parser=mock_result_parser,
            parser_args=parser_args)
        mock_response.json.asset_called_once()

    def test__format_response_400_text(self, mocker, base_request):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_response.json.side_effect = ValueError
        mock_response.text.return_value = 'error'
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 400

        base_request._format_response(
            mock_response,
            parser=mock_result_parser,
            parser_args=parser_args)
        mock_response.text.asset_called_once()

    def test__format_response_401_text(self, mocker, base_request):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_response.json.side_effect = ValueError
        mock_response.text.return_value = 'error'
        mock_result_parser.return_value = 'parsed_result'
        mock_response.status_code = 401

        with pytest.raises(InvalidRequest):
            base_request._format_response(
                mock_response,
                parser=mock_result_parser)
            mock_response.text.asset_called_once()

    def test__set_credentials(self, mocker):
        get_eco_credentials = mocker.patch(
            self.MODULE_PATH + '.CredentialsFactory.get_eco_credentials',
            return_value=1)
        br = BaseRequest()
        br._set_credentials
        assert br.credentials == 1
        get_eco_credentials.call_count == 2

    def test_get_parser_pandas(self, base_request):
        result_format = 'pandas'
        data_key = 'data-key'
        parser = base_request._get_parser(result_format, data_key=data_key)
        assert parser['parser'] == RequestParser.pandas_parser
        assert parser['parser_args'] == {'data_key': data_key}

    def test_get_parser_csv(self, base_request):
        result_format = 'csv'
        data_key = 'data-key'
        parser = base_request._get_parser(
            result_format, data_key=data_key)
        assert parser['parser'] == RequestParser.csv_parser
        assert parser['parser_args'] == {'data_key': data_key}

    def test_get_parser_tuple(self, base_request):
        result_format = 'tuple'
        data_key = 'data-key'
        parser = base_request._get_parser(result_format, data_key=data_key)
        assert parser['parser'] == RequestParser.tuple_parser
        assert parser['parser_args'] == {'data_key': data_key}

    def test_get_parser_json(self, base_request):
        result_format = 'json'
        parser = base_request._get_parser(result_format)
        assert parser['parser'] == RequestParser.json_parser
        assert parser['parser_args'] == {}

    def test_get_parser_value_error(self, base_request):
        result_format = 'arrow'
        with pytest.raises(ValueError):
            base_request._get_parser(result_format)
