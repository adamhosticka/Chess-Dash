""""""

import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.gui.player.dash_components import time_class_selector
from app.helpers.gui_config import PLAYER_TIME_CLASS_SELECTOR, SEQUENTIAL_COLOR


class PlayersRatingPerCountry(GraphLayout):
    COMPONENT_ID = 'players-rating-per-country'
    GRAPH_ID = 'players-rating-per-country-graph'
    CALLBACK = True

    def get_children(self) -> list:
        return [time_class_selector(self.df, self.COMPONENT_ID, True)]

    def set_callback(self) -> html.Div:
        @self.app.callback(
            Output(self.GRAPH_ID, 'figure'),
            Input(f'{PLAYER_TIME_CLASS_SELECTOR}-{self.COMPONENT_ID}', 'value')
        )
        def get_callback_figure(time_class):

            dff = self.df.groupby("country")[time_class].mean().reset_index()

            fig = px.choropleth(
                data_frame=dff,
                locations='country',
                color=time_class,
                labels={time_class: time_class.replace("_", " ")},
                color_continuous_scale=SEQUENTIAL_COLOR,
            )

            return fig
