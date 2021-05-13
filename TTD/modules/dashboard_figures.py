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



def gen_table_top():

    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    fig = go.Figure(data=[go.Table(
    header=dict(values=['<b>TOTAL GAINZ</b>', f'<b>{r.get("tpnl")}</b>'],
                line_color='#d2ff2f',
                fill_color='#4f4f4a',
                align='left',
                font_color='#d2ff2f'),
    cells=dict(values=[[ "<b>Doge Balance</b>", "<b>USDT Balance</b>"], # 1st column
                       [ r.get("dogebal"), r.get("usdtbal")]], # 2nd column
               line_color='#d2ff2f',
               fill_color='#4f4f4a',
                font_color='#d2ff2f',
               align='left'))
        ])

    fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=0),
        paper_bgcolor="#292927",

        height=150
    )

    return fig

def gen_table_timer(clock,nexttrade):

    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    fig = go.Figure(data=[go.Table(
    header=dict(values=[f"<b> {clock} </b>"],
                line_color='#d2ff2f',
                fill_color='#4f4f4a',
                align='center',
                font_color='red',
                font_size=26),

    cells=dict(values=[ f"Next trade: {nexttrade}" ],                    
               line_color='#d2ff2f',
               fill_color='#4f4f4a',
               align='center',
                font_color='#d2ff2f',
               font_size=20,
               height=30))
        ])

    fig.update_layout(
        margin=dict(l=10, r=10, t=0, b=0),
        paper_bgcolor="#292927",
        height=100
        )

    return fig    



def gen_barchart():
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    position = r.get("position")
    data = [["buy", len(r.lrange("buy",0,-1))], ["sell", len(r.lrange("sell",0,-1))]]
    df = pd.DataFrame(data, columns=['Action', 'Count'])
    fig = px.bar(df, x="Action", y="Count")

    fig.add_shape(type="line",
    xref="paper", yref="paper",
    x0=0, y0=10,
    x1=1, y1=10,
    line=dict(
        color="red",
        width=3,
    ),
             )

    fig.update_layout(yaxis_range=[0,24],
    margin=dict(l=10, r=20, t=5, b=0),
    paper_bgcolor='#292927',
    plot_bgcolor='#4f4f4a',
    font_color='#d2ff2f',
    height=350

    
    )

    return fig