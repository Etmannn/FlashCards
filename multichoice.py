import functions
import pickle

username = input("Input username: ")

file = functions.quizselect(username=username)

with open(file, "rb") as f:
    Quiz_Details = pickle.load(f)
qn = int(len(Quiz_Details["Q"]))

if qn < 4:
    print("You need a minimum of 4 questions to use multichoice")
else:
    correctans = 0
    for i in range(qn):
        correct = functions.mutlichoice(file=file, question=i)
        correctans += correct

    print(f"You got {correctans} out of {qn}")
