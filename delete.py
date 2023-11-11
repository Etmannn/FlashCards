import functions
import os

# Username select
username = input("Input username: ")

# Select Quiz
file = functions.quizselect(username=username)

# Delete file
os.remove(file)

# Reprint list
