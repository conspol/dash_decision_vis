from numbers import Real
from typing import Callable, Dict, List, Optional

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html
from dash.dependencies import ALL, Input, Output

from .callbacks import update_aux_plot_cback, update_plots_cback
from .dash_view_utils import generate_dash_layout_tree
from .plot_node import PlotNode
from .type_vars import TPlotInstances


class DashApp:
    def __init__(
        self,
        dataframe: pd.DataFrame,
        metadata: Optional[Dict | pd.DataFrame] = None,
        cols2exclude: Optional[List[str]] = None,
        debug_app: bool = False,
        use_reloader_app: bool = False,
        aux_updating_func: Callable[[List], go.Figure] = lambda: go.Figure(),
        color_mapping: Optional[Dict] = None,
        update_on_yaxis: bool = False,
    ):
        self.df = dataframe
        self.app = dash.Dash(__name__)

        self._debug_flag = debug_app
        self._use_reloader_flag = use_reloader_app

        self.metadata = metadata
        self.aux_updating_func = aux_updating_func
        self.update_on_yaxis = update_on_yaxis

        if color_mapping is None:
            unique_labels = self.df['label'].unique()
            colors = px.colors.qualitative.Plotly 
            color_mapping = {label: colors[i % len(colors)]
                                  for i, label in enumerate(unique_labels)}

        self.color_mapping = color_mapping

        if cols2exclude:
            if isinstance(cols2exclude, list) and all(isinstance(col, str) for col in cols2exclude):
                if all(col in self.df.columns for col in cols2exclude):
                    self.df.drop(columns=cols2exclude, inplace=True)
                else:
                    raise ValueError("One or more columns in `cols2exclude` do not exist in the dataframe")
            else:
                raise TypeError("`cols2exclude` must be a list of strings")

        self.root_plot = PlotNode(
            data=self.df,
            id='0',
            metadata=metadata,
            color_mapping=self.color_mapping,
        )

        self.plot_instances: TPlotInstances = {'0': self.root_plot}
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self) -> None:
        self.app.layout = html.Div(id='plots-container', children=generate_dash_layout_tree(self.plot_instances))

    def setup_callbacks(self) -> None:
        plot_instances = self.plot_instances

        @self.app.callback(
            Output('plots-container', 'children'),
            [
                Input({'type': 'dynamic-slider', 'index': ALL}, 'value'),
                Input({'type': 'dynamic-dropdown-x', 'index': ALL}, 'value'),
                Input({'type': 'dynamic-dropdown-y', 'index': ALL}, 'value'),
            ],
            prevent_initial_call=True
        )
        def update_plots(
            slider_values: List[Real],
            x_values: List[str],
            y_values: List[str],
        ) -> List[html.Div]:
            return update_plots_cback(
                slider_values,
                x_values,
                y_values,
                plot_instances,
                self.update_on_yaxis
            )

        @self.app.callback(
            Output('aux-plot', 'figure'),
            Input({'type': 'dynamic-graph', 'index': ALL}, 'clickData'),
            prevent_initial_call=True,
        )
        def update_aux_plot(clickData: Dict) -> go.Figure:
            return update_aux_plot_cback(
                clickData,
                self.aux_updating_func,
                plot_instances,
            )

    def run(self):
        self.app.run_server(debug=self._debug_flag, use_reloader=self._use_reloader_flag)