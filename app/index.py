"""Main application."""

import time
from flask_caching import Cache
from dash import Dash, html
from dash_bootstrap_components.themes import GRID

from app.helpers.data_filenames import PLAYERS_FILENAME, REFORMATED_GAMES_FILENAME
from app.utils.load_save_dataframe import load_dataframe
from gui.player.player_layout import player_layout
from gui.game.game_layout import game_layout


def main():
    app = Dash(
        __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=[GRID]
    )
    app.title = "Chess data visualization"
    cache = Cache(app.server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory'
    })

    @cache.memoize(timeout=3600)
    def get_dataframes(file1: str, file2: str) -> tuple:
        print("loading dataframes")
        return load_dataframe(file1), load_dataframe(file2)

    # players_df, games_df = get_dataframes(PLAYERS_FILENAME, REFORMATED_GAMES_FILENAME)
    players_df, games_df = get_dataframes(PLAYERS_FILENAME, 'reformated_games_truncated.pkl')

    app.layout = html.Div(
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
    app.run_server(debug=True)


if __name__ == "__main__":
    main()