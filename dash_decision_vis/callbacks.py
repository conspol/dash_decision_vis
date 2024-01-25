import dash
from dash.exceptions import PreventUpdate
import json
from .utils import reconstruct_flat_index, update_child_plots
from .dash_view_utils import generate_dash_layout


def update_plots_cback(slider_values, x_values, y_values, plot_instances):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    plot_id = trigger_id['index']
    depth, index = map(int, plot_id.split('-'))

    current_plot = plot_instances[depth][index]
    update_type = ctx.triggered[0]['prop_id'].split('.')[1]

    flat_index = reconstruct_flat_index(plot_id, plot_instances)

    max_depth = max(plot_instances.keys())
    if depth == max_depth:
        max_depth += 1

    if 'slider' in trigger_id['type']:  # Slider update
        current_plot.threshold = slider_values[flat_index]
    elif 'dynamic-dropdown-x' in trigger_id['type']:
        current_plot.x_col = x_values[flat_index]
    elif 'dynamic-dropdown-y' in trigger_id['type']:
        current_plot.y_col = y_values[flat_index]

    # Adjust the logic for child plot updates
    if update_type == 'value':  # Only update child plots if the slider was changed
        update_child_plots(current_plot, depth + 1, max_depth, plot_instances)

    layout = generate_dash_layout(plot_instances)
    return layout