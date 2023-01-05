"""
Base class for fetching data from Chess.com API and saving them to a file.
"""

import requests
import json
import pandas as pd
from time import sleep

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
        if res.status_code != 200:
            print(f"WARNING: Status code {res.status_code} for url: {url}.")
            sleep(1)
            if res.status_code == 429:  # Rate limit
                print("Sleeping for one minute.")
                sleep(60)
                res = requests.get(url, headers=REQUEST_HEADERS)
                if res.status_code == 429:  # Rate limit
                    print("Rate limit exceeded -> exiting.")
                    exit(0)
            return None
        return json.loads(res.text)

    @staticmethod
    def create_dataframe_from_list(data: list) -> pd.DataFrame:
        """Save list of data into dataframe.

        :param list data: Data to save.
        :return: Dataframe.
        :rtype: pd.DataFrame.
        """
        return pd.DataFrame.from_dict(data)

    @staticmethod
    def load_dataframe(filename: str) -> pd.DataFrame:
        """Call load_dataframe function from utils.

        :param: str filename: Name of file to load.
        :return: Dataframe.
        :rtype: pd.DataFrame.
        """
        return load_dataframe(filename)

    @staticmethod
    def save_dataframe(dataframe: pd.DataFrame, filename: str):
        """Call save_dataframe function from utils.

        :param: pd.Dataframe dataframe: Dataframe to save.
        :param: str filename: Filename to save dataframe to.
        """
        save_dataframe(dataframe, filename)

    def _save_data(self):
        """Save data to file."""
        self.save_dataframe(self.dataframe, self.FILE_NAME)
