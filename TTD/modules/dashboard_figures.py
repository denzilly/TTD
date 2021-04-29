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
import plotly.graph_objects as go




#GENERATES ALL CHARTS AND DASH ELEMENTS FOR TTD



def gen_table():

    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    fig = go.Figure(data=[go.Table(
    header=dict(values=['<b>TOTAL GAINZ</b>', f'<b>{r.get("tpnl")}</b>'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[[ "<b>Position</b>", "<b>Doge Balance</b>", "<b>USDT Balance</b>"], # 1st column
                       [ r.get("position"), r.get("dogebal"), r.get("usdtbal")]], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
        ])

    return fig



def gen_barchart():
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    data = [["buy", len(r.lrange("buy",0,-1))], ["sell", len(r.lrange("sell",0,-1))]]
    df = pd.DataFrame(data, columns=['Action', 'Count'])
    fig = px.bar(df, x="Action", y="Count")
    fig.update_layout(yaxis_range=[0,24])

    return fig