import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
import pandas as pd
import dash_daq as daq
import redis
import dash_bootstrap_components as dbc
import dash_html_components as html
import datetime as dt
import plotly.graph_objects as go

from modules.dashboard_figures import *


r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
r.delete('trigger-time')



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col(html.H1(children="Twitch Trades Doge")),
        dbc.Col(html.Img(src="/assets/doge.png",style={'size':'35%'}))]),
    
    
    html.Div(children=[
    dcc.Graph(id="table"),
    dcc.Graph(id="bar-chart"),
    daq.LEDDisplay(
        id='clock',
        label="Default",
        value='5:00'
    ),
    dcc.Interval(
            id='interval-short',
            interval=1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-long',
            interval=5000, # in milliseconds
            n_intervals=0
        )
])
])




@app.callback(
    Output("bar-chart", "figure"), 
    [Input("interval-short", "n_intervals")])
def update_bar_chart(day):
    #r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    fig = gen_barchart()
    return fig



@app.callback(
    Output("table", "figure"), 
    [Input("interval-long", "n_intervals")])
def update_table(day):
    fig = gen_table()
    return fig
    
   
@app.callback(
    Output("clock", "value"), 
    [Input("interval-short", "n_intervals")])
def update_clock(value):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)

    #reset the clock, if old
    if  (r.get('trigger-time') == None):
        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=30)))
        print(f"trigger has been reset to {r.get('trigger-time')}")
        for x in ["buy","vote","sell","threshhold"]:
            r.delete(x)

    if (dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f') <= dt.datetime.now()):
        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=30)))
        print(f"trigger has been reset to {r.get('trigger-time')}")
        for x in ["buy","vote","sell","threshhold"]:
            r.delete(x)


    trigger = dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f')
    #get current clock time
    time_left = trigger - dt.datetime.now()
    
    return str(time_left)[2:7]
    


app.run_server(debug=True)


