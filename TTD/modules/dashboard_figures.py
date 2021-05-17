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

    #pnl calc
    total_u = float(r.get("usdtbal")) +  ( float(r.get("dogebal")) * float(r.get("price")))
    pnl_u = round(total_u - 100,2)
    pnl_perc = round(  (total_u - 100) / 100, 4  )

    if pnl_u > 0:
        fontcol = '#99ff5e'
        sym="+"
    else:
        fontcol = 'red'
        sym="-"




    fig = go.Figure(data=[go.Table(
    header=dict(values=['<b>TOTAL GAINZ</b>', f'<b>{round(pnl_perc*100,2)}%</b>'],
                line_color='#d2ff2f',
                fill_color='#4f4f4a',
                align='left',
                font_color=fontcol),
    cells=dict(values=[[ "<b>Doge Balance</b>", "<b>USDT Balance</b>"], # 1st column
                       [ round(float(r.get("dogebal")),2), round(float(r.get("usdtbal")),2)]], # 2nd column
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
               fill_color='#d2ff2f',
               align='center',
                font_color='#4f4f4a',
               font_size=20,
               height=30))
        ])

    fig.update_layout(
        margin=dict(l=10, r=10, t=0, b=0),
        paper_bgcolor="#292927",
        height=80
        )

    return fig    

def gen_table_voter():
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)

    if len(r.lrange("votes", 0, -1)) == 0:
        output = "No votes yet!"
    else:
        output = f"{r.get('recent_voter').split(' ')[0]} votes <b>{r.get('recent_voter').split(' ')[1]}</b>!"

    fig = go.Figure(data=[go.Table(
        header=dict(values=[ output ],                    
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

def gen_table_lasttrade():
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    lasttrade = r.get("lasttrade")

    if lasttrade is None:
        output = "No trades yet."
    else:
        output = f"Last trade: {lasttrade}"

    fig = go.Figure(data=[go.Table(
        header=dict(values=[ output ],                    
               line_color='#d2ff2f',
               fill_color='#4f4f4a',
               align='center',
              font_color='#d2ff2f',
               font_size=16,
               ))
        ])

    fig.update_layout(
        margin=dict(l=10, r=10, t=0, b=0),
        paper_bgcolor="#292927",
        height=50
        )

    return fig






def get_side_color(direction):
    if direction == "buy":
        direction =  "<mark class='red'>buy</mark>"
    elif direction == "sell":
        direction =  "<span style='color:#fadf57'>sell</span>"
    elif direction == "hold":
        direction =  "<span style='color:#b32a20'>hold</span>"
    
    return direction



def gen_barchart():
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    position = r.get("position")



    if position == "long":
        data = [["!hold", len(r.lrange("hold",0,-1))], ["!sell", len(r.lrange("sell",0,-1))]]
    elif position == "short":
        data = [["!buy", len(r.lrange("buy",0,-1))],["!hold", len(r.lrange("hold",0,-1))]]
    elif position == "neutral":
        data = [["!buy", len(r.lrange("buy",0,-1))],["!hold", len(r.lrange("hold",0,-1))], ["!sell", len(r.lrange("sell",0,-1))]]
    
    
    df = pd.DataFrame(data, columns=['Action', 'Count'])
    fig = px.bar(df, x="Action", y="Count",text=df['Count'], color="Action", color_discrete_sequence=["#367038","#fadf57","#b32a20"])

    fig.add_hline(y=10, line_width=2.5, line_color="red")

    fig.add_annotation(text=f"Minimum votes:{r.get('threshold')}", bordercolor='#d2ff2f', bgcolor='#4f4f4a',borderwidth=1.5,
     x=0.98, xref='paper',xanchor='right', y=0.97, yref='paper',yanchor='top',showarrow=False)

    fig.update_layout(
    margin=dict(l=10, r=20, t=5, b=0),
    paper_bgcolor='#292927',
    plot_bgcolor='#4f4f4a',
    font_color='#d2ff2f',
    height=350,
    showlegend=False,
    )


    fig.update_xaxes(tickfont=dict(family='lucida console', size=25), title_font_size=1, title_font_color='#4f4f4a')



    #dynamic axis ranges
    if max([len(r.lrange("hold",0,-1)), len(r.lrange("sell",0,-1)), len(r.lrange("buy",0,-1))]) < float(r.get('threshold') ) *2.5 :
        fig.update_layout(yaxis_range=[0,(float(r.get('threshold')) * 2.5)])





    return fig