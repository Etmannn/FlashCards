import pickle
import os
from discord.ext import commands
import asyncio


class Createfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def createquiz(self, ctx):
        # initialize vars
        Quiz_Details = {"Q": [], "A": []}
        inputing = True
        num = 0

        # Get user inputs
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        # Delete
        try:
            await ctx.send("Input Username: ")
            username = await self.bot.wait_for("message", check=check, timeout=30.0)
            username = username.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
        # Grab username 

        try:
            await ctx.send("Input quiz name: ")
            quizname = await self.bot.wait_for("message", check=check, timeout=30.0)
            quizname = quizname.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

        # Format file name
        quizname = quizname.replace(" ", "_")

        # Set file location
        file = str(f"userfiles/{username}/{quizname}.pkl")

        # Input questions and answers
        while inputing == True:
            num += 1

            try:
                await ctx.send(f"Input Question number {num} or type 'done': ")
                Qu = await self.bot.wait_for("message", check=check, timeout=30.0)
                Qu = Qu.content
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond.")

            if Qu == "done":
                inputing = False
            else:
                try:
                    await ctx.send(f"Input Answer for Question number {num}: ")
                    An = await self.bot.wait_for("message", check=check, timeout=30.0)
                    An = An.content
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond.")

                Quiz_Details["Q"].append(Qu)
                Quiz_Details["A"].append(An)

        # Find or create folder
        if os.path.isdir(f"userfiles/{username}"):
            pass
        else:
            os.mkdir(f"userfiles/{username}")
            os.mkdir(f"userfiles/{username}/shared")

        # Dump dictionary into pickle file
        with open(file, "wb") as f:
            pickle.dump(Quiz_Details, f)


async def setup(bot):
    await bot.add_cog(Createfile(bot))
