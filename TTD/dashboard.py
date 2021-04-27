

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
import pandas as pd

df = px.data.tips()
days = df.day.unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="bar-chart"),
    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
])




@app.callback(
    Output("bar-chart", "figure"), 
    [Input("interval-component", "n_intervals")])
def update_bar_chart(day):
    
    data = [["buy", random.randint(10,20)], ["sell", random.randint(5,10)]]
    df = pd.DataFrame(data, columns=['Action', 'Count'])
    


    fig = px.bar(df, x="Action", y="Count")
    return fig

app.run_server(debug=True)


