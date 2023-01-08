"""Graph for displaying ratings statictics per time class."""

from dash import html
import plotly.express as px
import pandas as pd

from app.gui.graph_layout import GraphLayout
from app.src.format_data.gui_format_players import get_ratings_per_time_class_and_status


class RatingsPerTimeClassAndStatus(GraphLayout):
    """Graph for displaying ratings statictics per time class."""

    COMPONENT_ID = 'time-class-ratings'
    GRAPH_ID = 'time-class-ratings-graph'

    def get_figure(self) -> html.Div:
        dff = get_ratings_per_time_class_and_status(self.df)

        return px.box(
            data_frame=dff,
            title="Rating statistics per time class and status",
            x='time class',
            y='rating',
            color='status'
        )
