"""
Fetch user information from Chess.com API and save it to csv file
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
        self.fetch_data()
        self._export_to_csv()

    def fetch_data(self):
        pass

    @staticmethod
    def fetch_item(url: str) -> dict:
        res = requests.get(url, headers=REQUEST_HEADERS)
        item = json.loads(res.text)
        item['status_code'] = res.status_code
        item['etag'] = res.headers.get('etag')
        item['last_modified'] = res.headers.get('last-modified')
        print(item)
        return item

    def _export_to_csv(self):
        df = pd.DataFrame.from_dict(self.data)
        df.to_csv(os.path.join(DATA_DIR, self.FILE_NAME), index=False)
