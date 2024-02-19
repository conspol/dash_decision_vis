Interactive Dash app to visualise sequential data splitting plots based of various features, akin to a manual decision tree.

## Basic Usage
Initialize the app with your DataFrame and optional configurations:

``` python
from dash_decision_vis import DashApp
import pandas as pd

# Load your dataset
dataframe = pd.read_csv("path/to/your/dataset.csv")

# Optional: Define metadata and color mappings
# Metadata can also be pd.DataFrame
metadata = {'additional_info': ['Info 1', 'Info 2', ...]}
color_mapping = {0: 'blue', 1: 'red', ...}  # Map your labels to specific colors

# Initialize and run the Dash app
app = DashApp(dataframe, metadata=metadata, color_mapping=color_mapping)
app.run()
```


## Auxiliary plot
Click on any data point within the scatter plots to trigger an auxiliary visualization (for example detailed images or custom plots, see `aux_upd_funcs.img_show.aux_imshow`).
To use it either see `aux_upd_funcs` folder for implemented functions, or implement a custom function that takes click data as input and returns a Plotly figure. 
You should pass `aux_updating_func` to `DashApp`, which
must return Plotly's `Figure` and accept `clickData` of one plot as an only argument.

You can access point's metadata via point's `customdata` that is contained in `clickData`
and use it for plotting.

## Customization

### Color mapping
The app automatically generates a color mapping for scatter plot markers based on unique labels within your dataset, ensuring each category is distinctly colored for better visual differentiation.
You can customize color mappings for data labels through the `color_mapping` argument.

### Column exclusion
Pass a list of column names to `cols2exclude` to omit them from visualization.

### Metadata integration
If available, metadata can be utilized to enrich plot tooltips, offering additional context or information upon hovering over data points.
Metadata should have the same indexes as the main data, 
and will be available as each point's `customdata`.

### Legends from data
Optionally use a `label_legend` column in the DataFrame to customize legend entries.