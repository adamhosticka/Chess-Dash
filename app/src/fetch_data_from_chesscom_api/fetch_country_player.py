"""
Fetch user information from Chess.com API and save it to csv file.
"""

import os
import pandas as pd

from app.definitions import DATA_DIR
from app.helpers.api_endpoints import COUNTRY_PLAYERS_ENDPOINT
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME, COUNTRIES_FILENAME


class FetchCountryPlayer(FetchBase):
    FILE_NAME = PLAYERS_FILENAME
    # Max value = 1000
    PLAYER_LIMIT_PER_COUNTRY = 1

    def __init__(self):
        self.countries = pd.read_csv(os.path.join(DATA_DIR, COUNTRIES_FILENAME))

    def fetch_data(self):
        """Fetch player usernames for each country, save API status response to countries and usernames to players."""
        players = []
        country_player_response = []
        for code in self.countries['code']:
            item = self.fetch_item(COUNTRY_PLAYERS_ENDPOINT.format(iso=code))
            players_cnt = 0
            if 'players' in item:
                players_cnt = max(self.PLAYER_LIMIT_PER_COUNTRY, len(item['players']))
                for player in item['players'][:self.PLAYER_LIMIT_PER_COUNTRY]:
                    players.append({
                        'username': player,
                        'country_code': code,
                    })
            country_player_response.append({
                'code': code,
                'saved_players_cnt': players_cnt,
                'players_status_code': item['status_code'],
                'players_etag': item['etag'],
                'players_last_modified': item['last_modified'],
            })
        self.countries = pd.merge(
            self.countries,
            pd.DataFrame.from_dict(country_player_response),
            how='left',
            on='code',
        )
        self.countries.to_csv(os.path.join(DATA_DIR, COUNTRIES_FILENAME), index=False)
        self.save_dataframe(players)


if __name__ == '__main__':
    FetchCountryPlayer().run()
