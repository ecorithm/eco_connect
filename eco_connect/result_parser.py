import os
from collections import namedtuple

import pandas as pd

from eco_connect.errors import ResultParserError


class RequestParser:

    @classmethod
    def raw_parser(cls, response):
        try:
            return response.json()
        except ValueError:
            return response.text

    @classmethod
    def tuple_parser(cls, response, data_key=None):
        try:
            result = response.json()
            if data_key:
                result = result[data_key]
        except (ValueError, KeyError):
            raise ResultParserError('Unable to parse the response.')

        parsed_result = []

        if isinstance(dict, result):
            response_tuple = namedtuple('response_tuple', result.keys())
            return [response_tuple(**result)]

        elif isinstance(list, result) and isinstance(dict, result[0]):
            response_tuple = namedtuple('response_tuple', result[0].keys())
            for row in result:
                parsed_result.append(response_tuple(**row))

        else:
            raise ResultParserError('Unable to parse the response.')

    @classmethod
    def pandas_parser(cls, response, data_key=None):
        tuple_response = cls.tuple_parser(response, data_key)
        return pd.DataFrame(tuple_response)

    @classmethod
    def csv_parser(cls, response,
                   data_key=None,
                   download_folder=os.path.expanduser('~') + '/downloads/',
                   file_name='data.csv'):
        result_df = cls.pandas_parser(response, data_key=data_key)
        os.makedirs(download_folder, exist_ok=True)
        result_df.to_csv(file_name, index=None)
        return result_df
