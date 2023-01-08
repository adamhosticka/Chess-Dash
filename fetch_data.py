"""Fetch data from Chess.com API and reformat games."""

import time
from argparse import ArgumentParser

from app.src.fetch_data.fetch_country import FetchCountry
from app.src.fetch_data.fetch_country_player import FetchCountryPlayer
from app.src.fetch_data.fetch_game import FetchGame
from app.src.fetch_data.fetch_player import FetchPlayer
from app.src.format_data.reformat_games import save_reformated_games


def fetch_item(data_class, print_info: bool, cnt: int = 1):
    start_time = time.time()
    for i in range(cnt):
        if print_info and cnt != 1:
            print(f"{i + 1}. stovka.")
        try:
            data_class().run()
        except Exception as e:
            if print_info:
                print(f"Skoncila s chybou {repr(e)}.")
    if print_info:
        print(f"Fetching {str(data_class)} took {time.time() - start_time} seconds")


def fetch_data(fetch_countries: bool = False, fetch_country_players: bool = False, hundreds_of_players: int = 0,
               hundreds_of_games: int = 0, reformat_and_save: bool = False, print_info: bool = False):
    """Fetch data from Chess.com API based on input switches.

    :param: bool fetch_countries: Fetch countries switch.
    :param: bool fetch_country players: Fetch country players switch.
    :param: int hundreds_of_players: Number of hundreds of players to fetch.
    :param: int hundreds_of_games: Number of hundreds of games to fetch.
    :param: bool reformat_and_save: Reformat and save games switch.
    :param: bool print_info: Print fetching info switch.
    """
    if fetch_countries:
        fetch_item(FetchCountry, print_info)

    if fetch_country_players:
        fetch_item(FetchCountryPlayer, print_info)

    if hundreds_of_players > 0:
        fetch_item(FetchPlayer, print_info, hundreds_of_players)

    if hundreds_of_games > 0:
        fetch_item(FetchGame, print_info, hundreds_of_games)

    if reformat_and_save:
        save_reformated_games()


if __name__ == '__main__':
    parser = ArgumentParser(description="Fetch data from Chess.com API and reformat games.")
    parser.add_argument("-fc", "--fetch-countries",
                        default=False,
                        action='store_true',
                        help="Fetch countries")
    parser.add_argument("-fcp", "--fetch-country-players",
                        default=False,
                        action='store_true',
                        help="Fetch country players")
    parser.add_argument("-FP", "--hundreds-of-players",
                        default=0,
                        choices=range(0, 50),
                        type=int,
                        help="Number of hundreds of players to fetch")
    parser.add_argument("-FG", "--hundreds-of-games",
                        default=0,
                        choices=range(0, 50),
                        type=int,
                        help="Number of hundreds of games to fetch")
    parser.add_argument("-r", "--reformat-and-save",
                        default=False,
                        action='store_true',
                        help="Reformat fetched games after fetching and save them to another file")
    parser.add_argument("-p", "--print-info",
                        default=False,
                        action='store_true',
                        help="Print fetching information")
    args = parser.parse_args()

    fetch_data(**vars(args))
