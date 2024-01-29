Interactive Dash app to visualise sequential data splitting plots based of various features, akin to a manual decision tree.

## Auxiliary plot
To use aux plot, you should pass `aux_updating_func` to `DashApp`. `aux_updating_func` must return Plotly's `Figure` and accept `clickData` of one plot as an only argument.