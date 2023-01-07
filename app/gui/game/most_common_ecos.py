""""""

from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.helpers.gui_config import SEQUENTIAL_COLOR
from app.src.format_data.gui_format_games import get_most_common_ecos


class MostCommonEcos(GraphLayout):
    COMPONENT_ID = 'most-common-ecos'
    GRAPH_ID = 'most-common-ecos-graph'
    MOST_COMMON_CNT = 10

    def get_figure(self) -> html.Div:
        dff = get_most_common_ecos(self.df, self.MOST_COMMON_CNT)

        fig = px.pie(
            data_frame=dff,
            values='uuid',
            names='eco_name',
            labels={'uuid': 'count', 'eco_name': 'opening_name'},
            title=f"Most common {self.MOST_COMMON_CNT} openings",
            color_discrete_sequence=SEQUENTIAL_COLOR,
        )
        fig.update_traces(hoverinfo='label+percent', textinfo='value')

        return fig
