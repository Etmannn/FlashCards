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

while editing:
    # Get amout of questions
    qn = len(Quiz_Details["Q"])

    option = int(input("Edit(1), Add(2), Remove(3): "))

    for i in range(qn):
        print(f"{i}.) {Quiz_Details['Q'][i]} -> {Quiz_Details['A'][i]}")

    if option == 1:
        choice1 = int(input("Select Question to edit: "))

        print(f"{Quiz_Details['Q'][choice1]} -> {Quiz_Details['A'][choice1]}")

        choice2 = int(input("Choose what to edit: Question(1) or Answer(2): "))
        if choice2 == 1:
            choice2 = "Q"
        else:
            choice2 = "A"

        print(f"Original: {Quiz_Details[choice2][choice1]}")
        new = input("Input New Question/Answer: ")

        Quiz_Details[choice2][choice1] = new
        print(f"{Quiz_Details['Q'][choice1]} -> {Quiz_Details['A'][choice1]}")

    if option == 2:
        new = input("Input Question: ")
        new2 = input("Input Answer: ")

        Quiz_Details["Q"].append(new)
        Quiz_Details["A"].append(new2)
        print(f"{Quiz_Details['Q'][qn]} -> {Quiz_Details['A'][qn]}")

    if option == 3:
        choice1 = int(input("Select Question to remove: "))
        del Quiz_Details["Q"][choice1]
        del Quiz_Details["A"][choice1]

    loop = input("Would you like to edit anything else(y/n)")
    if loop == "n":
        editing = False

with open(file, "wb") as f:
    pickle.dump(Quiz_Details, f)
