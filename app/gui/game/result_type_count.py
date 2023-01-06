""""""

from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.helpers.gui_config import SEQUENTIAL_COLOR
from app.utils.format_graph_labels import format_labels


class ResultTypeCount(GraphLayout):
    COMPONENT_ID = 'result-type-count'
    GRAPH_ID = 'result-type-count-graph'

    def get_figure(self) -> html.Div:
        dff = self.df.groupby(['result_type', 'result'], as_index=False)['uuid'].count()
        dff.sort_values('uuid', inplace=True)

        labels = format_labels(['result_type'])
        labels.update({'uuid': 'count'})
        fig = px.bar(
            data_frame=dff,
            x='uuid',
            y='result_type',
            color='result',
            text='result',
            labels=labels,
            title=f"Result type count",
            color_discrete_sequence=SEQUENTIAL_COLOR,
        )
        # fig.update_traces(marker_color='#1a6c75', width=0.8)
        # fig.update_layout(barmode='group', bargap=0.3, bargroupgap=0)

        return fig
