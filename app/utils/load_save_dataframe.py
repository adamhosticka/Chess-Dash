"""Load/save dataframes from/to data directory."""

import os
import pandas as pd

from app.definitions import DATA_DIR


def load_dataframe(filename: str) -> pd.DataFrame:
    """Load dataframe from file.

    :arg: str filename: Name of file to load.
    :return: Dataframe.
    :rtype: pd.DataFrame.
    """
    return pd.read_pickle(os.path.join(DATA_DIR, filename))


def save_dataframe(dataframe: pd.DataFrame, filename: str):
    """Save dataframe to file.

    :arg: pd.Dataframe dataframe: Dataframe to save.
    :arg: str filename: Filename to save dataframe to.
    """
    dataframe.to_pickle(os.path.join(DATA_DIR, filename))
