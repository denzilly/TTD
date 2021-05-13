import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
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
from modules.vote_logic import *

r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
r.delete('trigger-time')
reset(r)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(children=[
    html.Div(
    
    dbc.Row([
        
            dbc.Col(gif.GifPlayer(
                gif='assets/spinnymed.gif',
                still='assets/doge.png',
                autoplay=True
            ), width="auto"),
        dbc.Col(html.H3(children="Twitch Trades Doge")),

            dbc.Col(gif.GifPlayer(
                gif='assets/spinnymed.gif',
                still='assets/doge.png',
                autoplay=True
            ), width="auto"),
        


    ]
    ),
    style={'height':'150px' }),
    
    
    
    dcc.Graph(id="table"),
    dcc.Graph(id="timertable"),
    dcc.Graph(id="bar-chart"),
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
    fig = gen_table_top()
    return fig

  
   
@app.callback(
    Output("timertable", "figure"), 
    [Input("interval-short", "n_intervals")])
def update_clock(value):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)

    #SET THE TIMER LENGTH
    clock = 10


    #reset the clock, if old
    if  (r.get('trigger-time') == None):
        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=clock)))
        print(f"trigger has been reset to {r.get('trigger-time')}")
        reset(r)

    if (dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f') <= dt.datetime.now()):
        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=clock)))
        
        #perform trade
        vote(r)

        #force position neutral for now
        r.set("position", "neutral")

        print(f"trigger has been reset to {r.get('trigger-time')}")
        reset(r)


    trigger = dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f')
    #get current clock time
    time_left = trigger - dt.datetime.now()

    data = {}

    for key in ["buy","sell","votes","hold"]:
        data[key] = len(r.lrange(key, 0, -1))
    data['threshold'] = int(r.get('threshold'))

    if (data['buy'] >= data['threshold']) or (data['sell'] >= data['threshold']):
        if(data['buy'] >= data['sell']):
            nexttrade = "BUY BUY BUY"
        else:
            nexttrade = "SELL SELL SELL"
    else:
        nexttrade = "HODL"





    fig = gen_table_timer(str(time_left)[2:7], nexttrade)
    
    return fig
    


app.run_server(debug=True)


