from typing import Dict, List

from .plot_node import PlotNode
from .type_vars import TPlotInstances


def reconstruct_flat_index(
    target_plot_id: str,
    plot_instances: TPlotInstances,
) -> int:
    flat_index = 0
    for depth, plots in plot_instances.items():
        for index, plot in enumerate(plots):
            if plot.id == target_plot_id:
                return flat_index
            flat_index += 1
    raise ValueError(f"Plot with ID {target_plot_id} not found")


def update_child_plots(
    parent_plot: PlotNode,
    depth: int,
    max_depth: int, 
    plot_instances: TPlotInstances,
) -> None:
    if depth > max_depth:
        return

    below_threshold, above_threshold = PlotNode.split_data(parent_plot.data, parent_plot.threshold, parent_plot.x_col)
    
    for i, threshold_data in enumerate([below_threshold, above_threshold]):
        child_id = f"{depth}-{i}"
        existing_plot = next((p for p in plot_instances.get(depth, []) if p.id == child_id), None)

        if existing_plot:
            existing_plot.parent = parent_plot
            existing_plot.data = threshold_data
            existing_plot.metadata = parent_plot.get_metadata_loc(threshold_data.index)

        else:
            # Create a new child plot if it doesn't exist
            new_plot = PlotNode(
                child_id,
                threshold_data,
                x_col=parent_plot.x_col,
                y_col=parent_plot.y_col,
                parent=parent_plot,
                metadata=parent_plot.get_metadata_loc(threshold_data.index),
            )

            if depth not in plot_instances:
                plot_instances[depth] = []
            plot_instances[depth].append(new_plot)
            parent_plot.children.append(new_plot)

    # Recursively update children of the new/updated child plots
    for child_plot in parent_plot.children:
        update_child_plots(child_plot, depth + 1, max_depth, plot_instances)


def traverse_plots(plot: PlotNode):
    yield plot
    for child in plot.children:
        yield from traverse_plots(child)