import pickle
import functions

# Intialize vars
editing = True

# Select username
username = input("Input Username: ")

# Select Quiz
file = functions.quizselect(username=username)

# Open file
with open(file, "rb") as f:
    Quiz_Details = pickle.load(f)

# Find how many questions there are
qn = int(len(Quiz_Details["Q"]))

# print questions
print("\n_______________")
for question in range(0, qn):
    print(f"\n{Quiz_Details['Q'][question]}: {Quiz_Details['A'][question]}")
print("_______________")

# Select and edit Questions and answers
while editing == True:
    # Select what you want to edit
    choice1 = input("Would you like to edit a question(1) or an answer(2)?: ")

    # Edit a question
    if choice1 == "1":
        num = 0
        for i in Quiz_Details["Q"]:
            num += 1
            print(f"{i}({num})")
        try:
            choice2 = int(input("Input choice: ")) - 1
        except ValueError:
            pass
        else:
            choice3 = input("Input new question: ")
            Quiz_Details["Q"][choice2] = choice3
            repeat = input("Anything else(y/n): ").lower()
            if repeat == "y":
                pass
            else:
                editing = False

    # Edit an answer
    if choice1 == "2":
        num = 0
        for i in Quiz_Details["A"]:
            num += 1
            print(f"{i}({num})")
        try:
            choice2 = int(input("Input choice: ")) - 1
        except ValueError:
            pass
        else:
            choice3 = input("Input new answer: ")
            Quiz_Details["A"][choice2] = choice3
            repeat = input("Anything else(y/n): ").lower()
            if repeat == "y":
                pass
            else:
                editing = False

# Dump info into pickle file
with open(file, "wb") as f:
    pickle.dump(Quiz_Details, f)
