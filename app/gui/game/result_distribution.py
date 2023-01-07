""""""

from dash import Input, Output
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.helpers.gui_config import GAME_TIME_CLASS_CHECKLIST_ID
from app.gui.game.dash_components import time_class_checklist
from app.src.format_data.gui_format_games import get_result_distribution
from app.utils.format_graph_labels import format_labels


class ResultDistribution(GraphLayout):
    COMPONENT_ID = 'result-distribution'
    GRAPH_ID = 'result-distribution-graph'
    CALLBACK = True

    def get_children(self) -> list:
        return [time_class_checklist(self.df, self.COMPONENT_ID)]

    def set_callback(self):
        @self.app.callback(
            Output(self.GRAPH_ID, 'figure'),
            Input(f'{GAME_TIME_CLASS_CHECKLIST_ID}-{self.COMPONENT_ID}', 'value')
        )
        def get_callback_figure(time_classes):
            dff = get_result_distribution(self.df, time_classes)

            fig = px.bar(
                data_frame=dff,
                x='time_class',
                y='result type (%)',
                color='result',
                hover_data=['count'],
                barmode='group',
                title=f"Result distribution for selected time classes",
                labels=format_labels(['time_class']),
            )

            return fig
