""""""

from dash import Dash, html, Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime

from app.gui.graph_layout import GraphLayout
from app.gui.player.dash_components import time_class_selector
from app.helpers.gui_config import PLAYER_TIME_CLASS_SELECTOR


class RatingCorrelation(GraphLayout):
    CALLBACK = True
    CORR = ""

    def get_children(self) -> list:
        return [time_class_selector(self.df, self.COMPONENT_ID)]

    def set_callback(self) -> html.Div:
        @self.app.callback(
            Output(self.GRAPH_ID, 'figure'),
            Input(f'{PLAYER_TIME_CLASS_SELECTOR}-{self.COMPONENT_ID}', 'value')
        )
        def get_ratings_figure(time_class):
            figure = px.scatter(
                data_frame=self.df,
                x=self.CORR,
                y=time_class,
                labels={time_class: time_class.replace("_", " ")},
                color_continuous_scale=px.colors.sequential.Darkmint
            )

            return figure


class TacticsRatingCorrelation(RatingCorrelation):
    COMPONENT_ID = 'tactics-rating-correlation'
    GRAPH_ID = 'tactics-rating-correlation-graph'
    CORR = 'tactics_highest_rating'


class PuzzleRatingCorrelation(RatingCorrelation):
    COMPONENT_ID = 'puzzle-rating-correlation'
    GRAPH_ID = 'puzzle-rating-correlation-graph'
    CORR = 'puzzle_rush_best_score'


class JoinedRatingCorrelation(RatingCorrelation):
    COMPONENT_ID = 'joined-rating-correlation'
    GRAPH_ID = 'joined-rating-correlation-graph'
    CORR = 'days_since_joined'

    def __init__(self, app: Dash, df: pd.DataFrame):
        super().__init__(app, df)
        df_days_since_joined = df[df['joined'].notna()]
        df_days_since_joined['days_since_joined'] = \
            (datetime.today() - pd.to_datetime(df_days_since_joined['joined'], unit="s")).astype('timedelta64[h]') / 24
        self.df = df_days_since_joined


class FollowersRatingCorrelation(RatingCorrelation):
    COMPONENT_ID = 'followers-rating-correlation'
    GRAPH_ID = 'followers-rating-correlation-graph'
    CORR = 'followers'
