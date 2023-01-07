""""""

import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.helpers.gui_config import GAME_COLOR
from app.src.format_data.gui_format_games import get_rated_rating_correlation
from app.utils.format_graph_labels import format_labels


class RatedRatingCorrelation(GraphLayout):
    COMPONENT_ID = 'rated-rating-correlation'
    GRAPH_ID = 'rated-rating-correlation-graph'

    def get_figure(self):
        dff = get_rated_rating_correlation(self.df)

        fig = px.bar(
            data_frame=dff,
            x='rated',
            y='rating_mean',
            labels=format_labels(['rating_mean']),
            title="Rated vs. non-rated games mean rating",
        )
        fig.update_traces(marker_color=GAME_COLOR, width=0.40)

        return fig
