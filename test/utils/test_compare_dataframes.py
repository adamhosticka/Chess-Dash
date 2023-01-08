"""Test compare dataframes module."""
from typing import Union

import pytest
import pandas as pd

from app.utils.compare_dataframes import dataframes_equal


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
