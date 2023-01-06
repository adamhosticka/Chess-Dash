"""Layout for game data visualization."""

import pandas as pd
from dash import Dash, html

from app.gui.game.result_distribution import ResultDistribution
from app.gui.game.rated_rating_correlation import RatedRatingCorrelation
from app.gui.game.most_common_ecos import MostCommonEcos
from app.gui.game.timeout_increment_correlation import TimeoutIncrementCorrelation
from app.gui.game.result_type_count import ResultTypeCount


def game_layout(app: Dash, df: pd.DataFrame) -> html.Div:
    print("Game_layout")
    return html.Div(
        id='game_layout',
        children=[
            html.H1("Games dataset"),
            html.Br(),
            html.P(f"There are {len(df)} games in the dataset."),
            html.Hr(),
            html.Div(
                children=[
                    ResultDistribution(app, df).render(),
                    RatedRatingCorrelation(app, df).render(),
                    MostCommonEcos(app, df).render(),
                    TimeoutIncrementCorrelation(app, df).render(),
                    ResultTypeCount(app, df).render(),
                ]
            )
        ]
    )
