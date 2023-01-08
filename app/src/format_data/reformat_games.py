"""Reformat games from official Chess.com API format and save them.
Inspired/copied from https://www.kaggle.com/code/adityajha1504/those-features-won-t-engineer-themselves/notebook.
"""

import numpy as np
import pandas as pd

from app.helpers.data_filenames import GAMES_FILENAME, REFORMATED_GAMES_FILENAME
from app.utils.dataframe_utils import load_dataframe, save_dataframe


def save_reformated_games():
    """Save reformated games"""
    games = load_dataframe(GAMES_FILENAME)
    reformated_games = reformat_games(games)
    save_dataframe(reformated_games, REFORMATED_GAMES_FILENAME)


def reformat_games(games_df: pd.DataFrame) -> pd.DataFrame:
    """Reformat games DataFrame for better working with its data.

    :param pd.DataFrame games_df: DataFrame to reformat.

    :return: Reformated dataframe.
    :rtype: pd.DataFrame.
    """

    df = games_df.copy()

    df = df[df['rules'] == 'chess']

    df.drop(
        columns=["tcn", "start_time", "end_time", "rules", "tournament", "match", "white_@id", "black_@id",
                 "white_uuid", "black_uuid", "initial_setup"],
        inplace=True, errors='ignore')

    df.dropna(axis=0, subset=['pgn'], inplace=True)

    df = extract_features_from_pgn(df)

    df = compute_datetimes(df)

    df['time'], df['increment'] = zip(*df['time_control'].apply(extract_time_and_increment))

    df['eco_name'] = get_eco_names(df['eco_url'])

    df['white_moves'], df['black_moves'], df['white_clock'], df['black_clock'] = \
        zip(*df['pgn'].apply(extract_moves_and_clock))
    df['moves_count'] = (df['white_moves'].apply(len) + df['black_moves'].apply(len)) / 2

    df = unite_results(df)

    df.drop(columns=['pgn', 'time_control'], axis=1, inplace=True)

    return df


def extract_features_from_pgn(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts the feature name at the feature position to dataframe.

    :param: pd.DataFrame df: Game dataframe.
    :return: Dataframe with features from pgn.
    :rtype: pd.DataFrame.
    """
    feature_names = ['start_date', 'end_date', 'start_time', 'end_time', 'eco', 'eco_url', 'result']
    feature_positions = [2, -6, -7, -5, -15, -14, 6]

    for feature_name, position in zip(feature_names, feature_positions):
        df[feature_name] = df['pgn'].apply(
            lambda x: x.split('\n')[position].split('"')[1])
    return df


def compute_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    """Computes the start/end game datetime from date and time.

    :param: pd.DataFrame df: Game dataframe.
    :return: Game dataframe with computed start_datetime and end_datetime.
    :rtype: pd.DataFrame.
    """
    df['start_datetime'] = df['start_date'] + " " + df['start_time']
    df['end_datetime'] = df['end_date'] + " " + df['end_time']
    df['start_datetime'] = pd.to_datetime(df['start_datetime'], format="%Y-%m-%d %H:%M:%S")
    df['end_datetime'] = pd.to_datetime(df['end_datetime'], format="%Y-%m-%d %H:%M:%S")
    return df.drop(columns=['start_date', 'end_date', 'start_time', 'end_time'])


def get_eco_names(eco_urls: pd.Series) -> pd.Series:
    """Get eco names from eco urls.

    :param: pd.DataFrame df: Dataframe with eco urls.
    :return: Series of eco names.
    :rtype: pd.Series.
    """
    return eco_urls.apply(lambda x: x.split('/')[-1])


def extract_moves_and_clock(pgn: str) -> tuple:
    """Get moves and clock times from pgn.

    :param: str pgn: Chess pgn.
    :return: White moves, black moves, white clock, black clock.
    :rtype: tuple.
    """
    if pgn.find('{[') == -1:
        white_moves = pgn.split("\n")[-2].split()[1::3]
        black_moves = pgn.split("\n")[-2].split()[2::3]
        white_clock = np.nan
        black_clock = np.nan
    else:
        white_moves = pgn.split("\n")[-2].split()[1::8]
        black_moves = pgn.split("\n")[-2].split()[5::8]
        white_clock = [x[:-2] for x in pgn.split("\n")[-2].split()[3::8]]
        black_clock = [x[:-2] for x in pgn.split("\n")[-2].split()[7::8]]
    results = ['1-0', '0-1', '1/2-1/2']
    if white_moves and white_moves[-1] in results:
        white_moves.pop()
    if black_moves and black_moves[-1] in results:
        black_moves.pop()
    return white_moves, black_moves, white_clock, black_clock


def extract_time_and_increment(time_control: str) -> tuple:
    """Extract time and increment from time_control. Daily chess are in format 1/max_for_one_move. Those will be
    extracted as time=1, increment=0.

    :param: str time_control: Time control.
    :return: Time and increment.
    :rtype: tuple.
    """
    if time_control[:2] == '1/':
        return 1, 0
    else:
        splitted = time_control.split('+')
        if len(splitted) == 1:
            return int(splitted[0]), 0
        else:
            return int(time_control.split('+')[0]), int(time_control.split('+')[1])


def unite_results(df: pd.DataFrame) -> pd.DataFrame:
    """Combine white result, black result and result type into two columns.

    :param: pd.DataFrame df: Dataframe with columns result, white_result and black_result.
    :return: Dataframe with result.
    :rtype: pd.DataFrame.
    """
    df['result_type'] = df['white_result'].apply(lambda x: x if x != 'win' else 0)
    idx = df[df['result_type'] == 0].index
    df.loc[idx, 'result_type'] = df['black_result'][idx]
    df['result'] = df['result'].apply(
        lambda x: 'Black' if x == '0-1' else ('White' if x == '1-0' else 'Draw'))
    return df.drop(columns=['white_result', 'black_result'])
