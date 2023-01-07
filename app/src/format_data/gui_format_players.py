"""Format players DataFrame for gui graphs."""

from typing import Union
import numpy as np
import pandas as pd
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3


def get_time_class_selector_options(df: pd.DataFrame, tactics_and_puzzles: bool) -> list:
    """Get time class options for dropdown.

    :arg: pd.DataFrame df: Player dataframe.
    :arg: bool tactics_and_puzzles: True if tactics and puzzles should be included.
    :return: List of dropdown options.
    :rtype: list.
    """
    time_class_cols = [col for col in df.columns if col.find("_rating") != -1 and col.find("tactics") == -1]
    if tactics_and_puzzles:
        time_class_cols.extend(['tactics_highest_rating', 'puzzle_rush_best_score'])
    return [
        {"label": col.split("_")[0].title(), "value": col}
        for col in time_class_cols
    ]


def convert_alpha2_code_to_alpha3(code: str) -> Union[str, float]:
    """Convert two digit country code to three digit country code.

    :arg: str code: Two digit country code.
    :return: Three digit country code if code exists, numpy nan otherwise.
    """
    try:
        return country_name_to_country_alpha3(country_alpha2_to_country_name(code))
    except KeyError:
        return np.nan


def get_players_count_per_country(df: pd.DataFrame) -> pd.DataFrame:
    """Get players count per country.

    :arg: pd.DataFrame df: Dataframe with columns country and username.
    :return: Dataframe grouped by country with column players count.
    :rtype: pd.DataFrame.
    """
    return df.groupby('country')['username'].count().rename('players count').reset_index()


def get_players_rating_per_country_and_time_class(df: pd.DataFrame, time_class: str) -> pd.DataFrame:
    """Get players count per country from columns country and username.

    :arg: pd.DataFrame df: Dataframe with columns country, username and one of chess `time_class` (rating).
    :arg: str time_class: Chess time_class rating with Chess.com API format.
    :return: Dataframe grouped by country with columns number of players and `time_class` (rating mean).
    :rtype: pd.DataFrame.
    """
    return df.groupby("country") \
        .agg({time_class: 'mean', 'username': 'size'}) \
        .rename(columns={'username': 'number of players'}) \
        .reset_index()


def get_status_rating_correlation(df: pd.DataFrame, time_class: str, statuses: list) -> pd.DataFrame:
    """Get status rating correlation for time_class and statuses.

    :arg: pd.DataFrame df: Dataframe with columns status and one of chess `time_class` (rating).
    :arg: str time_class: Chess time_class rating with Chess.com API format.
    :arg: list statuses: Selected statuses.
    :return: Dataframe grouped by country with columns number of players and `time_class` (rating mean).
    :rtype: pd.DataFrame.
    """
    dff = df[df['status'].isin(statuses)]
    return dff.groupby('status')[time_class].mean().reset_index()
