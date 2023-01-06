"""Test loading and saving dataframes."""

import pandas as pd

from app.utils.load_save_dataframe import load_dataframe


def test_load_dataframe_empty_if_unknown_filename():
    """Test if load dataframe returns empty Dataframe when filename does not exist."""
    assert pd.DataFrame().equals(load_dataframe('unknown_filename'))
