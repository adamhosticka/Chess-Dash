"""Load/save dataframes from/to data directory."""

import os
import pandas as pd

from app.definitions import DATA_DIR


def load_dataframe(filename: str) -> pd.DataFrame:
    """Load dataframe from file if exists.

    :param: str filename: Name of file to load.
    :return: Dataframe.
    :rtype: pd.DataFrame.
    """
    if os.path.isfile(os.path.join(DATA_DIR, filename)):
        return pd.read_pickle(os.path.join(DATA_DIR, filename))
    print(f"Couldnt' find dataframe with filename {filename} -> returning empty dataframe")
    return pd.DataFrame()


def save_dataframe(dataframe: pd.DataFrame, filename: str):
    """Save dataframe to file.

    :param: pd.Dataframe dataframe: Dataframe to save.
    :param: str filename: Filename to save dataframe to.
    """
    dataframe.to_pickle(os.path.join(DATA_DIR, filename))
