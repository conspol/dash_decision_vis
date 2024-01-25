from dash import html, dcc
import plotly.graph_objs as go


class PlotNode:
    def __init__(self, id, data, threshold, x_col, y_col, parent=None):
        self.id = id
        self.data = data
        self.threshold = threshold
        self.x_col = x_col
        self.y_col = y_col
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def layout(self):
        fig = go.Figure()
        for label, df_group in self.data.groupby('label'):
            fig.add_trace(go.Scatter(
                x=df_group[self.x_col], 
                y=df_group[self.y_col], 
                mode='markers', 
                name=f'Label {label}',
                marker=dict(color='red' if label == 1 else 'blue')
            ))
        fig.add_shape(type="line", x0=self.threshold, y0=self.data[self.y_col].min(), x1=self.threshold, y1=self.data[self.y_col].max(), line=dict(color="RoyalBlue", width=2))
        
        title_text = f"Split by {self.parent.x_col} at {self.parent.threshold}" if self.parent else "Root Plot"
        fig.update_layout(title=title_text)

        return html.Div([
            dcc.Dropdown(
                id={'type': 'dynamic-dropdown-x', 'index': self.id},
                options=[{'label': col, 'value': col} for col in self.data.columns],
                value=self.x_col,
                clearable=False,
            ),
            dcc.Dropdown(
                id={'type': 'dynamic-dropdown-y', 'index': self.id},
                options=[{'label': col, 'value': col} for col in self.data.columns],
                value=self.y_col,
                clearable=False,
            ),
            dcc.Graph(id={'type': 'dynamic-graph', 'index': self.id}, figure=fig),
            dcc.Slider(
                id={'type': 'dynamic-slider', 'index': self.id},
                min=self.data[self.x_col].min(),
                max=self.data[self.x_col].max(),
                value=self.threshold,
                step=(self.data[self.x_col].max() - self.data[self.x_col].min()) / 1000,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ], style={'width': '50%', 'minWidth': '300px', 'boxSizing': 'border-box', 'padding': '10px'})

    @staticmethod
    def split_data(data, threshold, x_col):
        below_threshold = data[data[x_col] <= threshold]
        above_threshold = data[data[x_col] > threshold]
        return below_threshold, above_threshold