""""""

from dash import html
import plotly.express as px

from app.gui.graph_layout import GraphLayout


class PlayersCountPerCountry(GraphLayout):
    COMPONENT_ID = 'players-count-per-country'
    GRAPH_ID = 'players-count-per-country-graph'
    GRAPH_WIDTH_PERCENT = 80

    def get_figure(self) -> html.Div:

        dff = self.df.groupby('country')['username'].count().reset_index()

        return px.choropleth(
            data_frame=dff,
            title="Number of players per country",
            locations='country',
            color='username',
            labels={"username": "players count"},
            color_continuous_scale=px.colors.sequential.Darkmint
        )
