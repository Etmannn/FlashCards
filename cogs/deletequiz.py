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

        username = ctx.author

        # Select Quiz
        file = await quizselect(ctx, username=username)

        # Delete file
        os.remove(file)


async def setup(bot):
    await bot.add_cog(Deletequiz(bot))
