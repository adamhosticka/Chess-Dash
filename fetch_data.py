"""Fetch data from Chess.com API and reformat games."""

import time
from argparse import ArgumentParser

from app.src.fetch_data.fetch_country import FetchCountry
from app.src.fetch_data.fetch_country_player import FetchCountryPlayer
from app.src.fetch_data.fetch_game import FetchGame
from app.src.fetch_data.fetch_player import FetchPlayer
from app.src.format_data.reformat_games import save_reformated_games


def get_data_class_name(data_class) -> str:
    """Get data class name.

    :param: data_class: Data class.
    :return: Data class name.
    :rtype: str.
    """
    return str(data_class).rsplit('.', maxsplit=1)[-1][:-2]


def fetch_item(data_class, print_info: bool, cnt: int = 1):
    """Fetch data by data_class class.

    :param: data_class: Fetching data class.
    :param: bool print_info: Print info if True.
    :param: int cnt: How many times to call data_class.run().
    """
    start_time = time.time()
    if print_info:
        print(f"Fetching {get_data_class_name(data_class)}")
    for i in range(cnt):
        if print_info and cnt != 1:
            print(f"{i + 1}. stovka.")
        try:
            data_class().run()
        except Exception as e:
            if print_info:
                print(f"Skoncila s chybou {repr(e)}.")
    if print_info:
        print(f"Fetching {get_data_class_name(data_class)} took {time.time() - start_time} seconds")


def fetch_data(fetch_all_and_reformat: bool, fetch_countries: bool, fetch_country_players: bool,
               hundreds_of_players: int, hundreds_of_games: int, reformat_and_save: bool, disable_print_info: bool):
    """Fetch data from Chess.com API based on input switches.

    :param: bool fetch_countries: Fetch countries switch.
    :param: bool fetch_country players: Fetch country players switch.
    :param: int hundreds_of_players: Number of hundreds of players to fetch.
    :param: int hundreds_of_games: Number of hundreds of games to fetch.
    :param: bool reformat_and_save: Reformat and save games switch.
    :param: bool print_info: Print fetching info switch.
    """
    if fetch_all_and_reformat:
        fetch_countries = True
        fetch_country_players = True
        hundreds_of_players = 10
        hundreds_of_games = 5
        reformat_and_save = True

    if disable_print_info:
        print("Fetching...")

    if fetch_countries:
        fetch_item(FetchCountry, disable_print_info)

    if fetch_country_players:
        fetch_item(FetchCountryPlayer, disable_print_info)

    if hundreds_of_players > 0:
        fetch_item(FetchPlayer, disable_print_info, hundreds_of_players)

    if hundreds_of_games > 0:
        fetch_item(FetchGame, disable_print_info, hundreds_of_games)

    if reformat_and_save:
        if disable_print_info:
            print("Reformating games...")
        save_reformated_games()


if __name__ == '__main__':
    parser = ArgumentParser(description="Fetch data from Chess.com API and reformat games.")
    parser.add_argument("-far", "--fetch-all-and-reformat",
                        default=False,
                        action='store_true',
                        help="Fetch countries, players (1000) and games (500) - then reformat them. "
                             "Takes around twenty minutes.")
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
                        choices=range(0, 101),
                        type=int,
                        help="Number of hundreds of players to fetch")
    parser.add_argument("-FG", "--hundreds-of-games",
                        default=0,
                        choices=range(0, 51),
                        type=int,
                        help="Number of hundreds of players to fetch games from (each player can have multiple games)")
    parser.add_argument("-r", "--reformat-and-save",
                        default=False,
                        action='store_true',
                        help="Reformat fetched games after fetching and save them to another file")
    parser.add_argument("-p", "--disable-print-info",
                        default=True,
                        action='store_true',
                        help="Disable printing fetching information")
    args = parser.parse_args()

    fetch_data(**vars(args))
