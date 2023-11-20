import pickle
from discord.ext import commands
from cogs.common_functions import quizselect
import asyncio


class Listquiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listquizes(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            await ctx.send("Input Username: ")
            username = await self.bot.wait_for("message", check=check, timeout=30.0)
            username = username.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
        file = await quizselect(ctx, username=username)

        with open(file, "rb") as f:
            Quiz_Details = pickle.load(f)

        qn = int(len(Quiz_Details["Q"]))

        await ctx.send("\n_______________")
        for question in range(0, qn):
            await ctx.send(
                f"{Quiz_Details['Q'][question]}: {Quiz_Details['A'][question]}"
            )
        await ctx.send("_______________")


async def setup(bot):
    await bot.add_cog(Listquiz(bot))
