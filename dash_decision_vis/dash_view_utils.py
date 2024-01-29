from typing import List

from dash import dcc, html


def generate_dash_layout(plot_instances):
    layout: List[html.Div] = []
    for level, level_plots in plot_instances.items():
        row = html.Div([plot.layout() for plot in level_plots],
                       style={'display': 'flex', 'flex-wrap': 'wrap'})
        layout.append(row)

    layout[0].children.append(dcc.Graph(id='aux-plot'))

    return layout
