import common_functions
import os

# Username select
username = input("Input username: ")

# Select Quiz
file = common_functions.quizselect(username=username)

# Delete file
os.remove(file)

# Reprint list
