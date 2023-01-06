""""""

from dash import html, Input, Output
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.gui.player.dash_components import time_class_selector
from app.helpers.gui_config import PLAYER_TIME_CLASS_SELECTOR, SEQUENTIAL_COLOR
from app.utils.format_graph_labels import format_labels


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

            dff = self.df.groupby("country")\
                .agg({time_class: 'mean', 'username': 'size'})\
                .rename(columns={'username': 'number of players'})\
                .reset_index()

            fig = px.choropleth(
                data_frame=dff,
                locations='country',
                color=time_class,
                hover_data=['number of players'],
                labels=format_labels([time_class]),
                color_continuous_scale=SEQUENTIAL_COLOR,
            )

            return fig
