""""""

from dash import html, Input, Output
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.gui.player.dash_components import time_class_selector
from app.helpers.gui_config import PLAYER_TIME_CLASS_SELECTOR, PLAYER_COLOR


class StatusRatingCorrelation(GraphLayout):
    COMPONENT_ID = 'status-rating-correlation'
    GRAPH_ID = 'status-rating-correlation-graph'
    CALLBACK = True

    def get_children(self) -> list:
        return [time_class_selector(self.df, self.COMPONENT_ID)]

    def set_callback(self) -> html.Div:
        @self.app.callback(
            Output(self.GRAPH_ID, 'figure'),
            Input(f'{PLAYER_TIME_CLASS_SELECTOR}-{self.COMPONENT_ID}', 'value')
        )
        def get_callback_figure(time_class):
            dff = self.df[self.df['status'].isin(['basic', 'premium'])]
            dff = dff.groupby('status')[time_class].mean().reset_index()

            fig = px.bar(
                data_frame=dff,
                x='status',
                y=time_class,
                labels={time_class: f'{time_class.replace("_", " ")} mean'},
            )
            fig.update_traces(marker_color=PLAYER_COLOR, width=0.40)

            return fig
