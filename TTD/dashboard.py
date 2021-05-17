import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output, State
import plotly.express as px
import random
import pandas as pd
import dash_daq as daq
import redis
import dash_bootstrap_components as dbc
import dash_html_components as html
import datetime as dt
import plotly.graph_objects as go
from playsound import playsound
import simpleaudio as sa


from modules.dashboard_figures import *
from modules.vote_logic import *


#initialise the program
r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
r.delete('trigger-time')
r.set("popup", "closed")
reset(r)
set_price(r)
set_bal(r)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(children=[
    html.Div(
    
    dbc.Row([
        
            dbc.Col(gif.GifPlayer(
                gif='assets/spinnysmall.gif',
                still='assets/doge.png',
                autoplay=True
            ), width="auto"),
        dbc.Col(html.H3(children="Twitch Trades DOGE")),

            dbc.Col(gif.GifPlayer(
                gif='assets/spinnysmall.gif',
                still='assets/doge.png',
                autoplay=True
            ), width="auto"),
        


    ]
    ),
    style={'height':'100px' }),
    
    
    
    dcc.Graph(id="table"),
    dcc.Graph(id="timertable"),
    dcc.Graph(id="lasttrade-table"),
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="voter-table"),

    
    
    dbc.Modal(
        [
            dbc.ModalBody([ gif.GifPlayer(
                gif='assets/spinnysmall.gif',
                still='assets/doge.png',
                autoplay=True
            ),
            r.get("thistrade"),
             gif.GifPlayer(
                gif='assets/spinnysmall.gif',
                still='assets/doge.png',
                autoplay=True
            )]
            ),
            
        ],
        id="modal-centered",
        centered=True,
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



@app.callback(
    Output("modal-centered", "is_open"),
    Input("interval-short", "n_intervals"),
    [State("modal-centered", "is_open")],)
def toggle_modal(is_open, n_intervals):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    popup = r.get("popup")
    if popup == "open":
        print("POPUP OPEN")
        
        return is_open
    return not is_open





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
    Output("voter-table", "figure"), 
    [Input("interval-long", "n_intervals")])
def update_table(day):
    set_price(r)
    fig = gen_table_voter()
    return fig
  
@app.callback(
    Output("lasttrade-table", "figure"), 
    [Input("interval-long", "n_intervals")])
def update_table(day):
    fig = gen_table_lasttrade()
    return fig

   
@app.callback(
    Output("timertable", "figure"), 
    [Input("interval-short", "n_intervals")])
def update_clock(value):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)

    #SET THE TIMER LENGTH
    clock = 15


    #reset the clock, if old
    if  (r.get('trigger-time') == None):
        
        set_price(r)
        set_bal(r)
        reset(r)

        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=clock)))
        print(f"trigger has been reset to {r.get('trigger-time')}")

    if (dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f') <= dt.datetime.now()):
        #perform trade
        set_price(r)
        trade(r)
        set_bal(r)
        
        reset(r)
        
        #reset clock after trade
        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=clock)))
        print(f"trigger has been reset to {r.get('trigger-time')}")


    #close popup
    if ((dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f') < dt.datetime.now() + dt.timedelta(seconds=clock-5))   ):
        r.set("popup", "closed")
        print("closing")




    trigger = dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f')
    #get current clock time
    time_left = trigger - dt.datetime.now()

    data = {}

    for key in ["buy","sell","votes","hold"]:
        data[key] = len(r.lrange(key, 0, -1))
    data['threshold'] = int(r.get('threshold'))

    get_nexttrade(r)
    




    fig = gen_table_timer(str(time_left)[2:7], r.get("nexttrade"))
    
    return fig
    


app.run_server(debug=True)


