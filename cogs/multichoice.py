import pickle
from discord.ext import commands
from cogs.common_functions import quizselect, mutlichoice
import asyncio


class Multichoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command
    async def multichoice(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            await ctx.send("Input username: ")
            username = await self.bot.wait_for("message", check=check, timeout=30.0)
            username = username.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

        file = await quizselect(ctx, username=username)

        with open(file, "rb") as f:
            Quiz_Details = pickle.load(f)
        qn = int(len(Quiz_Details["Q"]))

        if qn < 4:
            print("You need a minimum of 4 questions to use multichoice")
        else:
            correctans = 0
            for i in range(qn):
                correct = await mutlichoice(ctx, file=file, question=i)
                correctans += correct

            print(f"You got {correctans} out of {qn}")


async def setup(bot):
    await bot.add_cog(Multichoice(bot))
