import pandas as pd
import plotly.graph_objects as go
from sklearn.datasets import make_classification

from dash_decision_vis.app import DashApp

from typing import Dict

def aux_display_text(clickData: Dict) -> go.Figure:
    # Extract text from the clicked point's customdata.
    text_content = clickData['points'][0]['customdata'][0]

    fig = go.Figure()

    # Use a scatter plot for displaying text
    fig.add_trace(go.Scatter(x=[0], y=[0], text=[text_content], mode="text"))

    # Update layout to hide axis lines and ticks, 
    # and set margins to minimize white space
    fig.update_layout(xaxis=dict(showgrid=False, zeroline=False,
                                 showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False,
                                 showticklabels=False),
                      margin=dict(l=20, r=20, t=20, b=20))

    return fig


if __name__ == '__main__':
    # Generate synthetic dataset with 5 labels
    X, y = make_classification(
        n_samples=100,
        n_features=4,
        n_classes=4,
        n_clusters_per_class=1,
        random_state=42,
    )
    feature_names = ['Feature1', 'Feature2', 'Feature3', 'Feature4']
    df = pd.DataFrame(X, columns=feature_names)
    df['label'] = y

    # Assigning legend names based on labels
    df['label_legend'] = [f'Category {label}' for label in y]

    # Example metadata
    metadata = pd.DataFrame({
        'text': [f"Detail info for point {i}" for i in range(len(df))]
    }, index=df.index)

    # Define a color mapping for 5 labels
    color_mapping = {0: 'blue', 1: 'red', 2: 'green', 3: 'orange', 4: 'purple'}

    dash_app = DashApp(
        dataframe=df,
        metadata=metadata,
        color_mapping=color_mapping,
        aux_updating_func=aux_display_text,
        debug_app=True,
        # Set to True if you want the app to reload on code changes
        use_reloader_app=False,
    )
    dash_app.run()
