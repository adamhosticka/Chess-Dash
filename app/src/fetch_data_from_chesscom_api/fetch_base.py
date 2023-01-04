"""
Base class for fetching data from Chess.com API and saving them to a file.
"""

import requests
import json
import pandas as pd

from app.helpers.api_endpoints import REQUEST_HEADERS
from app.utils.load_save_dataframe import load_dataframe, save_dataframe


class FetchBase:
    FILE_NAME = None

    dataframe = pd.DataFrame()

    def run(self):
        """Fetch data and export them to csv."""
        self.fetch_data()
        self._save_data()

    def fetch_data(self):
        """Call fetch_item, modify the return value and save it to data."""
        pass

    @staticmethod
    def fetch_item(url: str) -> dict:
        """Send request to Chess.com API.

        :param str url: Request url.
        :return: API response item.
        :rtype: dict.
        """
        res = requests.get(url, headers=REQUEST_HEADERS)
        item = json.loads(res.text)
        item['status_code'] = res.status_code
        item['etag'] = res.headers.get('etag')
        item['last_modified'] = res.headers.get('last-modified')
        return item

    def create_dataframe_from_list(self, data: list):
        """Save list of data into dataframe.

        :param list data: Data to save.
        """
        self.dataframe = pd.DataFrame.from_dict(data)

    @staticmethod
    def remove_same_columns_from_right(left: pd.DataFrame, right: pd.DataFrame, keep_column: str) -> pd.DataFrame:
        left_columns_for_diff = set(left.columns)
        left_columns_for_diff.remove(keep_column)
        return right[list(set(right.columns).difference(left_columns_for_diff))]

    @staticmethod
    def load_dataframe(filename: str) -> pd.DataFrame:
        """Call load_dataframe function from utils.

        :arg: str filename: Name of file to load.
        :return: Dataframe.
        :rtype: pd.DataFrame.
        """
        return load_dataframe(filename)

    @staticmethod
    def save_dataframe(dataframe: pd.DataFrame, filename: str):
        """Call save_dataframe function from utils.

        :arg: pd.Dataframe dataframe: Dataframe to save.
        :arg: str filename: Filename to save dataframe to.
        """
        save_dataframe(dataframe, filename)

    def _save_data(self):
        """Save data to file."""
        self.save_dataframe(self.dataframe, self.FILE_NAME)
