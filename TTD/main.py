import os
from twitchio.ext import commands


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


@bot.command(name='test')
async def test(ctx):
    await ctx.send('test PASSED!')








# bot.py
if __name__ == "__main__":
    bot.run()
