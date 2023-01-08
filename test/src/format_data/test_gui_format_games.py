"""Test formatting DataFrames for games graphs"""

import pytest
import pandas as pd
import numpy as np

from app.src.format_data.gui_format_games import get_time_classes_and_checklist_options, get_most_common_ecos, \
    get_result_distribution, get_rated_rating_correlation, get_result_type_count, get_result_type_increment_correlation
from app.utils.dataframe_utils import dataframes_equal

GAMES_DF = pd.DataFrame({
    'uuid': [1, 2, 3, 4, 5, 6],
    'result': ['White', 'Black', 'White', 'White', 'Draw', 'White'],
    'result_type': ['checkmated', 'resigned', 'resigned', 'timeout', 'agreed', 'checkmated'],
    'eco_name': ['Sicilian', 'Kings Gambit', 'Sicilian', 'Queens Gambit', 'Sicilian', 'Queens Gambit'],
    'time_class': ['daily', 'rapid', 'blitz', 'blitz', 'bullet', 'rapid'],
    'time': [1, 10, 5, 3, 1, 10],
    'increment': [70, 0, 2, 0, 1, 3],
    'rated': [True, False, True, True, False, False],
    'white_rating': [1000, 800, 1200, 1500, 300, 300],
    'black_rating': [1200, 1000, 1300, 1400, 500, 100]
})


@pytest.mark.parametrize(
    ['df', 'expected'],
    [
        (
            GAMES_DF,
            (
                [
                    {"label": "Daily", "value": "daily"},
                    {"label": "Rapid", "value": "rapid"},
                    {"label": "Blitz", "value": "blitz"},
                    {"label": "Bullet", "value": "bullet"},
                ],
                np.array(['daily', 'rapid', 'blitz', 'bullet'])
            )
        )
    ]
)
def test_get_time_classes_and_checklist_options(df: pd.DataFrame, expected: tuple):
    options, time_classes = get_time_classes_and_checklist_options(df)
    assert options == expected[0]
    assert np.array_equal(time_classes, expected[1])


@pytest.mark.parametrize(
    ['df', 'cnt', 'expected'],
    [
        (
            GAMES_DF, 10,
            pd.DataFrame({
                'opening name': ['Sicilian', 'Kings Gambit', 'Queens Gambit'],
                'count': [3, 1, 2]
            })
        ),
        (
            GAMES_DF, 1,
            pd.DataFrame({
                'opening name': ['Sicilian'],
                'count': [3]
            })
        )
    ]
)
def test_get_most_common_ecos(df: pd.DataFrame, cnt: int, expected: pd.DataFrame):
    assert dataframes_equal(expected, get_most_common_ecos(df, cnt), 'opening name')


@pytest.mark.parametrize(
    ['df', 'time_classes', 'expected'],
    [
        (
            GAMES_DF, [],
            pd.DataFrame({
                'result': ['Black', 'White', 'White', 'Draw', 'White'],
                'time_class': ['rapid', 'daily', 'blitz', 'bullet', 'rapid'],
                'count': [1, 1, 2, 1, 1],
                'result (%)': [50.0, 100.0, 100.0, 100.0, 50.0],
            })
        )
    ]
)
def test_get_result_distribution(df: pd.DataFrame, time_classes: list, expected: pd.DataFrame):
    assert dataframes_equal(expected, get_result_distribution(df, time_classes), ['count', 'time_class', 'result'])


@pytest.mark.parametrize(
    ['df', 'expected'],
    [
        (
            GAMES_DF,
            pd.DataFrame({
                'rated': [True, False],
                'rating_mean': [3800/3, 500.0]
            })
        )
    ]
)
def test_get_rated_rating_correlation(df: pd.DataFrame, expected: pd.DataFrame):
    assert dataframes_equal(expected, get_rated_rating_correlation(df), ['rated', 'rating_mean'])


@pytest.mark.parametrize(
    ['df', 'expected'],
    [
        (
            GAMES_DF,
            pd.DataFrame({
                'result_type': ['checkmated', 'resigned', 'timeout', 'resigned', 'agreed'],
                'result': ['White', 'White', 'White', 'Black', 'Draw'],
                'count': [2, 1, 1, 1, 1],
            })
        )
    ]
)
def test_get_result_type_count(df: pd.DataFrame, expected: pd.DataFrame):
    assert dataframes_equal(expected, get_result_type_count(df), ['result_type', 'result', 'count'])


@pytest.mark.parametrize(
    ['df', 'result_types', 'expected'],
    [
        (
            GAMES_DF, ['timeout', 'checkmated', 'agreed'],
            pd.DataFrame({
                'increment': [3, 1, 0],
                'result_type': ['checkmated', 'agreed', 'timeout'],
                'count': [1, 1, 1],
                'result type %': [100.0, 100.0, 100.0]
            })
        ),
        (
            GAMES_DF, [],
            pd.DataFrame({
                'increment': [3, 2, 1, 0, 0],
                'result_type': ['checkmated', 'resigned', 'agreed', 'resigned', 'timeout'],
                'count': [1, 1, 1, 1, 1],
                'result type %': [100.0, 100.0, 100.0, 50.0, 50.0]
            })
        )
    ]
)
def test_get_result_type_increment_correlation(df: pd.DataFrame, result_types: list, expected: pd.DataFrame):
    assert dataframes_equal(expected, get_result_type_increment_correlation(df, result_types),
                            ['result type %', 'increment'])
