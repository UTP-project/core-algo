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

# crossover (partial-mapped)
def crossover(parentList):
    random.seed()
    offspringList = []
    cuts = []
    for i in range(len(parentList)):
        child1 = parentList[i][0].copy()
        child2 = parentList[i][1].copy()
        cut = random.sample(range(1, len(child1)), 2)
        cut.sort()
        map1 = {}
        map2 = {}
        for j in range(*cut):
            map1[child2[j]] = j
            map2[child1[j]] = j
        for j in range(len(child1)):
            if len(map1) == 0:
                break
            while child1[j] in map1:
                t = child1[j]
                child1[j], child1[map1[t]] = child1[map1[t]], child1[j]
                del(map1[t])
        for k in range(len(child2)):
            if len(map2) == 0:
                break
            while child2[k] in map2:
                t = child2[k]
                child2[k], child2[map2[t]] = child2[map2[t]], child2[k]
                del(map2[t])
        offspringList.append(child1)
        offspringList.append(child2)
        cuts.append(cut)
    return offspringList, cuts


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
