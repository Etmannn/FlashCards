import pickle
import os

# initialize vars
Quiz_Details = {"Q": [], "A": []}
inputing = True
num = 0

# Get user inputs
username = input("Input Username: ")
quizname = input("Input Quiz Name: ")

# Format file name
quizname = quizname.replace(" ", "_")

# Set file location
file = str(f"userfiles/{username}/{quizname}.pkl")

# Input questions and answers
while inputing == True:
    num += 1
    Qu = input(f"\nInput Question number {num} or type 'done': ")
    if Qu == "done":
        inputing = False
    else:
        An = input(f"Input Answer for Question number {num}: ").lower()
        Quiz_Details["Q"].append(Qu)
        Quiz_Details["A"].append(An)

# Find or create folder
if os.path.isdir(f"userfiles/{username}"):
    pass
else:
    os.mkdir(f"userfiles/{username}")
    os.mkdir(f"userfiles/{username}/shared")

# Dump dictionary into pickle file
with open(file, "wb") as f:
    pickle.dump(Quiz_Details, f)
