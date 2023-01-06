""""""

import pandas as pd
from dash import html, dcc

from app.helpers.gui_config import GAME_TIME_CLASS_CHECKLIST_ID


def time_class_checklist(df: pd.DataFrame, parent_component_id: str) -> html.Div:
    time_classes = df['time_class'].unique()
    options = [
        {"label": col.split("_")[0].title(), "value": col}
        for col in time_classes
    ]
    return html.Div(
        dcc.Checklist(
            id=f"{GAME_TIME_CLASS_CHECKLIST_ID}-{parent_component_id}",
            options=options,
            labelStyle={'paddingLeft': '1em', 'fontSize': '1.3em'},
            value=time_classes,
            inline=True,
        )
    )
