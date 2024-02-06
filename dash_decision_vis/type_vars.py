from typing import List, Dict, Union
from .plot_node import PlotNode


TPlotInstances = Dict[int, List[Union['TPlotInstances', PlotNode]]]