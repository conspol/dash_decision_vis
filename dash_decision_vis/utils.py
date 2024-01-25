from .plot_node import PlotNode
import numpy as np
from typing import Dict, List


def reconstruct_flat_index(target_plot_id, plot_instances):
    flat_index = 0
    for depth, plots in plot_instances.items():
        for index, plot in enumerate(plots):
            if plot.id == target_plot_id:
                return flat_index
            flat_index += 1
    raise ValueError(f"Plot with ID {target_plot_id} not found")


def update_child_plots(parent_plot: PlotNode, depth, max_depth, plot_instances: Dict[int, List]) -> None:
    if depth > max_depth:
        return

    below_threshold, above_threshold = PlotNode.split_data(parent_plot.data, parent_plot.threshold, parent_plot.x_col)
    
    for i, threshold_data in enumerate([below_threshold, above_threshold]):
        child_id = f"{depth}-{i}"
        existing_plot = next((p for p in plot_instances.get(depth, []) if p.id == child_id), None)

        if existing_plot:
            existing_plot.data = threshold_data

        else:
            # Create a new child plot if it doesn't exist
            new_plot = PlotNode(
                child_id,
                threshold_data,
                np.median(threshold_data[parent_plot.x_col]) if len(threshold_data) > 0 else 0,
                parent_plot.x_col,
                parent_plot.y_col,
                parent=parent_plot,
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