""""""

import pandas as pd
from dash import Dash, html, dcc


def render(app: Dash, df: pd.DataFrame, parent_component_id: str, tactics_and_puzzles: bool = False) -> html.Div:
    time_class_cols = [col for col in df.columns if col.find("_rating") != -1 and col.find("tactics") == -1]
    if tactics_and_puzzles:
        time_class_cols.extend(['tactics_highest_rating', 'puzzle_rush_best_score'])
    options = [
        {"label": col.split("_")[0].title(), "value": col}
        for col in time_class_cols
    ]
    return html.Div(
        dcc.Dropdown(
            id=f"time-class-selector-{parent_component_id}",
            style={"width": "20vh"},
            options=options,
            value="blitz_rating",
            clearable=False,
        )
    )
