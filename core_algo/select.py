import random

from . import toolbox

# rws part
#
# calculate selection probability
def cal_select_prob(fitness):
    select_prob = []
    f_sum = sum([1 / f for f in fitness])
    acc = 0
    for f in fitness:
        acc += 1 / f
        select_prob.append(acc / f_sum)
    return select_prob


# roulette wheel selection
def rws(select_prob):
    rand = random.random()
    l = 0
    r = len(select_prob)
    while l < r:
        pos = round((r - l) / 2) + l
        if select_prob[pos] < rand:
            l = pos + 1
        elif select_prob[pos] == rand:
            return pos + 1
        else:
            if pos > 0:
                if select_prob[pos - 1] <= rand:
                    return pos
                else:
                    r = pos
            else:
                return pos
    return l


# use rws to select parents
def rws_select(population, fitness):
    pop_num = len(population)
    parents = []
    select_prob = cal_select_prob(fitness)
    for _ in range(0, pop_num, 2):
        dad = population[rws(select_prob)].copy()
        mom = population[rws(select_prob)].copy()
        parents.extend([dad, mom])
    return parents


# tournament part
#
# use tournament to select parents
def tourn_select(population, fitness, set_size=2, elite_prob=0.5):
    pop_num = len(population)
    parents = []
    for _ in range(pop_num):
        # get random set of tournament
        tourn_set_idx = random.sample(range(pop_num), set_size)

        # random pick one in tournament set
        [best_fitness_idx] = random.sample(tourn_set_idx, 1)
        best_fitness = fitness[best_fitness_idx]

        rand = random.random()
        # select best fitness individual of tournament set
        if rand <= elite_prob:
            for idx in tourn_set_idx:
                if fitness[idx] < best_fitness:
                    best_fitness_idx = idx
                    best_fitness = fitness[idx]

        parents.append(population[best_fitness_idx].copy())

    return parents


def use_select(name):
    if name == "rws":
        return rws_select
    elif name == "tourn":
        return tourn_select
    return rws_select
