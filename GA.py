import random

# generate random list
def gen_list(start, end):
    random.seed()
    tmp = []
    if start < end:
        tmp = [*range(start, end)]
        random.shuffle(tmp)
    return tmp

# generate chromosome matrix(population)
def gen_population(chromosomeNum, geneNum):
    chromosomeSet = set()
    matrix = []
    for i in range(chromosomeNum):
        chromosome = gen_list(1, geneNum + 1)
        while str(chromosome) in chromosomeSet:
            chromosome = gen_list(1, geneNum + 1)
        chromosomeSet.add(str(chromosome))
        matrix.append(chromosome)
    return matrix

# select chromosome
def select(population, offspring_percent, selection_prob):
    offSpringNum = round(offspring_percent * len(selection_prob) / 2)
    parentList = []
    for i in range(offSpringNum):
        dad = population[rws(selection_prob)].copy()
        mom = population[rws(selection_prob)].copy()
        parentList.append((dad, mom))
    return parentList

# roulette wheel selection
def rws(selection_prob):
    random.seed()
    rand = random.random()
    acc = 0
    for i, v in enumerate(selection_prob):
        acc += v
        if acc > rand:
            return i
    else:
        len(selection_prob) - 1
