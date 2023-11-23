import os
import shutil
import pickle
from discord.ext import commands
from cogs.common_functions import quizselect
import asyncio


class Sharequiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command
    async def sharequiz(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        username = ctx.author

        file = await quizselect(ctx, username=username)

        with open(file, "rb") as f:
            Quiz_Details = pickle.load(f)

        try:
            await ctx.send("Input name of user to share to: ")
            shareto = await self.bot.wait_for("message", check=check, timeout=30.0)
            shareto = shareto.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

        sharefile = f"userfiles/{shareto}/shared"

        if shareto in os.listdir("userfiles"):
            shutil.copy(file, sharefile)

        else:
            await ctx.send("That user is not registered")


async def setup(bot):
    await bot.add_cog(Sharequiz(bot))
