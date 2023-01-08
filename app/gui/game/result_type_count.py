"""Bar graph displaying result type count and winner."""

from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.helpers.gui_config import SEQUENTIAL_COLOR
from app.src.format_data.gui_format_games import get_result_type_count
from app.utils.format_graph_labels import format_labels


class ResultTypeCount(GraphLayout):
    """Class rendering a bar graph displaying result type count and winner."""
    COMPONENT_ID = 'result-type-count'
    GRAPH_ID = 'result-type-count-graph'

    def get_figure(self) -> html.Div:
        dff = get_result_type_count(self.df)

        labels = format_labels(['result_type'])
        fig = px.bar(
            data_frame=dff,
            x='count',
            y='result_type',
            color='result',
            text='result',
            labels=labels,
            title="Result type count",
            color_discrete_sequence=SEQUENTIAL_COLOR,
        )
        # fig.update_traces(marker_color='#1a6c75', width=0.8)
        # fig.update_layout(barmode='group', bargap=0.3, bargroupgap=0)

        return fig

    @staticmethod
    def set_text():
        return html.P("As we can see, resignation is the most common result type in chess. That would make sense, "
                      "since one can usually tell when there is no change to win. "
                      "Although I did not expect so many stalemates.")
