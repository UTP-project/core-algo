import random

from . import toolbox

# rws part
#
# calculate selection probability
def cal_select_prob(fitness):
    select_prob = []
    f_sum = sum(fitness)
    acc = 0
    for f in fitness:
        acc += f
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
        parents.append((dad, mom))
    return parents


# tournament part
#
# use tournament to select parents
def tourn_select(population, fitness, set_size=2, elite_prob=0.5):
    pop_num = len(population)
    parents = []
    for _ in range(set_size):
        for cur in range(0, pop_num, set_size):
            rand = random.random()
            if rand <= elite_prob:
                # select elite(the max fitness individual)
                max_fitness_idx = cur
                max_fitness = fitness[cur]
                for offset in range(1, set_size):
                    if cur + offset < pop_num and fitness[cur + offset] > max_fitness:
                        max_fitness_idx = cur + offset
                        max_fitness = fitness[cur + offset]
                parents.append(population[max_fitness_idx].copy())
            else:
                # random pick one
                stop = set_size
                if cur + set_size >= pop_num:
                    stop = pop_num - cur
                idx = cur + random.randrange(0, stop)
                parents.append(population[idx].copy())
    # handle odd length
    if len(parents) % 2 != 0:
        parents.pop()
    parents = toolbox.adj_zip(parents, 2)
