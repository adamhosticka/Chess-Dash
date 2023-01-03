"""
Base class for fetching data from Chess.com API and saving them to csv file.
"""

import os
import requests
import json
import pandas as pd

from app.definitions import DATA_DIR
from app.helpers.api_endpoints import REQUEST_HEADERS


class FetchBase:
    FILE_NAME = None

    data = []

    def run(self):
        """Fetch data and export them to csv."""
        self.fetch_data()
        self._export_to_csv()

    def fetch_data(self):
        """Call fetch_item, modify the return value and save it to data."""
        pass

    @staticmethod
    def fetch_item(url: str) -> dict:
        """Send request to Chess.com API.

        :param str url: Request url.
        :return: API response item.
        :rtype: dict
        """
        res = requests.get(url, headers=REQUEST_HEADERS)
        item = json.loads(res.text)
        item['status_code'] = res.status_code
        item['etag'] = res.headers.get('etag')
        item['last_modified'] = res.headers.get('last-modified')
        return item

    def _export_to_csv(self):
        """Export data to csv file."""
        df = pd.DataFrame.from_dict(self.data)
        df.to_csv(os.path.join(DATA_DIR, self.FILE_NAME), index=False)
