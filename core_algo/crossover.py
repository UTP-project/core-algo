import random

# partial mapped crossover
def pmx(parents):
    offspring = []
    for parent in parents:
        child1 = parent[0].copy()
        child2 = parent[1].copy()
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
                del map1[t]
        for k in range(len(child2)):
            if len(map2) == 0:
                break
            while child2[k] in map2:
                t = child2[k]
                child2[k], child2[map2[t]] = child2[map2[t]], child2[k]
                del map2[t]
        offspring.append(child1)
        offspring.append(child2)
    return offspring


def use_crossover(name):
    if name == "pmx":
        return pmx
    return pmx
