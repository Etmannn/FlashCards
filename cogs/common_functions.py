import os
import pickle
import random
from fuzzywuzzy import fuzz
import discord
import asyncio


# List quizes given a username
async def list(ctx, username):
    options = os.listdir(f"userfiles/{username}")
    for option in options:
        if ".pkl" not in option:
            options.remove(option)
    n = 0
    await ctx.send("My Quizes:\n---------------")
    for i in options:
        i = i.replace(".pkl", "")
        await ctx.send(f"{i}({n})")
        n += 1
    await ctx.send("---------------\n")

    soptions = os.listdir(f"userfiles/{username}/shared")
    if len(soptions) > 0:
        n = 0
        await ctx.send("Shared Quizes:\n---------------")
        for i in soptions:
            i = i.replace(".pkl", "")
            await ctx.send(f"{i}(0{n})")
            n += 1
        await ctx.send("---------------")


# Select a quiz given a username
async def quizselect(ctx, username):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

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
            print("You took too long to respond.")
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

        sim = fuzz.ratio(Cans, Ians)
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

    await ctx.send(output)

    ans = input("Input answer: ").lower()
    try:
        await  ctx.send("Input answer: ")
        ans = ctx.bot.wait_for('message', check = check, timeout = 30.0)
        ans = ans.content
    except asyncio.TimeoutError:
        print("You took too long to respond.")
    
    final, pc = answercheck(ctx, Quiz_Details["A"][question], ans, "n")
    if final == Quiz_Details["A"][question]:
        if pc == "c":
            await ctx.send("Correct!")
            correct += 1
        if pc == "nq":
            await ctx.send(
                f"Not quite but close enough. The correct answer is {final}."
            )
            correct += 1
    else:
        await ctx.send("False")

    return correct


# ask a question in a multi-choice format
async def mutlichoice(ctx, file, question):
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

    await ctx.send(output)

    correct_ans = Quiz_Details["A"][question]
    mchoices = [correct_ans]
    mchoices.extend(
        random.sample([ans for ans in Quiz_Details["A"] if ans != correct_ans], 3)
    )
    random.shuffle(mchoices)

    for i in range(0, 4):
        await ctx.send(f"{letter[i]}) {mchoices[i]}")
        
    try:
        await ctx.send("Input answer: ")
        letterans = ctx.bot.wait_for('message', check = check, timeout=30.0)
        letterans = letterans.content
    except asyncio.TimeoutError:
        print('You took too long to respond.')
    
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

    final, pc = answercheck(ctx, Quiz_Details["A"][question], ans, "n")
    if final == Quiz_Details["A"][question]:
        if pc == "c":
            await ctx.send("Correct!")
            correct += 1
        if pc == "nq":
            await ctx.send(
                f"Not quite but close enough. The correct answer is {final}."
            )
            correct += 1
    else:
        await ctx.send("False")

    return correct
