import plotly
import plotly.express as px
import pandas as pd
import json

def create_plot(x_var, y_var):
    """ Generate graphJSON file for Plotly plot """

    FILE_PATH = 'application/star_data.csv'
    TARGET_VAR = 'star_type'
    SIZE_VAR = 'r_clipped'
    WIDTH = 1000
    HEIGHT = 600

    # Get the data
    df = pd.read_csv(FILE_PATH)
    fig = px.scatter(df, x=x_var, y=y_var, color=TARGET_VAR, size=SIZE_VAR, 
                     width=WIDTH, height=HEIGHT)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
