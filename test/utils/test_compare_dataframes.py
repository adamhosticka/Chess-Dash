"""Test compare dataframes module."""

from typing import Union

import pytest
import pandas as pd

from app.utils.dataframe_utils import load_dataframe, dataframes_equal, create_dataframe_from_list


def test_load_dataframe_empty_if_unknown_filename():
    """Test if load dataframe returns empty Dataframe when filename does not exist."""
    assert pd.DataFrame().equals(load_dataframe('unknown_filename'))


@pytest.mark.parametrize(
    ['df1', 'df2', 'sort_by', 'expected'],
    [
        (
            pd.DataFrame({
                'name': ['Adam', 'Peter', 'Janka'],
                'prijmeni': ['Hosticka', 'Peter', 'Mala']
            }),
            pd.DataFrame({
                'name': ['Peter', 'Adam', 'Janka'],
                'prijmeni': ['Peter', 'Hosticka', 'Mala']
            }),
            'prijmeni',
            True
        ),
        (
            pd.DataFrame({
                'name': ['Adam', 'Peter', 'Janka'],
                'prijmeni': ['Hosticka', 'Peter', 'Mala']
            }),
            pd.DataFrame({
                'name': ['Peter', 'Adam', 'Janka'],
                'prijmeni': ['Hosticka', 'Peter', 'Mala']
            }),
            'prijmeni',
            False
        ),
        (
            pd.DataFrame({
                'count': [1, 1, 2, 1, 3, 2],
                'type': ['x', 'y', 'y', 'z', 'x', 's']
            }),
            pd.DataFrame({
                'count': [2, 1, 1, 1, 3, 2],
                'type': ['s', 'z', 'y', 'x', 'x', 'y']
            }),
            ['count', 'type'],
            True
        ),
        (
            pd.DataFrame(),
            pd.DataFrame(),
            None,
            True
        ),
        (
            pd.DataFrame(),
            pd.DataFrame([1, 2]),
            None,
            False
        ),
    ]
)
def test_dataframes_equal(df1: pd.DataFrame, df2: pd.DataFrame, sort_by: Union[str, list], expected: bool):
    if sort_by:
        assert dataframes_equal(df1, df2, sort_by) == expected
    else:
        assert dataframes_equal(df1, df2) == expected


DATA = [
    {"id": 1, "name": "Adam", "big_house": False},
    {"id": 2, "name": "Lenka", "big_house": True}
]


@pytest.mark.parametrize(
    ['data', 'expected'],
    [
        (
            [],
            pd.DataFrame()
        ),
        (
            DATA,
            pd.DataFrame(DATA)
        )
    ]
)
def test_create_dataframe_from_list(data: list, expected: pd.DataFrame):
    assert dataframes_equal(expected, create_dataframe_from_list(data), 'name')
