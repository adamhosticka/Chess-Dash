"""Reformat games DataFrame.
Inspired/copied from https://www.kaggle.com/code/adityajha1504/those-features-won-t-engineer-themselves/notebook.
"""

import numpy as np
import pandas as pd

from app.helpers.data_filenames import GAMES_FILENAME, REFORMATED_GAMES_FILENAME
from app.utils.load_save_dataframe import load_dataframe, save_dataframe


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

    df['eco_name'] = get_eco_names(df)

    df['white_moves'], df['black_moves'], df['white_clock'], df['black_clock'] = \
        zip(*df['pgn'].apply(extract_moves_and_clock))
    df['moves_count'] = (df['white_moves'].apply(len) + df['black_moves'].apply(len)) / 2

    df = unite_results(df)

    df.drop(
        columns=['white_result', 'black_result', 'pgn', 'start_date', 'end_date',
                 'start_time', 'end_time', 'time_control'],
        axis=1,
        inplace=True
    )

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
    return df


def get_eco_names(df: pd.DataFrame) -> pd.Series:
    """Get eco names from eco urls.

    :param: pd.DataFrame df: Dataframe with eco urls.
    :return: Series of eco names.
    :rtype: pd.Series.
    """
    return df['eco_url'].apply(lambda x: x.split('/')[-1])


def extract_moves_and_clock(pgn: str) -> tuple:
    """Get moves and clock times from pgn.

    :param: str pgn: Chess pgn.
    :return: White moves, black moves, white clock, black clock.
    :rtype: tuple.
    """
    if pgn.find('{[') == -1:
        return pgn.split("\n")[-2].split()[1::3], pgn.split("\n")[-2].split()[2::3], np.nan, np.nan
    else:
        return pgn.split("\n")[-2].split()[1::8], pgn.split("\n")[-2].split()[5::8], \
            [x[:-2] for x in pgn.split("\n")[-2].split()[3::8]], \
            [x[:-2] for x in pgn.split("\n")[-2].split()[7::8]]


def extract_time_and_increment(time_control: str):
    if time_control[:2] == '1/':
        return 1, 0
    else:
        splitted = time_control.split('+')
        if len(splitted) == 1:
            return splitted[0], 0
        else:
            return time_control.split('+')[0], time_control.split('+')[1]


def unite_results(df: pd.DataFrame) -> pd.DataFrame:
    """Combine white result, black result and result type into two columns.

    :param: pd.DataFrame df: Dataframe with white_result and black_result.
    :return: Dataframe with result.
    :rtype: pd.DataFrame.
    """
    df['result_type'] = df['white_result'].apply(lambda x: x if x != 'win' else 0)
    idx = df[df['result_type'] == 0].index
    df.loc[idx, 'result_type'] = df['black_result'][idx]
    df['result'] = df['result'].apply(
        lambda x: 'Black' if x == '0-1' else ('White' if x == '1-0' else 'Draw'))
    return df


if __name__ == '__main__':
    games = load_dataframe(GAMES_FILENAME)
    reformated_games = reformat_games(games)
    # save_dataframe(reformated_games, REFORMATED_GAMES_FILENAME)
