import functions
import pickle

username = input("Input Username: ")

file = functions.quizselect(username=username)

with open(file, "rb") as f:
    Quiz_Details = pickle.load(f)
qn = int(len(Quiz_Details["Q"]))

correctans = 0
for i in range(qn):
    correct = functions.write(file=file, question=i)
    correctans += correct

print(f"You got {correctans} out of {qn}")
