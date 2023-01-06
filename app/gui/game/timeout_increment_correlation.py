""""""

import pandas as pd
from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout


class TimeoutIncrementCorrelation(GraphLayout):
    COMPONENT_ID = 'timeout-increment-correlation'
    GRAPH_ID = 'timeout-increment-correlation-graph'

    def get_figure(self) -> html.Div:

        dff = self.df[['increment', 'result_type', 'uuid']]
        dff = dff[dff['result_type'].isin(['agreed', 'checkmated', 'win', 'timeout', 'resigned', 'repetition'])]

        dff = pd.DataFrame(dff.groupby(['increment', 'result_type'], as_index=False).agg(count=('uuid', 'count')).reset_index())
        dff['timeout games %'] = \
            100 * dff['count'] / dff.groupby('increment')['count'].transform('sum')
        dff['increment'] = dff['increment'].astype(int)
        dff.sort_values(by=['increment'], inplace=True)

        fig = px.line(
            dff,
            x='increment',
            y='timeout games %',
            color='result_type',
            title='Players loosing to time in realtion to time increment',
            markers=True,
        )

        return fig
