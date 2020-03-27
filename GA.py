import random
from common import sort2List

def main(dist, time_cost, route_time, play_time, time_window, offspring_percent, iteration):
    days = len(route_time) - 1
    g_num = len(play_time) - 1
    population = gen_population(g_num, g_num)
    fitness, _ = cal_fitness(population, dist, time_cost, route_time, play_time, time_window)
    fitness, population = sort2List(fitness, population, True)
    print('The 0 generation:')
    print(f'population: {population}')
    print(f'fitness: {fitness}\n')
    for i in range(1, iteration + 1):
        selection_prob = [x / sum(fitness) for x in fitness]
        parents = select(population, offspring_percent, selection_prob)
        population, _ = crossover(parents)
        mutation(population)
        fitness, _ = cal_fitness(population, dist, time_cost, route_time, play_time, time_window)
        fitness, population = sort2List(fitness, population, True)
        print(f'The {i} generation:')
        print(f'population: {population}')
        print(f'fitness: {fitness}\n')
    return population, fitness

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

# calculate chromosome fitness
def cal_fitness(population, dist, time_cost, route_time, play_time, time_window):
    fitness = []
    total_cost = []
    days = len(route_time) - 1
    for _, chromosome in enumerate(population):
        cur_time = 0
        acc_route_time = 0
        day = 1
        prev = 0
        cost = 0
        for i, cur in enumerate(chromosome):
            # no solution
            if day > days:
                cost = -1
                break
            acc_route_time += time_cost[prev][cur] + play_time[cur]
            returned_time = acc_route_time + time_cost[cur][0] + play_time[0]
            if returned_time > route_time[day]:
                day += 1
                prev = 0
                cur_time = 0
                acc_route_time = time_cost[prev][cur] + play_time[cur]
                returned_time = acc_route_time + time_cost[cur][0] + play_time[0]
                # no solution
                if returned_time > route_time[day]:
                    cost = -1
                    break
            early, late = time_window[cur]
            cur_time += play_time[prev] + time_cost[prev][cur]
            cost += dist[prev][cur] + max(early - cur_time, 0, cur_time - late)
            prev = cur
            # last gene handle
            if i == len(chromosome) - 1:
                early, late = time_window[0]
                cur_time += play_time[cur] + time_cost[cur][0]
                cost += dist[prev][0] + max(early - cur_time, 0, cur_time - late)
        fitness.append(1000 / cost)
        total_cost.append(cost)
    return fitness, total_cost


# select chromosome
def select(population, offspring_percent, selection_prob):
    parentsNum = round(offspring_percent * len(selection_prob) / 2)
    parentList = []
    for i in range(parentsNum):
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

# mutation (swap)
def mutation(offspringList, mutation_prob = 0.5):
    random.seed()
    swap_points = []
    for i in range(len(offspringList)):
        tmp = random.random()
        if tmp > mutation_prob:
            swap_point = random.sample(range(len(offspringList[i])), 2)
            offspringList[i][swap_point[0]], offspringList[i][swap_point[1]] = offspringList[i][swap_point[1]], offspringList[i][swap_point[0]]
            swap_points.append(swap_point)
        else:
            swap_points.append(False)
    return swap_points

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
