# In progress

from fuzzywuzzy import fuzz
import pickle
import os
import random


# List quizes given a username
def list(username):
    options = os.listdir(f"userfiles\\{username}")
    for option in options:
        if ".pkl" not in option:
            options.remove(option)
    n = 0
    print("My Quizes:\n---------------")
    for i in options:
        i = i.replace(".pkl", "")
        print(f"{i}({n})")
        n += 1
    print("---------------\n")

    soptions = os.listdir(f"userfiles\\{username}\\shared")
    if len(soptions) > 0:
        n = 0
        print("Shared Quizes:\n---------------")
        for i in soptions:
            i = i.replace(".pkl", "")
            print(f"{i}(0{n})")
            n += 1
        print("---------------")


# Select a quiz given a username
def quizselect(username):
    list(username=username)
    options = os.listdir(f"userfiles\\{username}")
    soptions = os.listdir(f"userfiles\\{username}\\shared")

    validinput = False
    while validinput == False:
        try:
            choice = str(input("Choose a quiz: "))
        except ValueError:
            print("Choose with a number(displayed in parenthesis at the end)")
        else:
            try:
                if len(str(choice)) == 1:
                    file = f"userfiles\\{username}\\{options[int(choice)]}"
                if len(str(choice)) == 2:
                    file = f"userfiles\\{username}\\shared\\{soptions[int(choice)]}"
            except IndexError:
                print("Not a valid option")
            else:
                validinput = True

    return file


# Check how close an answer is to correct
def answercheck(Cans: str, Ians: str, perfect: str):
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
def write(file, question):
    with open(file, "rb") as f:
        Quiz_Details = pickle.load(f)

    correct = 0

    if "?" in Quiz_Details["Q"][question]:
        output = f"\n{Quiz_Details['Q'][question]}"
    else:
        output = f"\n{Quiz_Details['Q'][question]}?"

    print(output)

    ans = input("Input answer: ").lower()
    final, pc = answercheck(Quiz_Details["A"][question], ans, "n")
    if final == Quiz_Details["A"][question]:
        if pc == "c":
            print("Correct!")
            correct += 1
        if pc == "nq":
            print(f"Not quite but close enough. The correct answer is {final}.")
            correct += 1
    else:
        print("False")

    return correct


# ask a question in a multi-choice format
def mutlichoice(file, question):
    letter = ["A", "B", "C", "D"]

    with open(file, "rb") as f:
        Quiz_Details = pickle.load(f)

    correct = 0

    if "?" in Quiz_Details["Q"][question]:
        output = f"\n{Quiz_Details['Q'][question]}"
    else:
        output = f"\n{Quiz_Details['Q'][question]}?"

    print(output)

    correct_ans = Quiz_Details["A"][question]
    mchoices = [correct_ans]
    mchoices.extend(
        random.sample([ans for ans in Quiz_Details["A"] if ans != correct_ans], 3)
    )
    random.shuffle(mchoices)

    for i in range(0, 4):
        print(f"{letter[i]}) {mchoices[i]}")

    letterans = input("Input answer: ").lower()
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

    final, pc = answercheck(Quiz_Details["A"][question], ans, "n")
    if final == Quiz_Details["A"][question]:
        if pc == "c":
            print("Correct!")
            correct += 1
        if pc == "nq":
            print(f"Not quite but close enough. The correct answer is {final}.")
            correct += 1
    else:
        print("False")

    return correct
