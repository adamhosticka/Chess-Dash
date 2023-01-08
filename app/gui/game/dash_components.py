"""File with games dash components."""

import pandas as pd
from dash import html, dcc

from app.helpers.gui_config import GAME_TIME_CLASS_CHECKLIST_ID
from app.src.format_data.gui_format_games import get_time_classes_and_checklist_options


def time_class_checklist(df: pd.DataFrame, parent_component_id: str) -> html.Div:
    """Checklist with time classes from games dataframe.

    :param: pd.DataFrame df: Dataframe containing games data.
    :param: str parent_component_id: ID of parent component.
    :return: Checklist component.
    :rtype: html.Div.
    """

    options, time_classes = get_time_classes_and_checklist_options(df)
    return html.Div(
        dcc.Checklist(
            id=f"{GAME_TIME_CLASS_CHECKLIST_ID}-{parent_component_id}",
            options=options,
            labelStyle={'paddingLeft': '1em', 'fontSize': '1.3em'},
            value=time_classes,
            inline=True,
        )
    )
