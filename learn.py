import pickle
import functions

# Intialize vars
rangein = 0
rangeout = 0
rangeinlist = [1]
rangeoutlist = []

username = input("Input username: ")

file = functions.quizselect(username=username)

with open(file, "rb") as f:
    Quiz_Details = pickle.load(f)

# Get how many questions there are
qn = int(len(Quiz_Details["Q"]))


def learn(qn: int, rangein: int, rangeout: int):
    # Initialze vars
    asking = True
    totalscore = rangeout - (rangein - 1)
    multichoice = {}
    write = {}

    # Add question indexs
    for add in range(rangein - 1, rangeout):
        multichoice[add] = 0

    # Ask a segment of questions
    while asking == True:
        # Check for value of multichoice and if so switch it to write
        remove = []
        for key, value in multichoice.items():
            if value >= 2:
                remove.append(key)
                write[key] = 0
        for key in remove:
            del multichoice[key]

        # Combine dicts into one for asking questions
        combined_dict = {}
        for key in multichoice.keys():
            combined_dict[key] = 0
        for key in write.keys():
            combined_dict[key] = 1

        # Ask multichoice and write questions in order
        for key in range(rangein - 1, rangeout):
            if combined_dict.get(key) == 0:
                correct = 0
                correct = functions.mutlichoice(file=file, question=key)
                if correct > 0:
                    multichoice[key] += 1
            else:
                correct = 0
                correct = functions.write(file=file, question=key)
                if correct > 0:
                    write[key] += 1
        input("Press enter to continue: ")

        # Check whether loop is finished
        total = 0
        for value in write.values():
            total += value
        if total >= totalscore:
            asking = False


seg = 10
group = qn // seg
ones = qn % seg

if qn < 4:
    print("You need a minimum of 4 questions to use learn")
else:
    if group == 0:
        rangein = 1
        rangeout = ones
        learn(qn=qn, rangein=rangein, rangeout=rangeout)

    else:
        for tens in range(group):
            rangeoutlist.append(tens * seg + seg)
        rangeoutlist.append(rangeoutlist[-1] + ones)

        for append in rangeoutlist:
            rangeinlist.append(append + 1)

        for rangein, rangeout in zip(rangeinlist, rangeoutlist):
            learn(qn=qn, rangein=rangein, rangeout=rangeout)
