import random

# roulette wheel selection
def rws(selectionProbability):
    random.seed()
    rand = random.random()
    acc = 0
    for i, v in enumerate(selectionProbability):
        acc += v
        if acc > rand:
            return i
    else:
        return i
