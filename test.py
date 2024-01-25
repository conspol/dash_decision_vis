from dash_decision_vis.app import DashApp
import pandas as pd
import numpy as np


if __name__ == '__main__':
    df = pd.DataFrame(np.random.rand(100, 4), columns=['A', 'B', 'C', 'D'])
    df['label'] = np.random.choice([0, 1], size=len(df))

    dash_app = DashApp(df)
    dash_app.run()
