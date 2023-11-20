import discord
from discord.ext import commands
import os
from cogs import common_functions
import secretvars

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="q!", intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Bot successfully logged in")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="q!help")
    )
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py") and cog != "common_functions.py":
            await bot.load_extension(f"cogs.{cog[:-3]}")


@bot.command()
async def help(ctx):
    await ctx.send("can't help yet")


bot.run(secretvars.token)
