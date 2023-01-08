"""Layout for player data visualization."""

import pandas as pd
from dash import Dash, html

from app.gui.player.players_count_per_country import PlayersCountPerCountry
from app.gui.player.players_rating_per_country import PlayersRatingPerCountry
from app.gui.player.ratings_per_time_class_and_status import RatingsPerTimeClassAndStatus
from app.gui.player.rating_correlation import \
    TacticsRatingCorrelation, PuzzleRatingCorrelation, JoinedRatingCorrelation
from app.src.format_data.gui_format_players import convert_alpha2_code_to_alpha3


def player_layout(app: Dash, df: pd.DataFrame) -> html.Div:
    """Layout for player statistics.

    :param: Dash app: Dash application.
    :param: pd.DataFrame df: Dataframe with players data.
    :return: Player layout.
    :rtype: html.Div.
    """

    df['country'] = df['country_code'].apply(convert_alpha2_code_to_alpha3)
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
                    RatingsPerTimeClassAndStatus(app, df).render(),
                    html.Section("These scatter plots were my way to trying to prove, that with increasing tactics "
                                 "highest rating, puzzle rush best score and days since joined also increases "
                                 "the rating of a player."),
                    html.P("I think it shows that fact atleast a little bit."),
                    TacticsRatingCorrelation(app, df).render(),
                    PuzzleRatingCorrelation(app, df).render(),
                    JoinedRatingCorrelation(app, df).render(),
                ]
            )
        ]
    )
