from eco_connect.src.errors import InvalidRequest
from eco_connect.src.request_parser import RequestParser

import requests


class BaseRequest:

    @classmethod
    def get(cls, url, data={}, auth=()):
        kwargs = cls._format_kwargs(data=data,
                                    auth=auth,
                                    encode_type='querystring')
        return requests.get(url, **kwargs)

    @classmethod
    def put(cls, url, data={}, encode_type='form', auth=()):
        kwargs = cls._format_kwargs(data=data,
                                    auth=auth,
                                    encode_type=encode_type)
        return requests.put(url, **kwargs)

    @classmethod
    def post(cls, url, data={}, encode_type='form', auth=()):
        kwargs = cls._format_kwargs(data=data,
                                    auth=auth,
                                    encode_type=encode_type)
        return requests.post(url, **kwargs)

    @classmethod
    def delete(cls, url, data={}, encode_type='form', auth=()):
        kwargs = cls._format_kwargs(data=data,
                                    auth=auth,
                                    encode_type=encode_type)
        return requests.delete(url, **kwargs)

    @classmethod
    def _format_kwargs(cls, data, auth, encode_type):
        if encode_type.lower() == 'querystring':
            return {'auth': auth, 'params': data}

        elif encode_type.lower() == 'form':
            return {'auth': auth, 'data': data}

        elif encode_type.lower() == 'json':
            return {'auth': auth, 'json': data}

        else:
            raise ValueError(f'({encode_type}) is not valid!')

    @classmethod
    def _format_response(self, response,
                         result_parser=RequestParser.raw_parser,
                         parser_args={}):
        if response.status_code == 200 or response.status_code == 201:
            return result_parser(response, **parser_args)
        else:
            try:
                raise InvalidRequest(response.json(), response.status_code)
            except ValueError:
                raise InvalidRequest(response.text, response.status_code)
