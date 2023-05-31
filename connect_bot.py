import discord
from discord import app_commands
import asyncio
from discord.ext import commands
from discord import permissions,channel,guild,utils
import os

import bot_token

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

_token = bot_token.TOKEN

@bot.event
async def on_ready():
    print("Logged in as {0.user}.".format(bot))

    # try:
    #     synced = await bot.tree.sync()
    #     print(f"Synced commands {synced}")
    # except Exception as e:
    #     print(e)
    await bot.change_presence(activity=discord.Game(name=":)"))

# @bot.command()
# async def test(ctx):
#     user = str(ctx.author)
#     await ctx.send(f"Hemlo {user}")

@bot.command()
async def info(ctx,user:discord.Member):
    await ctx.send(f'{user.name}\'s id: `{user.id}`')

# @bot.tree.command()
# async def hello(ctx):
#     await ctx.response.send_message("hi") #emphemeral=true for whoever actucally saw only sees it
#
#
# @bot.tree.command(name="test")
# @app_commands.describe(name_arg = "description")
# async def test(ctx , name_arg : str):
#     usr = ctx.user.name
#     await ctx.response.send_message(f"{usr} and {name_arg}")
#


async def main():

    cogList=["Moderation","Csgo","Valo","Votebot", "mod", "ping","Music"]

    for myCog in cogList:
        await bot.load_extension('cogs.'+myCog)
    await bot.start(_token)

asyncio.run(main())