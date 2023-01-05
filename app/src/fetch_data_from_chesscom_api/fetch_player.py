"""
Fetch players details and stats from Chess.com API, merge ot with already saved player and save it to a file.
"""

import pandas as pd

from app.helpers.api_endpoints import PLAYER_PROFILE_ENDPOINT, PLAYER_STATS_ENDPOINT
from app.helpers.players_keep_columns_rename import PLAYERS_KEEP_COLUMNS_RENAME
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME


class FetchPlayer(FetchBase):
    FILE_NAME = PLAYERS_FILENAME
    KEEP_COLUMNS_RENAME = PLAYERS_KEEP_COLUMNS_RENAME

    def __init__(self, players_cnt: int = 10):
        self.players = self.load_dataframe(PLAYERS_FILENAME)
        self.players_cnt = players_cnt

    def fetch_data(self):
        players = []

        original_players_plain = True
        if 'player_id' in self.players:
            original_players_plain = False
            fetch_players_df = self.players[self.players['player_id'].isna()].head(self.players_cnt)
        else:
            fetch_players_df = self.players.head(self.players_cnt)

        # cnt = 0
        for username, country_code in fetch_players_df[['username', 'country_code']].itertuples(index=False):
            # cnt += 1
            # print(cnt)

            player = self.fetch_item(PLAYER_PROFILE_ENDPOINT.format(username=username))
            if player:
                player_stats = self.fetch_item(PLAYER_STATS_ENDPOINT.format(username=username))
                player.update(player_stats)
                player['country_code'] = country_code
                players.append(player)

        self.dataframe = pd.json_normalize(players, sep='_')
        keep_columns_intersected = list(set(self.KEEP_COLUMNS_RENAME.keys()).intersection(set(self.dataframe.columns)))
        self.dataframe = self.dataframe[keep_columns_intersected]
        keep_columns_intersected_rename = {k: v for k, v in self.KEEP_COLUMNS_RENAME.items()
                                           if k in keep_columns_intersected}
        self.dataframe.rename(columns=keep_columns_intersected_rename, inplace=True, errors='ignore')

        if original_players_plain:
            self.dataframe = pd.merge(self.players, self.dataframe, how='outer')
        else:
            self.dataframe = pd.merge(self.players, self.dataframe, how='outer')
            self.dataframe = self.dataframe[~(
                      self.dataframe.duplicated(subset='username', keep=False) &
                      self.dataframe['player_id'].isna()
            )]


if __name__ == '__main__':
    for i in range(1):
        print(f"{i}. jizda")
        try:
            FetchPlayer(8).run()
        except Exception as e:
            import time
            print(f"Skoncila s chybou {str(e)}.")
            print(repr(e))
            time.sleep(61)
