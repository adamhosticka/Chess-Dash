"""
Fetch games played by saved players from Chess.com API and save it to csv
"""

import os
import pandas as pd
import numpy as np

from app.definitions import DATA_DIR
from app.helpers.api_endpoints import PLAYER_MONTHLY_ARCHIVES
from app.helpers.data_filenames import GAMES_FILENAME, PLAYERS_FILENAME
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase


class FetchGame(FetchBase):
    FILE_NAME = GAMES_FILENAME
    LAST_X_ARCHIVES = 1

    def __init__(self):
        self.players = pd.read_csv(os.path.join(DATA_DIR, PLAYERS_FILENAME))

    def fetch_data(self):
        games = []
        cnt = 0
        for username in self.players['username']:
            cnt += 1
            print(cnt)
            archives_item = self.fetch_item(PLAYER_MONTHLY_ARCHIVES.format(username=username))
            for archive in archives_item['archives'][-self.LAST_X_ARCHIVES:]:
                games_item = self.fetch_item(archive)
                games.extend(games_item['games'])
        games_df = pd.DataFrame.from_dict(games)
        self.reformat_games_df(games_df)
        self.dataframe = games_df
        print("GamesCount", len(self.dataframe))

    @staticmethod
    def reformat_games_df(games_df: pd.DataFrame):
        """Reformat games DataFrame for better working with its data

        Inspired/copied from https://www.kaggle.com/code/adityajha1504/those-features-won-t-engineer-themselves/notebook

        :param pd.DataFrame games_df: DataFrame to reformat
        """

        players = ['white', 'black']
        attributes = ['rating', 'result', 'username']
        for player in players:
            for attribute in attributes:
                games_df[f"{player}_{attribute}"] = games_df[player].apply(
                    lambda x: x.get(attribute)
                )

        games_df.drop(columns=["tcn", "start_time", "end_time", "white", "black"], inplace=True)

        games_df.dropna(axis=0, subset=['pgn'], inplace=True)
        feature_names = ['start_date', 'end_date', 'start_time', 'game_url', 'end_time', 'eco', 'eco_url', 'result']
        feature_positions = [2, -6, -7, -4, -5, -15, -14, 6]

        # Takes in the name you want to give the feature, and the position of the feature in
        # the pgn.split('\n') and creates the feature with feature name in the dataframe
        for feature_name, position in zip(feature_names, feature_positions):
            games_df[feature_name] = games_df['pgn'].apply(
                lambda x: x.split('\n')[position].split('"')[1])

        games_df['eco_name'] = games_df['eco_url'].apply(lambda x: x.split('/')[-1])

        def extract_moves_and_clock(pgn):
            if pgn.find('{[') == -1:
                return pgn.split("\n")[-2].split()[1::3], pgn.split("\n")[-2].split()[2::3], np.nan, np.nan
            else:
                return pgn.split("\n")[-2].split()[1::8], pgn.split("\n")[-2].split()[5::8], \
                       [x[:-2] for x in pgn.split("\n")[-2].split()[3::8]], \
                       [x[:-2] for x in pgn.split("\n")[-2].split()[7::8]]

        games_df['white_moves'], games_df['black_moves'], games_df['white_clock'], games_df['black_clock'] = \
            zip(*games_df['pgn'].apply(extract_moves_and_clock))

        # games_df['result_type'] = games_df['white_result'].apply(lambda x: x if x != 'win' else 0)
        # idx = games_df[games_df['result_type'] == 0].index
        # games_df.loc[idx, 'result_type'] = games_df['black_result'][idx]
        # games_df.drop(columns=['white_result', 'black_result'], axis=1, inplace=True)

        games_df.drop(columns=['pgn'], inplace=True)


if __name__ == '__main__':
    import time
    start_time = time.time()
    FetchGame().run()
    print("--- %s seconds ---" % (time.time() - start_time))
