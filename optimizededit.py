import pickle
import functions

# Select username
username = input("Input Username: ")

# Select Quiz
file = functions.quizselect(username=username)

# Open file
with open(file, "rb") as f:
    Quiz_Details = pickle.load(f)

# Get amout of questions
qn = len(Quiz_Details["Q"])


for i in range(qn):
    print(f"{Quiz_Details["Q"][i] -> {Quiz_Details["A"][i]")

print("Edit question(1) or answer(2)")
choice = input()

