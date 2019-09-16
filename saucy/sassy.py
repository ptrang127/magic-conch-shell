import random

def random_sass():
    with open("answers.txt") as file:
        answers = file.read().split('\n')
    return random.choice(answers)
