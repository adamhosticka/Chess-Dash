""""""

import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.helpers.gui_config import GAME_COLOR
from app.utils.format_graph_labels import format_labels


class RatedRatingCorrelation(GraphLayout):
    COMPONENT_ID = 'rated-rating-correlation'
    GRAPH_ID = 'rated-rating-correlation-graph'

    def get_figure(self):
        df_copy = self.df.copy()
        df_copy['rating_mean'] = self.df.loc[:, ['white_rating', 'black_rating']].sum(axis=1)
        dff = df_copy.groupby('rated')['rating_mean'].mean().reset_index()

        fig = px.bar(
            data_frame=dff,
            x='rated',
            y='rating_mean',
            labels=format_labels(['rating_mean']),
            title="Rated vs. non-rated games mean rating",
        )
        fig.update_traces(marker_color=GAME_COLOR, width=0.40)

        return fig
