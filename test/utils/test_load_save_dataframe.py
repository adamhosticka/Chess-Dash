import pandas as pd

from app.utils.load_save_dataframe import load_dataframe


def test_load_dataframe_empty_if_unknown_filename():
    assert pd.DataFrame().equals(load_dataframe('unknown_filename'))
