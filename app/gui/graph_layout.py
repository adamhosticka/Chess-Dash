""""""

from dash import Dash, dcc, html
import pandas as pd


class GraphLayout:
    COMPONENT_ID = ""
    GRAPH_ID = ""
    GRAPH_WIDTH_PERCENT = 65
    CALLBACK = False

    def __init__(self, app: Dash, df: pd.DataFrame):
        self.app = app
        self.df = df
        self.children = self.get_children()

    def render(self):
        if self.CALLBACK:
            self.set_callback()
            self.children.append(dcc.Graph(id=self.GRAPH_ID))
        else:
            figure = self.get_figure()
            self.children.append(dcc.Graph(id=self.GRAPH_ID, figure=figure))

        return html.Div(
            id=self.COMPONENT_ID,
            children=[
                html.Br(),
                html.Div(
                    style={"width": f"{self.GRAPH_WIDTH_PERCENT}%", "margin": "auto"},
                    children=self.children,
                )
            ]
        )

    def get_figure(self):
        pass

    def get_children(self) -> list:
        return []

    def set_callback(self) -> None:
        pass
