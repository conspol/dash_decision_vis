import dash
from dash import html
from dash.dependencies import Input, Output, ALL
from .plot_node import PlotNode
from .callbacks import update_plots_cback
from .dash_view_utils import generate_dash_layout


class DashApp:
    def __init__(self, dataframe):
        self.df = dataframe
        self.app = dash.Dash(__name__)
        self.root_plot = PlotNode('0-0', self.df, self.df['A'].median(), 'A', 'B')
        self.plot_instances = {0: [self.root_plot]}
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = html.Div(id='plots-container', children=generate_dash_layout(self.plot_instances))

    def setup_callbacks(self):
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
        def update_plots(slider_values, x_values, y_values):
            return update_plots_cback(slider_values, x_values, y_values, plot_instances)

    def run(self):
        self.app.run_server(debug=True)