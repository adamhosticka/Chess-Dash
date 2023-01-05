"""Layout for player data visualization."""

import numpy as np
import pandas as pd
from datetime import datetime
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3

from app.gui.player import (
    players_count_per_country,
    players_rating_per_country,
    rating_correlation,
)


def player_layout(app: Dash, df: pd.DataFrame) -> html.Div:
    def convert_codes(code):
        try:
            return country_name_to_country_alpha3(country_alpha2_to_country_name(code))
        except:
            return np.nan

    df['country'] = df['country_code'].apply(convert_codes)
    df = df[df['player_id'].notna()]

    df_days_since_joined = df[df['joined'].notna()]
    df_days_since_joined['days_since_joined'] = \
        (datetime.today() - pd.to_datetime(df_days_since_joined['joined'], unit="s")).astype('timedelta64[h]')/24

    return html.Div(
        children=[
            html.H1("Players dataset"),
            html.Br(),
            html.Div(
                id='player_layout',
                children=[
                    players_count_per_country.render(app, df),
                    players_rating_per_country.render(app, df),
                    rating_correlation.render(app, df, 'followers'),
                    rating_correlation.render(app, df, 'tactics_highest_rating'),
                    rating_correlation.render(app, df, 'puzzle_rush_best_score'),
                    rating_correlation.render(app, df_days_since_joined, 'days_since_joined'),
                ]
            )
        ]
    )
