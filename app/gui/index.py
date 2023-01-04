import os

import numpy as np
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3

from app.definitions import DATA_DIR
from app.helpers.data_filenames import GAMES_FILENAME, PLAYERS_FILENAME


def run():
    app = Dash()
    app.layout = html.Div(
        id='root',
        children=[
            html.H1("Ahoj"),
            html.Hr(),
            html.Div(
                dcc.Dropdown(
                    id="select-time-class",
                    options=[
                        {"label": "Blitz", "value": "blitz"},
                        {"label": "Rapid", "value": "rapid"},
                    ],
                    value="blitz"
                )
            ),

            dcc.Graph(id="my-first")
        ]
    )

    @app.callback(
        Output(component_id="my-first", component_property='figure'),
        Input(component_id='select-time-class', component_property='value')
    )
    def update_graph(dropdown_val):
        print(dropdown_val)
        # df = pd.read_pickle(os.path.join(DATA_DIR, GAMES_FILENAME))
        # df = df[df['time_class'] == dropdown_val]

        df = pd.read_pickle(os.path.join(DATA_DIR, PLAYERS_FILENAME))
        print(df[df['country_code'] == "US"])

        def convert_codes(code):
            try:
                return country_name_to_country_alpha3(country_alpha2_to_country_name(code))
            except:
                return np.nan

        df['country'] = df['country_code'].apply(convert_codes)
        print(df[df['country'] == "BWA"])
        dff = df.groupby("country")[['chess_blitz_last_rating', 'chess_rapid_last_rating']].median().reset_index()
        rename_list = ['chess_blitz_last_rating', 'chess_rapid_last_rating']
        rename_dict = {k: k.replace("_", " ").title() for k in rename_list}
        dff.rename(columns=rename_dict, inplace=True)
        print(dff[dff['country'] == 'RUS'])
        print(dff)

        graph_key = rename_dict[f"chess_{dropdown_val}_last_rating"]

        figure = px.choropleth(
            data_frame=dff,
            locations='country',
            color=graph_key,
            hover_data=[
                graph_key,
            ],
            labels={"Label"},
            color_continuous_scale=px.colors.sequential.Darkmint
        )

        return figure

    # app.run_server(debug=True)
    app.run(debug=True)


if __name__ == '__main__':
    run()
