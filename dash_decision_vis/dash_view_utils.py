from dash import html


def generate_dash_layout(plot_instances):
    layout = []
    for level, level_plots in plot_instances.items():
        row = html.Div([plot.layout() for plot in level_plots],
                       style={'display': 'flex', 'flex-wrap': 'wrap'})
        layout.append(row)

    return layout