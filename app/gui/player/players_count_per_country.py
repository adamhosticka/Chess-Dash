""""""

from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout
from app.src.format_data.gui_format_players import get_players_count_and_rating_per_country


class PlayersCountPerCountry(GraphLayout):
    COMPONENT_ID = 'players-count-per-country'
    GRAPH_ID = 'players-count-per-country-graph'
    GRAPH_WIDTH_PERCENT = 80

    def get_figure(self) -> html.Div:
        dff = get_players_count_and_rating_per_country(self.df)

        return px.choropleth(
            data_frame=dff,
            title="Number of players per country",
            locations='country',
            color='players count',
            color_continuous_scale=px.colors.sequential.Darkmint
        )
