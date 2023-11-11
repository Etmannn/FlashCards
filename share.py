import os
import shutil
import pickle
import functions

username = input("Input username: ")

file = functions.quizselect(username=username)

with open(file, "rb") as f:
    Quiz_Details = pickle.load(f)

shareto = input("Input name of user to share to: ")
sharefile = f"userfiles\\{shareto}\\shared"

if shareto in os.listdir("userfiles"):
    shutil.copy(file, sharefile)

else:
    print("That user is not registered")
