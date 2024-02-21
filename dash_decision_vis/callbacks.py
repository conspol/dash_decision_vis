from numbers import Real
from typing import Callable, Dict, List

import dash
import plotly.graph_objs as go
from dash import html
from dash.exceptions import PreventUpdate

from .dash_view_utils import generate_dash_layout_tree
from .type_vars import TPlotInstances
from .utils import update_child_plots


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

    current_plot = plot_instances[plot_id]
    update_type = ctx.triggered[0]['prop_id'].split('.')[1]

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
