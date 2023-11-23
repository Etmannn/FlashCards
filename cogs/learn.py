import pickle
from discord.ext import commands
from cogs.common_functions import quizselect, learn
import asyncio


class Learn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def learn(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        # Intialize vars
        rangein = 0
        rangeout = 0
        rangeinlist = [1]
        rangeoutlist = []

        username = ctx.author

        file = await quizselect(ctx, username=username)

        with open(file, "rb") as f:
            Quiz_Details = pickle.load(f)

        # Get how many questions there are
        qn = int(len(Quiz_Details["Q"]))

        if qn >= 4 and qn <= 14:
            seg = 4
        elif qn >= 15 and qn <= 20:
            seg = 5
        elif qn >= 21 and qn <= 24:
            seg = 6
        elif qn >= 25 and qn <= 28:
            seg = 7
        elif qn >= 29 and qn <= 32:
            seg = 8
        elif qn >= 33 and qn <= 36:
            seg = 9
        else:
            seg = 10

        group = qn // seg
        ones = qn % seg

        if qn < 4:
            await ctx.send("You need a minimum of 4 questions to use learn.")
        else:
            if group == 0:
                rangein = 1
                rangeout = ones
                await learn(ctx, qn=qn, rangein=rangein, rangeout=rangeout, file=file)

            else:
                for tens in range(group):
                    rangeoutlist.append(tens * seg + seg)
                rangeoutlist.append(rangeoutlist[-1] + ones)

                for append in rangeoutlist:
                    rangeinlist.append(append + 1)

                for rangein, rangeout in zip(rangeinlist, rangeoutlist, strict=False):
                    await learn(
                        ctx, qn=qn, rangein=rangein, rangeout=rangeout, file=file
                    )


async def setup(bot):
    await bot.add_cog(Learn(bot))
