"""
Fetch games played by saved players from Chess.com API and save it to csv
"""

import os
import pandas as pd

from app.definitions import DATA_DIR
from app.helpers.api_endpoints import PLAYER_MONTHLY_ARCHIVES
from app.helpers.data_filenames import GAMES_FILENAME, PLAYERS_FILENAME
from app.src.fetch_data_from_chesscom_api.fetch_base import FetchBase
from app.src.format_data.reformat_games import reformat_games


class FetchGame(FetchBase):
    FILE_NAME = GAMES_FILENAME

    def __init__(self, archives_cnt: int = 1):
        self.players = pd.read_csv(os.path.join(DATA_DIR, PLAYERS_FILENAME))
        self.archives_to_fetch_cnt = archives_cnt

    def fetch_data(self):
        games = []
        for username in self.players['username']:
            archives_item = self.fetch_item(PLAYER_MONTHLY_ARCHIVES.format(username=username))
            archive_cnt = min(len(archives_item['archives']), self.archives_to_fetch_cnt)
            for archive in archives_item['archives'][-archive_cnt:]:
                games_item = self.fetch_item(archive)
                games.extend(games_item['games'])
        games_df = pd.json_normalize(games, sep='_')
        games_df = reformat_games(games_df)
        self.dataframe = games_df


if __name__ == '__main__':
    import time
    start_time = time.time()
    FetchGame().run()
    print("--- %s seconds ---" % (time.time() - start_time))
