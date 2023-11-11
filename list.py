# Functional

import functions
import pickle

username = input("Input Username: ")

file = functions.quizselect(username=username)

with open(file, "rb") as f:
    Quiz_Details = pickle.load(f)

qn = int(len(Quiz_Details["Q"]))

print("\n_______________")
for question in range(0, qn):
    print(f"{Quiz_Details['Q'][question]}: {Quiz_Details['A'][question]}")
print("_______________")
