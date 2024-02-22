from typing import List

from dash import dcc, html

from .type_vars import TPlotInstances
from .utils import group_by_key_length


def generate_dash_layout_simple(plot_instances: TPlotInstances) -> List[html.Div]:
    layout: List[html.Div] = []
    grouped_plots = group_by_key_length(plot_instances)
    for level, level_plots in grouped_plots.items():
        row = html.Div([plot.layout() for plot in level_plots],
                       style={'display': 'flex'})
        layout.append(row)

    layout[0].children.append(dcc.Graph(id='aux-plot'))

    return layout


def generate_dash_layout_tree(plot_instances: TPlotInstances) -> html.Div:
    max_depth = max(
        (plot_id.count('-') for plot_id in plot_instances), 
        default=0
    ) + 1

    def generate_table(max_depth):
        table = [
            [
                html.Td(
                    style={
                        'min-width': '500px', 
                        'visibility': 'hidden', 
                        'text-align': 'center'
                    }
                ) for _ in range(2**max_depth)
            ] for _ in range(max_depth)
        ]
        
        for plot_id, plot in plot_instances.items():
            depth = plot_id.count('-')
            index = int('0' + plot_id.replace('-', ''), 2) if plot_id else 0
            position = index * (2 ** (max_depth - depth - 1))
            position = min(position, 2**max_depth - 1)
            table[depth][position] = html.Td(
                plot.layout(), 
                style={
                    'min-width': '500px', 
                    'text-align': 'center'
                }
            )

        return html.Table(
            [html.Tr(row) for row in table], 
            style={
                # 'width': '100%', 
                # 'table-layout': 'fixed'
            }
        )

    layout = html.Div(
        style={
            'display': 'flex', 
            'height': '100vh'
        },
        children=[
            html.Div(
                style={
                    'overflow': 'auto', 
                    'flex-grow': '1'
                },
                children=[generate_table(max_depth)]
            ),
            html.Div(
                style={
                    'min-width': '40vw', 
                    # 'height': '100vh', 
                    'position': 'fixed', 
                    'right': '0', 
                    'top': '0'
                },
                children=[dcc.Graph(id='aux-plot')]
            )
        ]
    )

    return layout
