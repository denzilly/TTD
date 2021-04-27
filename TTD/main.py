import os
from twitchio.ext import commands

from trader import buy, sell, check_bal
from helpers import vote_cache


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
import pandas as pd



bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)


@bot.event
async def event_ready():
        'called on wakeup'
        print(f"{os.environ['BOT_NICK']} is online!")
        ws = bot._ws
        
        await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")



@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return
    await bot.handle_commands(ctx)


@bot.command(name='buy')
async def test(ctx):
    buy(check_bal())
    await ctx.send('BUY')

@bot.command(name='hold')
async def test(ctx):

    await ctx.send('HOLD')

@bot.command(name='sell')
async def test(ctx):
    sell(check_bal())
    await ctx.send('SELL')




async def run_dash():
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































# bot.py
if __name__ == "__main__":
    bot.run()
    #app.run_server(debug=True)
