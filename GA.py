import random

# generate random list
def generateList(start, end):
    random.seed()
    tmp = []
    if start < end:
        tmp = [*range(start, end)]
        random.shuffle(tmp)
    return tmp

# generate chromosome matrix
def generateChromosomeMatrix(chromosomeNum, geneNum):
    chromosomeSet = set()
    matrix = []
    for i in range(chromosomeNum):
        chromosome = generateList(1, geneNum + 1)
        while str(chromosome) in chromosomeSet:
            chromosome = generateList(1, geneNum + 1)
        chromosomeSet.add(str(chromosome))
        matrix.append(chromosome)
    return matrix

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
        len(selectionProbability) - 1
