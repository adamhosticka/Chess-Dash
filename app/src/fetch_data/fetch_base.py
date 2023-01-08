"""Base class for fetching data from Chess.com API and saving them to a file."""

import sys
import json
import pandas as pd
import requests

from app.helpers.api_endpoints import REQUEST_HEADERS
from app.utils.dataframe_utils import save_dataframe


class FetchBase:
    """Base class for fetching data from Chess.com API and saving them to a file."""

    FILE_NAME = None

    dataframe = pd.DataFrame()

    def run(self):
        """Fetch data and export them to csv."""
        self.dataframe = self.fetch_data()
        self._save_data()

    def fetch_data(self) -> pd.DataFrame:
        """Call fetch_item, modify the return values and return them.

        :return: Dataframe with fetched data.
        :rtype: pd.DataFrame.
        """
        # Disable pylint E1111
        raise NotImplementedError

    @staticmethod
    def fetch_item(url: str) -> dict:
        """Send request to Chess.com API.

        :param str url: Request url.
        :return: API response item.
        :rtype: dict.
        """
        res = requests.get(url, headers=REQUEST_HEADERS, timeout=10)
        if res.status_code != 200:
            print(f"WARNING: Status code {res.status_code} for url: {url}.")
            if res.status_code == 429:  # Rate limit
                print("Rate limit exceeded -> exiting.")
                sys.exit(1)
            return None
        return json.loads(res.text)

    def _save_data(self):
        """Save data to file."""
        save_dataframe(self.dataframe, self.FILE_NAME)
