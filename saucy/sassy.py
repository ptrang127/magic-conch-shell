import random

def random_sass():
    if random.randrange(100) < 50:

        f = open("./answers/no.txt")
    else:

        f = open("./answers/yes.txt")

    answers = f.read().split('\n')
    f.close()
    return random.choice(answers)