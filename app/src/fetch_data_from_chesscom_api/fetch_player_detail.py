"""
Fetch players from all players from all countries from Chess.com API and save it to a file.
"""

import pandas as pd

from app.helpers.api_endpoints import PLAYER_PROFILE_ENDPOINT
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME


class FetchPlayerDetail(FetchBase):
    FILE_NAME = PLAYERS_FILENAME

    def __init__(self):
        self.players = self.load_dataframe(PLAYERS_FILENAME)

    def fetch_data(self):
        player_details = []
        for username in self.players['username']:
            player_details.append(self.fetch_item(PLAYER_PROFILE_ENDPOINT.format(username=username)))
        player_details_df = pd.DataFrame.from_dict(player_details)
        player_details_df.drop(
            columns=['location', 'is_streamer', 'twitch_url', 'verified', 'title', 'name', 'avatar'],
            axis=1,
            inplace=True,
            errors='ignore'
        )
        player_details_df.rename(columns={"country": "country_@id"}, inplace=True)
        player_details_df = self.remove_same_columns_from_right(self.players, player_details_df, 'username')
        self.dataframe = pd.merge(
            self.players,
            player_details_df,
            how='left',
            on='username'
        )


if __name__ == '__main__':
    FetchPlayerDetail().run()
