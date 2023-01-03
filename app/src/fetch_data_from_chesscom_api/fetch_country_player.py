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

    def __init__(self, player_limit_per_country: int = 1):
        self.countries = pd.read_csv(os.path.join(DATA_DIR, COUNTRIES_FILENAME))
        self.player_limit_per_country = player_limit_per_country  # max value 1000

    def fetch_data(self):
        """Fetch player usernames for each country, save API status response to countries and usernames to players."""
        players = []
        country_player_response = []
        for code in self.countries['code']:
            item = self.fetch_item(COUNTRY_PLAYERS_ENDPOINT.format(iso=code))
            players_cnt = 0
            if 'players' in item:
                players_cnt = max(self.player_limit_per_country, len(item['players']))
                for player in item['players'][:self.player_limit_per_country]:
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
        country_player_df = pd.DataFrame.from_dict(country_player_response)
        country_player_df = self.remove_same_columns_from_right(self.countries, country_player_df, 'code')
        self.countries = pd.merge(
            self.countries,
            country_player_df,
            how='left',
            on='code',
        )
        self.countries.to_csv(os.path.join(DATA_DIR, COUNTRIES_FILENAME), index=False)
        self.save_dataframe(players)


if __name__ == '__main__':
    FetchCountryPlayer().run()
