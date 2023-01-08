"""Graphs for displaying correlation between rating and other paramters."""

from datetime import datetime
import plotly.express as px
import pandas as pd
from dash import Dash, html, Input, Output

from app.gui.graph_layout import GraphLayout
from app.gui.player.dash_components import time_class_selector
from app.helpers.gui_config import PLAYER_TIME_CLASS_SELECTOR
from app.utils.format_graph_labels import format_labels


class RatingCorrelation(GraphLayout):
    """Class for displaying correlation between rating and other paramters."""
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
                labels=format_labels([time_class, self.CORR]),
                color_continuous_scale=px.colors.sequential.Darkmint
            )

            return figure

    def get_figure(self) -> html.Div:
        # Disable pylint E1111
        raise NotImplementedError


class TacticsRatingCorrelation(RatingCorrelation):
    """Class for displaying correlation between rating and tactics."""

    COMPONENT_ID = 'tactics-rating-correlation'
    GRAPH_ID = 'tactics-rating-correlation-graph'
    CORR = 'tactics_highest_rating'

    def get_figure(self) -> html.Div:
        # Disable pylint E1111
        raise NotImplementedError


class PuzzleRatingCorrelation(RatingCorrelation):
    """Class for displaying correlation between rating and puzzles."""

    COMPONENT_ID = 'puzzle-rating-correlation'
    GRAPH_ID = 'puzzle-rating-correlation-graph'
    CORR = 'puzzle_rush_best_score'

    def get_figure(self) -> html.Div:
        # Disable pylint E1111
        raise NotImplementedError


class JoinedRatingCorrelation(RatingCorrelation):
    """Class for displaying correlation between rating and time since joined."""

    COMPONENT_ID = 'joined-rating-correlation'
    GRAPH_ID = 'joined-rating-correlation-graph'
    CORR = 'days_since_joined'

    def __init__(self, app: Dash, df: pd.DataFrame):
        super().__init__(app, df)
        df_days_since_joined = df[df['joined'].notna()]
        df_days_since_joined['days_since_joined'] = \
            (datetime.today() - pd.to_datetime(df_days_since_joined['joined'], unit="s")).astype('timedelta64[h]') / 24
        self.df = df_days_since_joined

    def get_figure(self) -> html.Div:
        # Disable pylint E1111
        raise NotImplementedError


class FollowersRatingCorrelation(RatingCorrelation):
    """Class for displaying correlation between rating and player's followers."""

    COMPONENT_ID = 'followers-rating-correlation'
    GRAPH_ID = 'followers-rating-correlation-graph'
    CORR = 'followers'

    def get_figure(self) -> html.Div:
        # Disable pylint E1111
        raise NotImplementedError
