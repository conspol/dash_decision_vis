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
    def find_children_ids(parent_id):
        return [f"{parent_id}-0" if parent_id != ''
                else "0", f"{parent_id}-1" if parent_id != '' else "1"]

    def generate_plot_layout(plot_id, level):
        plot = plot_instances.get(plot_id)
        if plot:
            return html.Div(
                plot.layout(),
                style={
                    'width': f'{100 / (2 ** level)}%',
                    'display': 'inline-block'
                },
            )
        return None

    def generate_level_layout(parent_ids, level):
        children_ids = []
        level_plots = []
        for parent_id in parent_ids:
            for child_id in find_children_ids(parent_id):
                child_layout = generate_plot_layout(child_id, level)
                if child_layout:
                    level_plots.append(child_layout)
                    children_ids.append(child_id)
        return level_plots, children_ids

    # Initialize the main container with overflow for horizontal scrolling
    layout = html.Div(
        id='plot-tree-container',
        style={
            'width': 'max-content',
            'display': 'block',
            'overflow-x': 'auto',
        },
        children=[],
    )

    current_level = 0
    current_level_ids = ['']

    first_row_added = False

    while current_level_ids:
        level_layout, next_level_ids = generate_level_layout(current_level_ids, current_level)
        # Special case for the first row to include aux-plot
        if not level_layout and not first_row_added: 
            level_layout = [dcc.Graph(id='aux-plot')]
            first_row_added = True
        elif not level_layout:
            break

        row = html.Div(level_layout, style={'display': 'flex', 'justify-content': 'center'})
        layout.children.append(row)

        # Add aux-plot to the first row
        if current_level == 0 and not first_row_added:
            row.children.append(dcc.Graph(id='aux-plot'))
            first_row_added = True

        current_level_ids = next_level_ids
        current_level += 1

    return layout
