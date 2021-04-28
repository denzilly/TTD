
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
import pandas as pd
import dash_daq as daq
import redis

import datetime as dt


r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
r.delete('trigger-time')
print('got here')
print(r.get('trigger-time'))






app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="bar-chart"),
    daq.LEDDisplay(
        id='clock',
        label="Default",
        value='5:00'
    ),
    dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
])




@app.callback(
    Output("bar-chart", "figure"), 
    [Input("interval-component", "n_intervals")])
def update_bar_chart(day):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    data = [["buy", len(r.lrange("buy",0,-1))], ["sell", len(r.lrange("sell",0,-1))]]
    df = pd.DataFrame(data, columns=['Action', 'Count'])
    


    fig = px.bar(df, x="Action", y="Count")
    fig.update_layout(yaxis_range=[0,24])
    return fig

@app.callback(
    Output("clock", "value"), 
    [Input("interval-component", "n_intervals")])
def update_clock(value):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)

    #reset the clock, if old
    if  (r.get('trigger-time') == None):
        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=30)))
        print(f"trigger has been reset to {r.get('trigger-time')}")
        for x in ["buy","vote","sell"]:
            r.delete(x)

    if (dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f') <= dt.datetime.now()):
        r.set('trigger-time', str(dt.datetime.now() + dt.timedelta(seconds=30)))
        print(f"trigger has been reset to {r.get('trigger-time')}")
        for x in ["buy","vote","sell"]:
            r.delete(x)


    trigger = dt.datetime.strptime(r.get('trigger-time'),  '%Y-%m-%d %H:%M:%S.%f')
    #get current clock time
    
    time_left = trigger - dt.datetime.now()
    
    return str(time_left)[2:7]
    


app.run_server(debug=True)


