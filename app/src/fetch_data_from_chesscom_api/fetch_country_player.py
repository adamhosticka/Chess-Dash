"""
Fetch user information from Chess.com API and save it to csv file
"""

import os
import pandas as pd

from app.definitions import DATA_DIR
from app.helpers.api_endpoints import COUNTRY_PLAYERS_ENDPOINT
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.src.fetch_data_from_chesscom_api.fetch_country import FetchCountry


class FetchCountryPlayer(FetchBase):
    FILE_NAME = "country_players.csv"

    def __init__(self):
        self.countries = pd.read_csv(os.path.join(DATA_DIR, FetchCountry.FILE_NAME))

    def fetch_data(self):
        for code in self.countries['code']:
            item = self.fetch_item(COUNTRY_PLAYERS_ENDPOINT.format(iso=code))
            item.pop('message', '')
            item.pop('comment', '')
            self.data.append(item)


if __name__ == '__main__':
    FetchCountryPlayer().run()
