import os
from discord.ext import commands
from cogs.common_functions import quizselect
import asyncio


class Deletequiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deletequiz(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        # Delete
        try:
            await ctx.send("Input username: ")
            username = await self.bot.wait_for("message", check=check, timeout="30.0")
            username = username.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

        # Grab username

        # Select Quiz
        file = await quizselect(ctx, username=username)

        # Delete file
        os.remove(file)


async def setup(bot):
    await bot.add_cog(Deletequiz(bot))
