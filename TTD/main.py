import os
from twitchio.ext import commands

#from trader import buy, sell, check_bal
from helpers import vote_cache


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
import pandas as pd
import redis



r = redis.Redis('localhost', charset="utf-8", decode_responses=True)

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
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
    #buy(check_bal())
    
    r.rpush('buy', ctx.author.name.lower())
    r.rpush('votes', ctx.author.name.lower())
    print("BUY!")
    await ctx.send('BUY')

@bot.command(name='hold')
async def test(ctx):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    r.rpush('hold', ctx.author.name.lower())
    r.rpush('votes', ctx.author.name.lower())
    print("HOLD")
    await ctx.send('HOLD')

@bot.command(name='sell')
async def test(ctx):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    #sell(check_bal())
    r.rpush('sell', ctx.author.name.lower())
    r.rpush('votes', ctx.author.name.lower())
    print("SELL")
    await ctx.send('SELL')









# bot.py
if __name__ == "__main__":
    bot.run()
    
