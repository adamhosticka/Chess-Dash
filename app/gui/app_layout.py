"""Render app layout."""

import pandas as pd
from dash import Dash, html

from app.gui.player.player_layout import player_layout
from app.gui.game.game_layout import game_layout


def render_app_layout(app: Dash, players_df: pd.DataFrame, games_df: pd.DataFrame) -> html.Div:
    """Render app layout.

    :param: Dash app: Dash application.
    :param: pd.DataFrame players_df: Dataframe containing players.
    :param: pd.DataFrame games_df: Dataframe containing games.
    :return: App layout.
    :rtype: html.Div.
    """
    return html.Div(
        id='root',
        style={"textAlign": "center", "paddingTop": "1vh"},
        children=[
            html.Div(
                style={"margin": "0 1rem"},
                children=[
                    html.Div(
                        style={"width": "75%", "margin": "auto"},
                        children=[
                            player_layout(app, players_df),
                            game_layout(app, games_df),
                        ]
                    )
                ]
            )
        ]
    )
