"""Utils for working with dataframes."""

import os
import pandas as pd
from typing import Union

from app.helpers.paths import DATA_DIR


def load_dataframe(filename: str) -> pd.DataFrame:
    """Load dataframe from file if exists.

    :param: str filename: Name of file to load.
    :return: Dataframe.
    :rtype: pd.DataFrame.
    """
    if os.path.isfile(os.path.join(DATA_DIR, filename)):
        return pd.read_pickle(os.path.join(DATA_DIR, filename))
    return pd.DataFrame()


def save_dataframe(dataframe: pd.DataFrame, filename: str):
    """Save dataframe to file.

    :param: pd.Dataframe dataframe: Dataframe to save.
    :param: str filename: Filename to save dataframe to.
    """
    dataframe.to_pickle(os.path.join(DATA_DIR, filename))


def dataframes_equal(df1: pd.DataFrame, df2: pd.DataFrame, sort_by: Union[str, list] = None) -> bool:
    """Compare dataframe regardles of row order.

    :param: pd.DataFrame df1: First dataframe.
    :param: pd.DataFrame df2: Second dataframe.
    :param: str sort_by: Column name to sort by.
    :return: True if dataframes are equals regardles of row order, False otherwise.
    :rtype: bool.
    """
    if df1.empty or df2.empty:
        return True if df1.empty and df2.empty else False
    if sort_by is None:
        sort_by = []
    sorted_df1 = df1.sort_values(sort_by).reset_index(drop=True)
    sorted_df2 = df2.sort_values(sort_by).reset_index(drop=True)
    return sorted_df1.equals(sorted_df2)


def create_dataframe_from_list(data: list) -> pd.DataFrame:
    """Create dataframe from list.

    :param list data: Data to save.
    :return: Dataframe.
    :rtype: pd.DataFrame.
    """
    return pd.DataFrame.from_dict(data)
