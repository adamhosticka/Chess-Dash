"""
Fetch players details and stats from Chess.com API, merge ot with already saved player and save it to a file.
"""

import pandas as pd

from app.helpers.api_endpoints import PLAYER_PROFILE_ENDPOINT, PLAYER_STATS_ENDPOINT
from app.helpers.players_keep_columns_rename import PLAYERS_KEEP_COLUMNS_RENAME
from app.src.fetch_data.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME
from app.utils.dataframe_utils import load_dataframe


class FetchPlayer(FetchBase):
    """
    Fetch players details and stats from Chess.com API, merge ot with already saved player and save it to a file.
    """

    FILE_NAME = PLAYERS_FILENAME
    KEEP_COLUMNS_RENAME = PLAYERS_KEEP_COLUMNS_RENAME

    def __init__(self, players_cnt: int = 100):
        self.players = load_dataframe(PLAYERS_FILENAME)
        self.players_cnt = players_cnt

    def fetch_data(self) -> pd.DataFrame:
        players = []

        original_players_plain = True
        if 'player_id' in self.players:
            original_players_plain = False
            fetch_players_df = self.players[self.players['player_id'].isna()].sample(n=self.players_cnt)
        else:
            fetch_players_df = self.players.sample(n=self.players_cnt)

        for username, country_code in fetch_players_df[['username', 'country_code']].itertuples(index=False):
            player = self.fetch_item(PLAYER_PROFILE_ENDPOINT.format(username=username))
            if player:
                player_stats = self.fetch_item(PLAYER_STATS_ENDPOINT.format(username=username))
                player.update(player_stats)
                player['country_code'] = country_code
                players.append(player)

        res = pd.json_normalize(players, sep='_')
        keep_columns_intersected = list(set(self.KEEP_COLUMNS_RENAME.keys()).intersection(set(res.columns)))
        res = res[keep_columns_intersected]
        keep_columns_intersected_rename = {k: v for k, v in self.KEEP_COLUMNS_RENAME.items()
                                           if k in keep_columns_intersected}
        res.rename(columns=keep_columns_intersected_rename, inplace=True, errors='ignore')

        if original_players_plain:
            return pd.merge(self.players, res, how='outer')

        res = pd.merge(self.players, res, how='outer')
        return res[~(
                  res.duplicated(subset='username', keep=False) &
                  res['player_id'].isna()
        )]
