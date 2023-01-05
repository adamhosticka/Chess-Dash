import time

from app.src.fetch_data_from_chesscom_api.fetch_country import FetchCountry
from app.src.fetch_data_from_chesscom_api.fetch_country_player import FetchCountryPlayer
from app.src.fetch_data_from_chesscom_api.fetch_game import FetchGame
from app.src.fetch_data_from_chesscom_api.fetch_player import FetchPlayer

FETCH_SETTINGS = [
    {
        "class": FetchCountry,
        "fetch": False,
        "repeat": 1,
    },
    {
        "class": FetchCountryPlayer,
        "fetch": False,
        "repeat": 1,
    },
    {
        "class": FetchPlayer,
        "fetch": False,
        "repeat": 15,
        "params": {
            "players_cnt": 100,
        },
    },
    {
        "class": FetchGame,
        "fetch": True,
        "repeat": 10,
        "params": {
            "fetch_from_players_cnt": 100,
            "year": 2022,
            "month": 12,
        },
    },
]


def fetch_data(settings: list):
    for item in settings:
        if item['fetch']:
            start_time = time.time()
            for i in range(item['repeat']):
                print(f"{i}. jizda")
                try:
                    item['class'](**item['params']).run()
                except Exception as e:
                    print(f"Skoncila s chybou {repr(e)}.")
                    time.sleep(61)
            print(f"Fetching {str(item['class'])} took {time.time() - start_time} seconds")


if __name__ == '__main__':
    fetch_data(FETCH_SETTINGS)
