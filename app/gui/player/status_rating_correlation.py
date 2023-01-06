""""""

import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from app.gui.player import time_class_selector


def render(app: Dash, df: pd.DataFrame) -> html.Div:
    component_id = 'status_rating_correlation'
    graph_id = f"{component_id}-graph"

    @app.callback(
        Output(graph_id, 'figure'),
        Input(f'time-class-selector-{component_id}', 'value')
    )
    def get_status_ratings_figure(time_class):
        dff = df[df['status'].isin(['basic', 'premium'])]
        dff = dff.groupby('status')[time_class].mean().reset_index()

        figure = px.bar(
            data_frame=dff,
            x='status',
            y=time_class,
            labels={time_class: f'{time_class.replace("_", " ")} mean'},
            color_continuous_scale=px.colors.sequential.Aggrnyl,
        )
        figure.update_traces(marker_color='#2bb585', width=0.40)

        return figure

    return html.Div(
        id=component_id,
        children=[
            time_class_selector.render(app, df, component_id),
            html.Div(
                style={"width": "50%", "margin": "auto"},
                children=[
                    dcc.Graph(id=graph_id)
                ],
            )
        ]
    )
