from numbers import Real
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html

from loguru import logger as lg


class PlotNode:
    def __init__(
        self,
        id: str,
        data: pd.DataFrame,
        threshold: Optional[Real] = None,
        x_col: Optional[str] = None,
        y_col: Optional[str] = None,
        parent: Optional['PlotNode'] = None,
        metadata: Optional[Dict | pd.DataFrame] = None,
        color_mapping: Optional[Dict] = None,
    ):
        self.id = id
        self.data = data

        if metadata is not None:
            if isinstance(metadata, dict):
                metadata = pd.DataFrame(metadata)
            elif not isinstance(metadata, pd.DataFrame):
                raise TypeError("`metadata` must be either a dict "
                                "or a pandas DataFrame")

            if not metadata.index.equals(self.data.index):
                raise ValueError("The index of `metadata` does not "
                                 "match the index of the main dataframe")

        self.metadata = metadata

        if x_col is None:
            self.x_col = self.data.columns[0]
        else:
            self.x_col = x_col

        if y_col is None:
            self.y_col = self.data.columns[1]
        else:
            self.y_col = y_col

        if threshold is None:
            self.threshold = self._get_default_threshold()
        else:
            self.threshold = threshold

        if color_mapping is None:
            unique_labels = self.data['label'].unique()
            colors = px.colors.qualitative.Plotly 
            self.color_mapping = {label: colors[i % len(colors)]
                                  for i, label in enumerate(unique_labels)}
        else:
            self.color_mapping = color_mapping

        self.parent = parent
        self.children = []

    def add_child(self, child: 'PlotNode') -> None:
        self.children.append(child)

    def layout(self) -> html.Div:
        fig = go.Figure()
        for label, df_group in self.data.groupby('label'):
            if self.metadata is not None:
                aligned_metadata = self.get_metadata_loc(df_group.index)
                custom_data = aligned_metadata.to_records(index=False)
                text_data = aligned_metadata['text']
                hovertemplate = (
                    f"{self.x_col}: %{{x}}<br>" +
                    f"{self.y_col}: %{{y}}<br>" +
                    "%{text}<br>"
                )
            else:
                custom_data = None
                text_data = None
                hovertemplate = None

            marker_color = self.color_mapping[label]

            if 'label_legend' in self.data.columns:
                unique_legends = df_group['label_legend'].unique()
                
                if len(unique_legends) > 1:
                    lg.warn("Inconsistent `label_legend` values for "
                            f"label: {label}. Using first value for legend.")
                legend_name = unique_legends[0]

            else:
                legend_name = f'{label}'

            fig.add_trace(go.Scatter(
                x=df_group[self.x_col], 
                y=df_group[self.y_col], 
                mode='markers', 
                name=legend_name,
                marker=dict(color=marker_color),
                customdata=custom_data,
                text=text_data,
                hovertemplate=hovertemplate,
            ))

        fig.add_shape(
            type="line",
            x0=self.threshold,
            y0=self.data[self.y_col].min(),
            x1=self.threshold,
            y1=self.data[self.y_col].max(),
            line=dict(color="RoyalBlue", width=2)
        )

        title_text = (f"Split by {self.parent.x_col} at {self.parent.threshold}"
                      if self.parent else "Root Plot")
        fig.update_layout(title=title_text)

        return html.Div([
            dcc.Dropdown(
                id={'type': 'dynamic-dropdown-x', 'index': self.id},
                options=[{'label': col, 'value': col}
                         for col in self.data.columns],
                value=self.x_col,
                clearable=False,
            ),
            dcc.Dropdown(
                id={'type': 'dynamic-dropdown-y', 'index': self.id},
                options=[{'label': col, 'value': col}
                         for col in self.data.columns],
                value=self.y_col,
                clearable=False,
            ),
            dcc.Graph(id={'type': 'dynamic-graph', 'index': self.id},
                      figure=fig),
            dcc.Slider(
                id={'type': 'dynamic-slider', 'index': self.id},
                min=self.data[self.x_col].min(),
                max=self.data[self.x_col].max(),
                value=self.threshold,
                step=(self.data[self.x_col].max() -
                      self.data[self.x_col].min()) / 1000,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ], style={
            'width': '50%',
            'minWidth': '300px',
            'boxSizing': 'border-box',
            'padding': '10px'
        })

    @staticmethod
    def split_data(
        data: pd.DataFrame,
        threshold: Real,
        x_col: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        below_threshold = data[data[x_col] <= threshold]
        above_threshold = data[data[x_col] > threshold]
        return below_threshold, above_threshold

    def reset_threshold(self):
        self.threshold = self._get_default_threshold()

    def _get_default_threshold(self) -> Real:
        return np.median(self.data[self.x_col])

    def get_metadata_loc(self, indices: pd.Index) -> Optional[pd.DataFrame]:
        if self.metadata is None:
            return None
        else:
            return self.metadata.loc[indices]
