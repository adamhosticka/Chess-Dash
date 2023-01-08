"""Test fetching countries."""
import pandas as pd
import pytest
from flexmock import flexmock

from app.src.fetch_data.fetch_country import FetchCountry
from app.helpers.iso_codes import ISO_CODES
from app.utils.dataframe_utils import dataframes_equal

FETCHED_ITEM = {"@id": "https://api.chess.com/pub/country/IT", "code": "IT", "name": "Italy"}


@pytest.mark.parametrize(
    ['fetched_item', 'expected'],
    [
        (
            FETCHED_ITEM,
            pd.DataFrame(
                [FETCHED_ITEM]*len(ISO_CODES)
            )
        ),
        (
            None,
            pd.DataFrame([])
        )
    ]
)
def test_fetch_data(fetched_item: dict, expected: pd.DataFrame):
    flexmock(
        FetchCountry,
        fetch_item=fetched_item
    )
    assert dataframes_equal(expected, FetchCountry().fetch_data())
