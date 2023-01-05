"""
Fetch username for each country from Chess.com API and save it to a file.
"""

import os
import pandas as pd

from app.helpers.paths import DATA_DIR
from app.helpers.api_endpoints import COUNTRY_PLAYERS_ENDPOINT
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME, COUNTRIES_FILENAME


class FetchCountryPlayer(FetchBase):
    FILE_NAME = PLAYERS_FILENAME

    def __init__(self):
        self.countries = self.load_dataframe(os.path.join(DATA_DIR, COUNTRIES_FILENAME))
        self.players = self.load_dataframe(os.path.join(DATA_DIR, PLAYERS_FILENAME))

    def fetch_data(self):
        """Fetch player usernames for each country, save API status response to countries and usernames to players."""
        players = []
        for code in self.countries['code']:
            item = self.fetch_item(COUNTRY_PLAYERS_ENDPOINT.format(iso=code))
            if 'players' in item:
                for player in item['players']:
                    players.append({
                        'username': player,
                        'country_code': code,
                    })
        if not players:
            exit(1)
        self.dataframe = self.create_dataframe_from_list(players)
        if not self.players.empty and not self.dataframe.empty:
            self.dataframe = pd.merge(self.players, self.dataframe, how='outer')
        self.dataframe = self.dataframe[~self.dataframe.duplicated(subset='username')]


if __name__ == '__main__':
    FetchCountryPlayer().run()
