"""Compare dataframes."""

from typing import Union
import pandas as pd


def dataframes_equal(df1: pd.DataFrame, df2: pd.DataFrame, sort_by: Union[str, list]) -> bool:
    """Compare dataframe regardles of row order.

    :param: pd.DataFrame df1: First dataframe.
    :param: pd.DataFrame df2: Second dataframe.
    :param: str sort_by: Column name to sort by.
    :return: True if dataframes are equals regardles of row order, False otherwise.
    :rtype: bool.
    """
    sorted_df1 = df1.sort_values(sort_by).reset_index(drop=True)
    sorted_df2 = df2.sort_values(sort_by).reset_index(drop=True)
    return sorted_df1.equals(sorted_df2)
