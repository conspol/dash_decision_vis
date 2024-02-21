from typing import Iterator

from .plot_node import PlotNode
from .type_vars import TPlotInstances


def reconstruct_flat_index(
    target_plot_id: str,
    plot_instances: TPlotInstances,
) -> int:
    raise DeprecationWarning("This function is most likely not doing "
                             "what it should anymore.")
    flat_index = 0
    for depth, plots in plot_instances.items():
        for index, plot in enumerate(plots):
            if plot.id == target_plot_id:
                return flat_index
            flat_index += 1
    raise ValueError(f"Plot with ID {target_plot_id} not found")

    
def create_child_plots_pair(
    parent_plot: PlotNode,
) -> tuple[PlotNode, PlotNode]:
    data_below_thr, data_above_thr = PlotNode.split_data(
            parent_plot.data, parent_plot.threshold, parent_plot.x_col)
    
    # parent_depth = get_node_depth(parent_plot)
    below_plot = PlotNode(
        data=data_below_thr,
        id='0',
        x_col=parent_plot.x_col,
        y_col=parent_plot.y_col,
        parent=parent_plot,
        metadata=parent_plot.get_metadata_loc(data_below_thr.index),
        color_mapping=parent_plot.color_mapping,
    )

    above_plot = PlotNode(
        data=data_above_thr,
        id='1',
        x_col=parent_plot.x_col,
        y_col=parent_plot.y_col,
        parent=parent_plot,
        metadata=parent_plot.get_metadata_loc(data_above_thr.index),
        color_mapping=parent_plot.color_mapping,
    )

    parent_plot.children = [below_plot, above_plot]

    return below_plot, above_plot


def update_child_plots(
    parent_plot: PlotNode,
    upd_plot_instances: bool = False,
    plot_instances: TPlotInstances = None,
) -> None:
    below_threshold, above_threshold = PlotNode.split_data(
            parent_plot.data, parent_plot.threshold, parent_plot.x_col)

    enumerate_data = enumerate([below_threshold, above_threshold])

    for plot_, (i_, data_) in zip(parent_plot.children,
                                  enumerate_data):
        plot_.data = data_
        plot_.metadata = parent_plot.get_metadata_loc(data_.index)
        update_child_plots(plot_, upd_plot_instances=False)
    
    if upd_plot_instances:
        plot_instances.clear()
        for plot_ in traverse_whole_tree_gen(parent_plot):
            plot_instances[plot_.id] = plot_
            # depth_index = get_node_depth(plot_) - 1
            # if depth_index not in plot_instances:
            #     plot_instances[depth_index] = []
            # plot_instances[depth_index].append(plot_)


def traverse_plots_gen(node: PlotNode) -> Iterator[PlotNode]:
    yield node
    yield from traverse_children_gen(node)


def traverse_children_gen(node: PlotNode) -> Iterator[PlotNode]:
    for child in node.children:
        yield child
        yield from traverse_children_gen(child)


def traverse_whole_tree_gen(node: PlotNode) -> Iterator[PlotNode]:
    while node.parent:
        node = node.parent
    yield from traverse_plots_gen(node)
    

def get_node_depth(node: PlotNode) -> int:
    depth = 1
    while node.parent:
        depth += 1
        node = node.parent
    return depth


def get_subtree_depth(root: PlotNode) -> int:
    # iterative
    depth = 1
    stack = [(root, depth)]
    while stack:
        current_node, current_depth = stack.pop()
        depth = max(depth, current_depth)
        for child in current_node.children:
            stack.append((child, current_depth + 1))

    return depth


def get_tree_depth(any_node: PlotNode) -> int:
    current_depth = get_node_depth(any_node)
    subtree_depth = get_subtree_depth(any_node)
    return subtree_depth + current_depth - 1 
 

def group_by_key_length(input_dict):
    grouped_dict = {}
    for key, value in input_dict.items():
        parts_count = key.count('-') + 1
        
        if parts_count not in grouped_dict:
            grouped_dict[parts_count] = []
        
        grouped_dict[parts_count].append(value)
    
    return grouped_dict
