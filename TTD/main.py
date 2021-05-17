import os
from twitchio.ext import commands

#from trader import buy, sell, check_bal



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
import pandas as pd
import redis
import asyncio



r = redis.Redis('localhost', charset="utf-8", decode_responses=True)



bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
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
        bot.loop.create_task(get_stream_info())
        await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")



async def get_stream_info():
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    while 1:    
        stream_info = await bot.get_stream("twitchtradesdoge")
        r.set("viewer_count",stream_info['viewer_count'])
        print(f'current viewers: {stream_info["viewer_count"]}')
        await asyncio.sleep(10)


# @bot.event
# async def event_message(ctx):
#     'Runs every time a message is sent in chat.'

#     # make sure the bot ignores itself and the streamer
#     if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
#         return
#     await bot.handle_commands(ctx)


@bot.command(name='buy')
async def test(ctx):
    #buy(check_bal())
    if r.get("position") != "long":
        r.rpush('buy', ctx.author.name.lower())
        r.rpush('votes', ctx.author.name.lower())
        r.set("recent_voter",ctx.author.name.lower()+" buy")
        print("BUY!")
        await ctx.send('BUY')

    else:
        print("Cannot buy, below minimum USDT Balance")
        await ctx.send("Cannot buy, below minimum USDT Balance")


@bot.command(name='buy12')
async def test(ctx):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    #sell(check_bal())
    if r.get("position") != "long":
        for x in range(12):
            r.rpush('buy', ctx.author.name.lower())
            r.rpush('votes', ctx.author.name.lower())
        print("BUY")
        r.set("recent_voter",ctx.author.name.lower()+" buy")
        await ctx.send('BUY')
    else:
        print("Cannot buy, below minimum USDT Balance")
        await ctx.send("Cannot buy, below minimum USDT Balance")






@bot.command(name='hold')
async def test(ctx):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    r.rpush('hold', ctx.author.name.lower())
    r.set("recent_voter",ctx.author.name.lower())
    r.rpush('votes', ctx.author.name.lower()+" hold")
    print("HOLD")
    await ctx.send('HOLD')


@bot.command(name='hold12')
async def test(ctx):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    #sell(check_bal())
    for x in range(12):
        r.rpush('hold', ctx.author.name.lower())
        r.rpush('votes', ctx.author.name.lower())
    r.set("recent_voter",ctx.author.name.lower()+" hold")
    print("HOLD")
    await ctx.send('HOLD')





@bot.command(name='sell')
async def test(ctx):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    #sell(check_bal())
    if r.get("position") != "short":
        r.rpush('sell', ctx.author.name.lower())
        r.rpush('votes', ctx.author.name.lower())
        r.set("recent_voter",ctx.author.name.lower()+" sell")
        print("SELL")
        await ctx.send('SELL')

    else:
        print("Cannot sell, below minimum DOGE Balance")
        await ctx.send("Cannot sell, below minimum DOGE Balance")


@bot.command(name='sell12')
async def test(ctx):
    r = redis.Redis('localhost', charset="utf-8", decode_responses=True)
    #sell(check_bal())
    if r.get("position") != "short":
        for x in range(12):
            r.rpush('sell', ctx.author.name.lower())
        print("SELL")
        r.set("recent_voter",ctx.author.name.lower()+" sell")
        await ctx.send('SELL')
    else:
        print("Cannot sell, below minimum DOGE Balance")
        await ctx.send("Cannot sell, below minimum DOGE Balance")
    #r.rpush('votes', ctx.author.name.lower())
    






# bot.py
if __name__ == "__main__":
    bot.run()
    
