import os
import pickle
import random
from fuzzywuzzy import fuzz
import discord
import asyncio


async def displaycard(ctx, heading, displaymessage: dict, inline: bool):
    displaycard = discord.Embed(title=heading, color=0x667A14)

    for key in displaymessage:
        message = ""
        for i in displaymessage[key]:
            message += i

        displaycard.add_field(name=key, value=message, inline=inline)

    await ctx.send(embed=displaycard)


# List quizes given a username
async def list(ctx, username):
    messages = {
        "My Personal Quizes": [],
        "My Shared Quizes": [],
    }

    options = os.listdir(f"userfiles/{username}")

    for option in options:
        if ".pkl" not in option:
            options.remove(option)

    n = 0
    for i in options:
        i = i.replace(".pkl", "")
        messages["My Personal Quizes"].append(f"{n}: {i}\n")
        n += 1

    soptions = os.listdir(f"userfiles/{username}/shared")
    if len(soptions) > 0:
        n = 0
        for i in soptions:
            i = i.replace(".pkl", "")
            messages["My Shared Quizes"].append(f"{n}: {i}\n")
            n += 1

    await displaycard(ctx, heading="My Quizes", displaymessage=messages, inline=True)


# Select a quiz given a username
async def quizselect(ctx, username):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        await list(ctx, username=username)
        options = os.listdir(f"userfiles/{username}")
        soptions = os.listdir(f"userfiles/{username}/shared")

        validinput = False
        while validinput == False:
            try:
                await ctx.send("Choose a quiz: ")
                choice = await ctx.bot.wait_for("message", check=check, timeout=30.0)
                choice = choice.content
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond.")
                break
            else:
                try:
                    if len(str(choice)) == 1:
                        file = f"userfiles/{username}/{options[int(choice)]}"
                    if len(str(choice)) == 2:
                        file = f"userfiles/{username}/shared/{soptions[int(choice)]}"
                except IndexError:
                    await ctx.send("Not a valid option")
                else:
                    validinput = True
                    return file

    except TypeError:
        pass


# Check how close an answer is to correct
async def answercheck(ctx, Cans: str, Ians: str, perfect: str):
    if perfect == "n":
        if len(Cans) < 4:
            threshold = 100
        if len(Cans) >= 4 and len(Cans) <= 7:
            threshold = 90
        if len(Cans) >= 8 and len(Cans) <= 10:
            threshold = 85
        else:
            threshold = 80

        sim = fuzz.ratio((Cans.lower()), (Ians.lower()))
        if sim == 100:
            pc = "c"
            final = Cans
            return final, pc
        elif sim >= threshold:
            final = Cans
            pc = "nq"
            return final, pc
        else:
            final = Ians
            pc = "n"
            return final, pc


# Ask a question in a write format
async def write(ctx, file, question):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    with open(file, "rb") as f:
        Quiz_Details = pickle.load(f)

    correct = 0

    if "?" in Quiz_Details["Q"][question]:
        output = f"\n{Quiz_Details['Q'][question]}"
    else:
        output = f"\n{Quiz_Details['Q'][question]}?"

    await displaycard(
        ctx, heading="Questions:", displaymessage={output: ""}, inline=False
    )

    try:
        await ctx.send("Input answer: ")
        ans = await ctx.bot.wait_for("message", check=check, timeout=30.0)
        ans = ans.content
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")

    final, pc = await answercheck(ctx, Quiz_Details["A"][question], ans, "n")
    if final == Quiz_Details["A"][question]:
        if pc == "c":
            await displaycard(
                ctx,
                heading="Correct",
                displaymessage={"Well Done!": "score +1"},
                inline=False,
            )
            correct += 1
        if pc == "nq":
            output = f"Not quite but close enough. The correct answer is {final}."
            await displaycard(
                ctx,
                heading="Correct",
                displaymessage={output: "score +1"},
                inline=False,
            )
            correct += 1
    else:
        output = f"The Correct answer is {final}"
        await displaycard(
            ctx, heading="False!", displaymessage={output: "score +0"}, inline=False
        )

    return correct


# ask a question in a multi-choice format
async def multichoice(ctx, file, question):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    letter = ["A", "B", "C", "D"]

    with open(file, "rb") as f:
        Quiz_Details = pickle.load(f)

    correct = 0

    if "?" in Quiz_Details["Q"][question]:
        output = f"\n{Quiz_Details['Q'][question]}"
    else:
        output = f"\n{Quiz_Details['Q'][question]}?"

    correct_ans = Quiz_Details["A"][question]
    mchoices = [correct_ans]
    mchoices.extend(
        random.sample([ans for ans in Quiz_Details["A"] if ans != correct_ans], 3)
    )
    random.shuffle(mchoices)

    letters = []
    for i in range(0, 4):
        letters.append({mchoices[i]})

    await displaycard(
        ctx,
        heading="Question:",
        displaymessage={
            output: "",
            "A": letters[0],
            "B": letters[1],
            "C": letters[2],
            "D": letters[3],
        },
        inline=False,
    )

    try:
        await ctx.send("Input answer: ")
        letterans = await ctx.bot.wait_for("message", check=check, timeout=30.0)
        letterans = (letterans.content).lower()
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")

    ans = ""

    if letterans == "a":
        ans = mchoices[0]

    elif letterans == "b":
        ans = mchoices[1]

    elif letterans == "c":
        ans = mchoices[2]

    elif letterans == "d":
        ans = mchoices[3]

    else:
        ans = letterans

    final, pc = await answercheck(ctx, Quiz_Details["A"][question], ans, "n")
    if final == Quiz_Details["A"][question]:
        if pc == "c":
            await displaycard(
                ctx,
                heading="Correct",
                displaymessage={"Well Done!": "score +1"},
                inline=False,
            )
            correct += 1
        if pc == "nq":
            output = f"Not quite but close enough. The correct answer is {final}."
            await displaycard(
                ctx,
                heading="Correct",
                displaymessage={output: "score +1"},
                inline=False,
            )
            correct += 1
    else:
        output = f"The Correct answer is {final}"
        await displaycard(
            ctx, heading="False!", displaymessage={output: "score +0"}, inline=False
        )

    return correct


async def learn(ctx, qn: int, rangein: int, rangeout: int, file: str):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    # Initialze vars
    asking = True
    totalscore = rangeout - (rangein - 1)
    mc = {}
    w = {}

    # Add question indexs
    for add in range(rangein - 1, rangeout):
        mc[add] = 0

    # Ask a segment of questions
    while asking == True:
        # Check for value of multichoice and if so switch it to write
        remove = []
        for key, value in mc.items():
            if value >= 2:
                remove.append(key)
                w[key] = 0
        for key in remove:
            del mc[key]

        # Combine dicts into one for asking questions
        combined_dict = {}
        for key in mc.keys():
            combined_dict[key] = 0
        for key in w.keys():
            combined_dict[key] = 1

        # Ask multichoice and write questions in order
        for key in range(rangein - 1, rangeout):
            if combined_dict.get(key) == 0:
                correct = 0
                correct = await multichoice(ctx, file=file, question=key)
                if correct > 0:
                    mc[key] += 1
            else:
                correct = 0
                correct = await write(ctx, file=file, question=key)
                if correct > 0:
                    w[key] += 1

        try:
            await ctx.send("Type anything to continue: ")
            dump = await ctx.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")

        # Check whether loop is finished
        total = 0
        for value in w.values():
            total += value
        if total >= totalscore:
            asking = False
            try:
                await ctx.send("Type anything to continue: ")
                dump = await ctx.bot.wait_for("message", check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond.")
