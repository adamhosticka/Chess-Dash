"""
Fetch players from all players from all countries from Chess.com API and save it to csv
"""

import os
import pandas as pd

from app.helpers.api_endpoints import PLAYER_PROFILE_ENDPOINT
from app.definitions import DATA_DIR
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME


class FetchPlayerDetail(FetchBase):
    FILE_NAME = PLAYERS_FILENAME

    def __init__(self):
        self.players = pd.read_csv(os.path.join(DATA_DIR, PLAYERS_FILENAME))

    def fetch_data(self):
        players = []
        for username in self.players['username']:
            print(username)
            players.append(self.fetch_item(PLAYER_PROFILE_ENDPOINT.format(username=username)))
        player_details = pd.DataFrame.from_dict(players)
        player_details.drop(
            columns=['location', 'is_streamer', 'twitch_url', 'verified', 'title', 'name', 'avatar'],
            axis=1,
            inplace=True,
            errors='ignore'
        )
        player_details.rename(columns={"country": "country_@id"}, inplace=True)
        self.dataframe = pd.merge(
            player_details,
            self.players,
            how='left',
            on='username'
        )


if __name__ == '__main__':
    FetchPlayerDetail().run()
