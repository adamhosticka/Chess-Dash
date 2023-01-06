"""Layout for player data visualization."""

import numpy as np
import pandas as pd
from datetime import datetime
from dash import Dash, html
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3

from app.gui.player.players_count_per_country import PlayersCountPerCountry
from app.gui.player.players_rating_per_country import PlayersRatingPerCountry
from app.gui.player.status_rating_correlation import StatusRatingCorrelation
from app.gui.player.rating_correlation import \
    TacticsRatingCorrelation, PuzzleRatingCorrelation, JoinedRatingCorrelation, FollowersRatingCorrelation


def convert_codes(code):
    try:
        return country_name_to_country_alpha3(country_alpha2_to_country_name(code))
    except:
        return np.nan


def player_layout(app: Dash, df: pd.DataFrame) -> html.Div:

    df['country'] = df['country_code'].apply(convert_codes)
    df = df[df['player_id'].notna()]

    return html.Div(
        id='player_layout',
        children=[
            html.H1("Players dataset"),
            html.Br(),
            html.P(f"There are {df['player_id'].nunique()} unique players in the dataset from all around the world."),
            html.Hr(),
            html.Div(
                children=[
                    PlayersCountPerCountry(app, df).render(),
                    PlayersRatingPerCountry(app, df).render(),
                    StatusRatingCorrelation(app, df).render(),
                    TacticsRatingCorrelation(app, df).render(),
                    PuzzleRatingCorrelation(app, df).render(),
                    JoinedRatingCorrelation(app, df).render(),
                    FollowersRatingCorrelation(app, df).render(),
                ]
            )
        ]
    )
