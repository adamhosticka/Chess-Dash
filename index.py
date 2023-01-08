"""Main application."""
from argparse import ArgumentParser

from flask_caching import Cache
from dash import Dash
from dash_bootstrap_components.themes import GRID

from app.gui.app_layout import render_app_layout
from app.helpers.data_filenames import PLAYERS_FILENAME, REFORMATED_GAMES_FILENAME
from app.utils.dataframe_utils import load_dataframe


def run_app(debug: bool):
    """Run application

    :param: bool debug: If true, run application in the debugging mode.
    """

    app = Dash(
        __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=[GRID]
    )
    app.title = "Chess data visualization"

    cache = Cache(app.server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory'
    })

    @cache.memoize(timeout=3600)
    def get_dataframes_cached(file1: str, file2: str) -> tuple:
        return load_dataframe(file1), load_dataframe(file2)

    if debug:
        players_df, games_df = get_dataframes_cached(PLAYERS_FILENAME, REFORMATED_GAMES_FILENAME)
    else:
        players_df, games_df = load_dataframe(PLAYERS_FILENAME), load_dataframe(REFORMATED_GAMES_FILENAME)

    app.layout = render_app_layout(app, players_df, games_df)
    app.run_server(debug=debug)


if __name__ == "__main__":
    parser = ArgumentParser(description="Run application.")
    parser.add_argument("-d", "--debug",
                        default=False,
                        action='store_true',
                        help="Turn on debugging mode")
    args = parser.parse_args()

    run_app(args.debug)
