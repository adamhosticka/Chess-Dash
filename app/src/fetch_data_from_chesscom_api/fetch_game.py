"""
Fetch games played by saved players from Chess.com API, merge them with already saved games and save all games to file.
"""

import pandas as pd

from app.helpers.api_endpoints import PLAYER_GAMES_MONTH
from app.helpers.data_filenames import GAMES_FILENAME, PLAYERS_FILENAME
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase


class FetchGame(FetchBase):
    FILE_NAME = GAMES_FILENAME

    def __init__(self, fetch_from_players_cnt: int = 100, year: int = 2022, month: int = 12):
        self.players = self.load_dataframe(PLAYERS_FILENAME)
        self.games = self.load_dataframe(GAMES_FILENAME)
        self.fetch_from_players_cnt = fetch_from_players_cnt
        self.year = year
        self.month = month

    def fetch_data(self):
        games = []
        saved_users = []
        games_date_df_col = f'games_saved_{self.year}_{self.month}'

        if games_date_df_col not in self.players:
            self.players[games_date_df_col] = False
        self.players[self.players[games_date_df_col].isna()][games_date_df_col] = False
        self.players[games_date_df_col] = self.players[games_date_df_col].astype(bool)

        cnt = 0
        for username in self.players[~self.players[games_date_df_col]].head(self.fetch_from_players_cnt)['username']:
            cnt += 1
            print(f"{cnt}. {username}")
            games_item = self.fetch_item(
                PLAYER_GAMES_MONTH.format(username=username, year=self.year, month=self.month)
            )
            if games_item and 'games' in games_item:
                games.extend(games_item['games'])
                saved_users.append(username)

        self.players.loc[self.players['username'].isin(saved_users), games_date_df_col] = True
        self.save_dataframe(self.players, PLAYERS_FILENAME)

        games_df = pd.json_normalize(games, sep='_')
        if self.games.empty:
            self.dataframe = games_df
        else:
            self.dataframe = pd.merge(self.games, games_df, how='outer')


if __name__ == '__main__':
    FetchGame(100).run()
    # for i in range(10):
    #     print(f"{i}. jizda")
    #     try:
    #         FetchGame(100).run()
    #     except Exception as e:
    #         import time
    #         print(f"Skoncila s chybou {str(e)}.")
    #         print(repr(e))
    #         time.sleep(61)
