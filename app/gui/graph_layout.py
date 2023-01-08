"""Graph layout template class."""

from dash import Dash, dcc, html
import pandas as pd


class GraphLayout:
    """Base class for graphs."""

    COMPONENT_ID = ""
    GRAPH_ID = ""
    GRAPH_WIDTH_PERCENT = 65
    CALLBACK = False

    def __init__(self, app: Dash, df: pd.DataFrame):
        """Initialize class.

        :param: Dash app: Dash application.
        :param pd.DataFrame df: Dataframe containing to be displayed data.
        """
        self.app = app
        self.df = df
        self.children = self.get_children()

    def render(self) -> html.Div:
        """Render graph.

        :return: Graph.
        :rtype: html.Div.
        """
        if self.CALLBACK:
            self.set_callback()
            self.children.append(dcc.Graph(id=self.GRAPH_ID))
        else:
            figure = self.get_figure()
            self.children.append(dcc.Graph(id=self.GRAPH_ID, figure=figure))
        if self.set_text():
            self.children.append(self.set_text())
            self.children.extend([html.Br(), html.Br()])

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

    def get_figure(self) -> html.Div:
        """Get graph figure.

        :return: Figure.
        :rtype: html.Div.
        """
        # Disable pylint E1111
        raise NotImplementedError

    def get_children(self) -> list:
        """Get children of html.Div containing graph.

        :return: List of children.
        :rtype: list.
        """
        return []

    def set_callback(self) -> None:
        """Set callback for graph components."""

    @staticmethod
    def set_text():
        """Set text under graph."""
        return None
