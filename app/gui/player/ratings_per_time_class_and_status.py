"""Graph for displaying ratings statictics per time class."""

from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.src.format_data.gui_format_players import get_ratings_per_time_class_and_status


class RatingsPerTimeClassAndStatus(GraphLayout):
    """Graph for displaying ratings statictics per time class."""

    COMPONENT_ID = 'ratings-time-class-status'
    GRAPH_ID = 'ratings-time-class-status-graph'

    def get_figure(self) -> html.Div:
        dff = get_ratings_per_time_class_and_status(self.df)

        return px.box(
            data_frame=dff,
            title="Rating statistics per time class and status",
            x='time class',
            y='rating',
            color='status'
        )
