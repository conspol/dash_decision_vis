import numpy as np
import plotly.express as px
from PIL import Image


def aux_imshow(clickData):
    # This should contain path to image.
    image_path = clickData['points'][0]['customdata'][1]
    img = Image.open(image_path)
    img_array = np.array(img)

    p1, p99 = np.percentile(img_array, (1, 99))
    img_array_clipped = np.clip(img_array, p1, p99)

    fig = px.imshow(img_array_clipped)

    fig.update_layout(xaxis_showticklabels=False, yaxis_showticklabels=False)

    return fig