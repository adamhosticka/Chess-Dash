""""""

import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px


def render(app: Dash, df: pd.DataFrame) -> html.Div:
    component_id = 'players-count-per-country'
    graph_id = f"{component_id}-graph"

    players_count = df['player_id'].nunique()
    df = df.groupby('country')['username'].count().reset_index()

    return html.Div(
        id=component_id,
        children=[
            html.P(f"There are {players_count} unique players in the dataset from all around the world."),
            html.Div(
                dcc.Graph(
                    id=graph_id,
                    figure=px.choropleth(
                        data_frame=df,
                        title="Number of players per country",
                        locations='country',
                        color='username',
                        labels={"username": "players count"},
                        color_continuous_scale=px.colors.sequential.Darkmint
                    )
                )
            )
        ]
    )
