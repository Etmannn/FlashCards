import pickle
from discord.ext import commands
from cogs.common_functions import quizselect
import asyncio


class Editquiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def editquiz(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        # Intialize vars
        editing = True

        username = ctx.author

        # Select Quiz
        file = await quizselect(ctx, username=username)

        # Open file
        with open(file, "rb") as f:
            Quiz_Details = pickle.load(f)

        while editing:
            # Get amout of questions
            qn = len(Quiz_Details["Q"])

            try:
                await ctx.send("Edit(1), Add(2), Remove(3): ")
                option = await self.bot.wait_for("message", check=check, timeout=30.0)
                option = int(option.content)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond.")

            for i in range(qn):
                await ctx.send(
                    f"{i}.) {Quiz_Details['Q'][i]} -> {Quiz_Details['A'][i]}"
                )

            if option == 1:
                try:
                    await ctx.send("Select Question to edit: ")
                    choice1 = await self.bot.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    choice1 = int(choice1.content)
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond.")

                await ctx.send(
                    f"{Quiz_Details['Q'][choice1]} -> {Quiz_Details['A'][choice1]}"
                )

                try:
                    await ctx.send("Choose what to edit: Question(1) or Answer(2): ")
                    choice2 = await self.bot.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    choice2 = int(choice2.content)
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond.")

                if choice2 == 1:
                    choice2 = "Q"
                else:
                    choice2 = "A"

                await ctx.send(f"Original: {Quiz_Details[choice2][choice1]}")

                try:
                    await ctx.send("Input New Question/Answer: ")
                    new = await self.bot.wait_for("message", check=check, timeout=30.0)
                    new = new.content
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond.")

                Quiz_Details[choice2][choice1] = new
                await ctx.send(
                    f"{Quiz_Details['Q'][choice1]} -> {Quiz_Details['A'][choice1]}"
                )

            if option == 2:
                try:
                    await ctx.send("Input Question: ")
                    new = await self.bot.wait_for("message", check=check, timeout=30.0)
                    new = new.content
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond.")
                try:
                    await ctx.send("Input Answer: ")
                    new2 = await self.bot.wait_for("message", check=check, timeout=30.0)
                    new2 = new2.content
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond.")

                Quiz_Details["Q"].append(new)
                Quiz_Details["A"].append(new2)
                await ctx.send(f"{Quiz_Details['Q'][qn]} -> {Quiz_Details['A'][qn]}")

            if option == 3:
                try:
                    await ctx.send("Select Question to remove: ")
                    choice1 = await self.bot.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    choice1 = int(choice1.content)
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond.")

                del Quiz_Details["Q"][choice1]
                del Quiz_Details["A"][choice1]

            try:
                await ctx.send("Would you like to edit anything else(y/n): ")
                loop = await self.bot.wait_for("message", check=check, timeout=30.0)
                loop = loop.content
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond.")

            if loop == "n":
                editing = False

        with open(file, "wb") as f:
            pickle.dump(Quiz_Details, f)


async def setup(bot):
    await bot.add_cog(Editquiz(bot))
