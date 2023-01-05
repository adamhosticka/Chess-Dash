""""""

import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from app.gui.player import time_class_selector


def render(app: Dash, df: pd.DataFrame, corr: str) -> html.Div:
    component_id = f'{corr}-followers_rating_correlation'
    graph_id = f"{component_id}-graph"

    @app.callback(
        Output(graph_id, 'figure'),
        Input(f'time-class-selector-{component_id}', 'value')
    )
    def get_ratings_figure(time_class):
        figure = px.scatter(
            data_frame=df,
            x=corr,
            y=time_class,
            labels={time_class: time_class.replace("_", " ")},
            color_continuous_scale=px.colors.sequential.Darkmint
        )

        return figure

    return html.Div(
        id=component_id,
        children=[
            time_class_selector.render(app, df, component_id),
            html.Div(
                children=[
                    dcc.Graph(id=graph_id)
                ],
            )
        ]
    )

