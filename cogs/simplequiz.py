import pickle
from discord.ext import commands
from cogs.common_functions import quizselect, write
import asyncio


class Write(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def write(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        username = ctx.author

        file = await quizselect(ctx, username=username)

        with open(file, "rb") as f:
            Quiz_Details = pickle.load(f)
        qn = int(len(Quiz_Details["Q"]))

        correctans = 0
        for i in range(qn):
            correct = await write(ctx, file=file, question=i)
            correctans += correct

        await ctx.send(f"You got {correctans} out of {qn}")


async def setup(bot):
    await bot.add_cog(Write(bot))
