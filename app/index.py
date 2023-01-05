"""Main application."""

from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP

from app.helpers.data_filenames import PLAYERS_FILENAME, GAMES_FILENAME
from app.utils.load_save_dataframe import load_dataframe
from gui.player.player_layout import player_layout
from gui.game.game_layout import game_layout


def main():

    players_df = load_dataframe(PLAYERS_FILENAME)
    games_df = load_dataframe(GAMES_FILENAME)

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Chess data visualization"
    app.layout = html.Div(
        id='root',
        style={"background-color": "#F8F8F8"},
        children=[
            html.Div(
                style={"text-align": "center", "margin": "0 10vh", "padding-top": "1vh", "background-color": "white"},
                children=[
                    html.Div(
                        style={"margin": "0 10vh"},
                        children=[
                            player_layout(app, players_df),
                            game_layout(app, games_df),
                        ]
                    )
                ]
            )
        ]
    )
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
