"""
Fetch players from all players from all countries from Chess.com API and save it to csv
"""

import os
import pandas as pd

from app.helpers.api_endpoints import PLAYER_STATS_ENDPOINT
from app.definitions import DATA_DIR
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME


class FetchPlayerStats(FetchBase):
    FILE_NAME = PLAYERS_FILENAME

    def __init__(self):
        self.players = pd.read_csv(os.path.join(DATA_DIR, PLAYERS_FILENAME))

    def fetch_data(self):
        player_stats = []
        for username in self.players['username']:
            player_stats_item = self.fetch_item(PLAYER_STATS_ENDPOINT.format(username=username))
            player_stats_item['username'] = username
            player_stats.append(player_stats_item)
        player_stats_df = pd.json_normalize(player_stats, sep="_")
        player_stats_df.drop(
            columns=['fide', 'chess960_daily_record_time_per_move', 'chess960_daily_record_timeout_percent',
                     'chess_daily_record_time_per_move', 'chess_daily_record_timeout_percent'],
            axis=1, inplace=True, errors='ignore')

        player_stats_df = self.remove_same_columns_from_right(self.players, player_stats_df, 'username')
        self.dataframe = pd.merge(
            self.players,
            player_stats_df,
            how='left',
            on='username'
        )


if __name__ == '__main__':
    FetchPlayerStats().run()
