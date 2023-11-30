import pickle
from discord.ext import commands
from cogs.common_functions import quizselect, displaycard
import asyncio


class Listquiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listquizes(self, ctx):
        messages = {"Question": [], "Answer": []}

        username = ctx.author

        file = await quizselect(ctx, username=username)

        with open(file, "rb") as f:
            Quiz_Details = pickle.load(f)

        qn = int(len(Quiz_Details["Q"]))

        for question in range(qn):
            messages["Question"].append(f'{Quiz_Details["Q"][question]}\n')
            messages["Answer"].append(f'{Quiz_Details["A"][question]}\n')

        name = file.split("/")[-1]
        name = name[:-4]
        await displaycard(ctx, heading=name, displaymessage=messages, inline=True)


async def setup(bot):
    await bot.add_cog(Listquiz(bot))
