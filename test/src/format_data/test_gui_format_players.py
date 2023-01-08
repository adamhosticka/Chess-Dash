"""Test formatting DataFrames for players graphs."""

import pytest
import numpy as np
import pandas as pd
from typing import Union

from app.src.format_data.gui_format_players import get_time_class_selector_options, convert_alpha2_code_to_alpha3, \
    get_players_count_and_rating_per_country, get_status_rating_correlation
from app.utils.dataframe_utils import dataframes_equal

PLAYERS_DF = pd.DataFrame({
    'player_id': [1, 2, 3, 4, 5, 6],
    'country': ['CZ', 'US', 'SK', 'CZ', 'CZ', 'SK'],
    'username': ['Adam', 'Johnas', 'Jozko', 'Milana', 'Bart', 'Metodej'],
    'status': ['premium', 'premium', 'basic', 'premium', 'premium', 'basic'],
    'blitz_rating': [100, 200, 500, 200, 900, 100],
    'daily_rating': [300, 900, 100, 100, 200, 500],
    'tactics_highest_rating': [1200, 500, 400, 1300, 400, 600],
    'puzzle_rush_best_score': [22, 11, 0, 1, 4, 5]
})


@pytest.mark.parametrize(
    ['df', 'tactics_and_puzzles', 'expected'],
    [
        (
            PLAYERS_DF,
            True,
            [
                {"label": "Blitz", "value": "blitz_rating"},
                {"label": "Daily", "value": "daily_rating"},
                {"label": "Tactics", "value": "tactics_highest_rating"},
                {"label": "Puzzle", "value": "puzzle_rush_best_score"},
            ]
        ),
        (
            PLAYERS_DF,
            False,
            [
                {"label": "Blitz", "value": "blitz_rating"},
                {"label": "Daily", "value": "daily_rating"},
            ]
        )
    ]
)
def test_get_time_class_selector_options(df: pd.DataFrame, tactics_and_puzzles: bool, expected: list):
    assert expected == get_time_class_selector_options(df, tactics_and_puzzles)


@pytest.mark.parametrize(
    ['code', 'expected'],
    [
        ('AU', 'AUS'),
        ('CZ', 'CZE'),
        ('XI', np.nan),
        ('GB', 'GBR'),
        ('America', np.nan),
    ]
)
def test_convert_alpha2_code_to_alpha3(code: str, expected: Union[str, float]):
    if type(expected) == float:
        assert np.isnan(convert_alpha2_code_to_alpha3(code))
    else:
        assert expected == convert_alpha2_code_to_alpha3(code)


@pytest.mark.parametrize(
    ['df', 'time_class', 'expected'],
    [
        (
            PLAYERS_DF,
            None,
            pd.DataFrame({
                'country': ['SK', 'CZ', 'US'],
                'players count': [2, 3, 1]
            })
        ),
        (
            PLAYERS_DF,
            'blitz_rating',
            pd.DataFrame({
                'country': ['SK', 'CZ', 'US'],
                'players count': [2, 3, 1],
                'blitz_rating': [300.0, 400.0, 200.0]
            })
        ),
        (
            PLAYERS_DF,
            'puzzle_rush_best_score',
            pd.DataFrame({
                'country': ['SK', 'CZ', 'US'],
                'players count': [2, 3, 1],
                'puzzle_rush_best_score': [2.5, 9.0, 11.0]
            })
        )
    ]
)
def test_get_players_count_and_rating_per_country(df: pd.DataFrame, time_class: Union[str, None], expected: pd.DataFrame):
    assert dataframes_equal(expected, get_players_count_and_rating_per_country(df, time_class), 'players count')


@pytest.mark.parametrize(
    ['df', 'time_class', 'statuses', 'expected'],
    [
        (
            PLAYERS_DF,
            'blitz_rating',
            ['basic', 'premium'],
            pd.DataFrame({
                'status': ['basic', 'premium'],
                'blitz_rating': [300.0, 350.0]
            })
        )
    ]
)
def test_get_status_rating_correlation(df: pd.DataFrame, time_class: str, statuses: list, expected: pd.DataFrame):
    assert dataframes_equal(expected, get_status_rating_correlation(df, time_class, statuses), 'status')
