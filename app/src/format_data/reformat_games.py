import numpy as np
import pandas as pd

from app.helpers.data_filenames import GAMES_FILENAME, REFORMATED_GAMES_FILENAME
from app.utils.load_save_dataframe import load_dataframe, save_dataframe

pd.options.mode.chained_assignment = None  # Disable SettingWithCopyWarning


def reformat_games(games_df: pd.DataFrame) -> pd.DataFrame:
    """Reformat games DataFrame for better working with its data.

    Inspired/copied from
    https://www.kaggle.com/code/adityajha1504/those-features-won-t-engineer-themselves/notebook.

    :param pd.DataFrame games_df: DataFrame to reformat.

    :return: Reformated dataframe.
    :rtype: pd.DataFrame.
    """

    games_df = games_df[games_df['rules'] == 'chess']

    games_df.drop(
        columns=["tcn", "start_time", "end_time", "rules", "tournament", "match", "white_@id", "black_@id",
                 "white_uuid", "black_uuid", "initial_setup"],
        inplace=True, errors='ignore')

    games_df.dropna(axis=0, subset=['pgn'], inplace=True)
    feature_names = ['start_date', 'end_date', 'start_time', 'end_time', 'eco', 'eco_url', 'result']
    feature_positions = [2, -6, -7, -5, -15, -14, 6]

    # Takes in the name you want to give the feature, and the position of the feature in
    # the pgn.split('\n') and creates the feature with feature name in the dataframe
    for feature_name, position in zip(feature_names, feature_positions):
        games_df[feature_name] = games_df['pgn'].apply(
            lambda x: x.split('\n')[position].split('"')[1])

    games_df['start_datetime'] = games_df['start_date'] + " " + games_df['start_time']
    games_df['end_datetime'] = games_df['end_date'] + " " + games_df['end_time']
    games_df['start_datetime'] = pd.to_datetime(games_df['start_datetime'], format="%Y-%m-%d %H:%M:%S")
    games_df['end_datetime'] = pd.to_datetime(games_df['end_datetime'], format="%Y-%m-%d %H:%M:%S")

    games_df['time'], games_df['increment'] = zip(*games_df['time_control'].apply(extract_time_and_increment))

    games_df['eco_name'] = games_df['eco_url'].apply(lambda x: x.split('/')[-1])
    games_df['rating_difference'] = games_df['white_rating'] - games_df['black_rating']

    games_df['white_moves'], games_df['black_moves'], games_df['white_clock'], games_df['black_clock'] = \
        zip(*games_df['pgn'].apply(extract_moves_and_clock))
    games_df['moves_count'] = (games_df['white_moves'].apply(len) + games_df['black_moves'].apply(len)) / 2

    games_df['result_type'] = games_df['white_result'].apply(lambda x: x if x != 'win' else 0)
    idx = games_df[games_df['result_type'] == 0].index
    games_df.loc[idx, 'result_type'] = games_df['black_result'][idx]
    games_df.drop(columns=['white_result', 'black_result'], axis=1, inplace=True)
    games_df['result'] = games_df['result'].apply(
        lambda x: 'Black' if x == '0-1' else ('White' if x == '1-0' else 'Draw'))

    games_df.drop(
        columns=['pgn', 'start_date', 'end_date', 'start_time', 'end_time', 'time_control'],
        axis=1,
        inplace=True
    )

    return games_df


def extract_moves_and_clock(pgn: str) -> tuple:
    """Get moves and clock times from pgn.

    :args: str pgn: Chess pgn.
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


if __name__ == '__main__':
    games = load_dataframe(GAMES_FILENAME)
    reformated_games = reformat_games(games)
    save_dataframe(reformated_games, REFORMATED_GAMES_FILENAME)
