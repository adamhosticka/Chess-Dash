"""Graph displaying correlation between increment and result_type."""

from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.src.format_data.gui_format_games import get_result_type_increment_correlation


class ResultTypeIncrementCorrelation(GraphLayout):
    """Class displaying correlation between increment and result_type."""

    COMPONENT_ID = 'timeout-increment-correlation'
    GRAPH_ID = 'timeout-increment-correlation-graph'

    def get_figure(self) -> html.Div:
        dff = get_result_type_increment_correlation(
            self.df, ['agreed', 'checkmated', 'win', 'timeout', 'resigned'])

        fig = px.line(
            dff,
            x='increment',
            y='result type %',
            color='result_type',
            hover_data=['count'],
            title='Players loosing to time in realtion to time increment',
            markers=True,
        )

        return fig
