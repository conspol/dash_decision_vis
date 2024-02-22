from typing import List
from collections import deque, defaultdict

from dash import dcc, html

from .type_vars import TPlotInstances
from .utils import group_by_key_length, get_node_depth, get_tree_depth


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

    def generate_table_dfs():
        """
        This function should be able to produce a table from any tree,
        not just a binary one.
        """
        table = defaultdict(list)
        irow = 0
        stack = [plot_instances['0']]
        max_depth = get_tree_depth(stack[0])

        while stack:
            current_plot = stack.pop()

            if irow == 0:
                for i_ in range(get_node_depth(current_plot) - 1):
                    table[i_].append(
                        html.Td(style={'background-color': 'whitesmoke'}))
                    irow += 1 

            table[irow].append(html.Td(
                current_plot.layout(),
                style={
                    'min-width': '500px', 
                    'text-align': 'center'
                }
            ))
            if current_plot.children:
                stack.extend(current_plot.children[::-1])
                irow += 1
            else:
                rows2fill = max_depth - irow - 1
                for _ in range(rows2fill):
                    irow += 1
                    table[irow].append(html.Td())
                irow = 0

        return html.Table(
            [html.Tr(row) for row in table.values()], 
            style={
                # 'width': '100%', 
                # 'table-layout': 'fixed'
            }
        )

    html_table = generate_table_dfs()

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
                children=[html_table]
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
