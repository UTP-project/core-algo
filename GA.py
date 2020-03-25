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

# select chromosome
def selectChromosome(chromosomeMatrix, offspringProportion, selectionProbability):
    offSpringNum = round(offspringProportion * len(selectionProbability) / 2)
    parentList = []
    for i in range(offSpringNum):
        dad = chromosomeMatrix[rws(selectionProbability)].copy()
        mom = chromosomeMatrix[rws(selectionProbability)].copy()
        parentList.append((dad, mom))
    return parentList

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
