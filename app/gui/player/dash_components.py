""""""

import pandas as pd
from dash import html, dcc

from app.helpers.gui_config import PLAYER_TIME_CLASS_SELECTOR
from app.src.format_data.gui_format_players import get_time_class_selector_options


def time_class_selector(df: pd.DataFrame, parent_component_id: str, tactics_and_puzzles: bool = False) -> html.Div:
    options = get_time_class_selector_options(df, tactics_and_puzzles)
    return html.Div(
        dcc.Dropdown(
            id=f"{PLAYER_TIME_CLASS_SELECTOR}-{parent_component_id}",
            style={"width": "20vh"},
            options=options,
            value="blitz_rating",
            clearable=False,
        )
    )
