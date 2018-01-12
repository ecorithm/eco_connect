import pytest

from eco_connect.src.base_request import BaseRequest
from eco_connect.src.errors import InvalidRequest


class TestBaseRequest:
    MODULE_PATH = 'eco_connect.src.base_request'
    CLASS_PATH = MODULE_PATH + '.BaseRequest'

    def test_get(self, mocker):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_get = mocker.patch(self.MODULE_PATH + '.requests.get',
                                        return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}
        auth = ('username', 'password')

        result = BaseRequest.get(mock_url, data, auth)
        mock_format_kwargs.assert_called_once_with(data=data,
                                                   auth=auth,
                                                   encode_type='querystring')
        mock_request_get.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test_put(self, mocker):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_put = mocker.patch(self.MODULE_PATH + '.requests.put',
                                        return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}
        auth = ('username', 'password')

        result = BaseRequest.put(url=mock_url,
                                 data=data, auth=auth,
                                 encode_type='querystring')
        mock_format_kwargs.assert_called_once_with(data=data,
                                                   auth=auth,
                                                   encode_type='querystring')
        mock_request_put.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test_post(self, mocker):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_post = mocker.patch(self.MODULE_PATH + '.requests.post',
                                         return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}
        auth = ('username', 'password')

        result = BaseRequest.post(url=mock_url,
                                  data=data, auth=auth,
                                  encode_type='querystring')
        mock_format_kwargs.assert_called_once_with(data=data,
                                                   auth=auth,
                                                   encode_type='querystring')
        mock_request_post.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test_delete(self, mocker):
        mock_format_kwargs = mocker.patch(self.CLASS_PATH + '._format_kwargs')
        mock_format_kwargs.return_value = {'arg1': 1, 'arg2': 2}
        mock_request_delete = mocker.patch(
            self.MODULE_PATH + '.requests.delete',
            return_value='response')

        mock_url = 'mock-get-url'
        data = {'param1': 1,
                'param2': 2}
        auth = ('username', 'password')

        result = BaseRequest.delete(url=mock_url,
                                    data=data, auth=auth,
                                    encode_type='querystring')
        mock_format_kwargs.assert_called_once_with(data=data,
                                                   auth=auth,
                                                   encode_type='querystring')
        mock_request_delete.assert_called_once_with(mock_url, arg1=1, arg2=2)
        assert result == 'response'

    def test__format_kwargs_querystring(self, mocker):
        mock_data = {'item1': 1, 'item2': 2}
        auth = ('username', 'password')
        encode_type = 'querystring'
        result = BaseRequest._format_kwargs(mock_data, auth, encode_type)
        assert result == {'auth': auth, 'params': mock_data}

    def test__format_kwargs_form(self, mocker):
        mock_data = {'item1': 1, 'item2': 2}
        auth = ('username', 'password')
        encode_type = 'form'
        result = BaseRequest._format_kwargs(mock_data, auth, encode_type)
        assert result == {'auth': auth, 'data': mock_data}

    def test__format_kwargs_json(self, mocker):
        mock_data = {'item1': 1, 'item2': 2}
        auth = ('username', 'password')
        encode_type = 'json'
        result = BaseRequest._format_kwargs(mock_data, auth, encode_type)
        assert result == {'auth': auth, 'json': mock_data}

    def test__format_kwargs_exception(self, mocker):
        mock_data = {}
        auth = ()
        encode_type = 'invalid'
        with pytest.raises(ValueError):
            BaseRequest._format_kwargs(mock_data, auth, encode_type)

    def test__format_response_200(self, mocker):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 200

        result = BaseRequest._format_response(
            mock_response,
            result_parser=mock_result_parser,
            parser_args=parser_args)
        mock_result_parser.assert_called_once_with(mock_response,
                                                   arg1=1,
                                                   arg2=2)

        assert result == 'parsed_result'

    def test__format_response_201(self, mocker):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 200

        result = BaseRequest._format_response(
            mock_response,
            result_parser=mock_result_parser,
            parser_args=parser_args)
        mock_result_parser.assert_called_once_with(mock_response,
                                                   arg1=1,
                                                   arg2=2)

        assert result == 'parsed_result'

    def test__format_response_400_json(self, mocker):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_response.json.return_value = {'error': 'bad request'}
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 400

        with pytest.raises(InvalidRequest):
            BaseRequest._format_response(
                mock_response,
                result_parser=mock_result_parser,
                parser_args=parser_args)
            mock_response.json.asset_called_once()

    def test__format_response_400_text(self, mocker):
        mock_response = mocker.Mock()
        mock_result_parser = mocker.Mock()
        mock_response.json.side_effect = ValueError
        mock_response.text.return_value = 'error'
        mock_result_parser.return_value = 'parsed_result'
        parser_args = {'arg1': 1, 'arg2': 2}
        mock_response.status_code = 400

        with pytest.raises(InvalidRequest):
            BaseRequest._format_response(
                mock_response,
                result_parser=mock_result_parser,
                parser_args=parser_args)
            mock_response.text.asset_called_once()
