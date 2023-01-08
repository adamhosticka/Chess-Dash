"""
Fetch usernames from each country from Chess.com API and save it to a file.
"""

import os
import pandas as pd

from app.helpers.paths import DATA_DIR
from app.helpers.api_endpoints import COUNTRY_PLAYERS_ENDPOINT
from app.src.fetch_data.fetch_base import FetchBase
from app.helpers.data_filenames import PLAYERS_FILENAME, COUNTRIES_FILENAME
from app.utils.dataframe_utils import load_dataframe, create_dataframe_from_list


class FetchCountryPlayer(FetchBase):
    FILE_NAME = PLAYERS_FILENAME

    def __init__(self):
        self.countries = load_dataframe(os.path.join(DATA_DIR, COUNTRIES_FILENAME))
        self.players = load_dataframe(os.path.join(DATA_DIR, PLAYERS_FILENAME))

    def fetch_data(self) -> pd.DataFrame:
        """Fetch player usernames for each country, save API status response to countries and usernames to players."""
        players = []
        for code in self.countries['code']:
            item = self.fetch_item(COUNTRY_PLAYERS_ENDPOINT.format(iso=code))
            if 'players' in item:
                for player in item['players']:
                    players.append({
                        'username': player,
                        'country_code': code,
                    })
        res = create_dataframe_from_list(players)
        if not self.players.empty and not res.empty:
            res = pd.merge(self.players, res, how='outer')
        res = res[~res.duplicated(subset='username')]
        return res
