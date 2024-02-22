from numbers import Real
from typing import Callable, Dict, List

import dash
import plotly.graph_objs as go
from dash import html
from dash.exceptions import PreventUpdate

from .dash_view_utils import generate_dash_layout_tree
from .type_vars import TPlotInstances
from .utils import (
    get_node_depth,
    get_tree_depth,
    update_child_plots,
    create_child_plots_pair,
)


def update_plots_cback(
    slider_values: List[Real],
    x_values: List[str],
    y_values: List[str],
    plot_instances: TPlotInstances,
    update_on_yaxis: bool = False,
) -> List[html.Div]:
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered_id
    plot_id = trigger_id['index']

    # depth, index = map(int, plot_id.split('-'))

    current_plot = plot_instances[plot_id]
    update_type = ctx.triggered[0]['prop_id'].split('.')[1]

    # flat_index = reconstruct_flat_index(plot_id, plot_instances)

    # max_depth = max(plot_instances.keys())
    # if depth == max_depth:
    #     max_depth += 1

    tree_depth = get_tree_depth(current_plot)
    current_depth = get_node_depth(current_plot)
    if current_depth == tree_depth:
        below_thr_node, above_thr_node = create_child_plots_pair(current_plot)

    if 'slider' in trigger_id['type']:  # Slider update
        current_plot.threshold = ctx.triggered[0]['value']
    elif 'dynamic-dropdown-x' in trigger_id['type']:
        current_plot.x_col = ctx.triggered[0]['value']
        current_plot.reset_threshold()
    elif 'dynamic-dropdown-y' in trigger_id['type']:
        current_plot.y_col = ctx.triggered[0]['value']
        if update_on_yaxis:
            current_plot.reset_threshold()

    # Only update child plots if the slider was changed
    if update_type == 'value':
        update_child_plots(
            current_plot,
            upd_plot_instances=True,
            plot_instances=plot_instances,
        )

    layout = generate_dash_layout_tree(plot_instances)
    return layout


def update_aux_plot_cback(
    clickData: List[Dict],
    aux_updating_func: Callable[[Dict], go.Figure],
    plot_instances: TPlotInstances,
) -> go.Figure:
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    plot_id = ctx.triggered_id['index']
    for i_, d_ in enumerate(ctx.inputs_list[0]):
        if d_['id']['index'] == plot_id:
            flat_index = i_
            return aux_updating_func(clickData[flat_index])
