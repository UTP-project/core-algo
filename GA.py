import random
import time
import numpy as np
from common import sort2List


def main(data, offspring_percent, recovery_rate, iteration):
    random.seed()
    res = []
    not_counted_time = 0
    g_num = data["gene_num"]
    population = gen_population(max(g_num, 100), g_num)
    fitness = cal_population_fitness(population, data)
    fitness, population = sort2List(fitness, population, True)
    start_time = time.time()
    res.append((population.copy(), fitness.copy()))
    not_counted_time += time.time() - start_time

    part_time = {}

    for _ in range(1, iteration + 1):
        # select
        start_time = time.time()
        selection_prob = cal_select_prob(fitness)
        parents = select(population, offspring_percent, selection_prob)
        run_time = time.time() - start_time
        part_time["select"] = (
            part_time["select"] + run_time if "select" in part_time else run_time
        )

        # crossover
        start_time = time.time()
        offspring, _ = crossover(parents)
        run_time = time.time() - start_time
        part_time["crossover"] = (
            part_time["crossover"] + run_time if "crossover" in part_time else run_time
        )

        # mutation
        start_time = time.time()
        offspring_fitness = cal_population_fitness(offspring, data)
        mutation(offspring, offspring_fitness, data)
        run_time = time.time() - start_time
        part_time["mutation"] = (
            part_time["mutation"] + run_time if "mutation" in part_time else run_time
        )

        # fitness calculate
        start_time = time.time()
        offspring_fitness, offspring = sort2List(offspring_fitness, offspring, True)
        run_time = time.time() - start_time
        part_time["final_calculate"] = (
            part_time["final_calculate"] + run_time
            if "final_calculate" in part_time
            else run_time
        )

        # recovery
        start_time = time.time()
        population, fitness = recovery(
            population, fitness, offspring, offspring_fitness, recovery_rate
        )
        fitness, population = sort2List(fitness, population, True)
        run_time = time.time() - start_time
        part_time["recovery"] = (
            part_time["recovery"] + run_time if "recovery" in part_time else run_time
        )

        start_time = time.time()
        res.append((population.copy(), fitness.copy()))
        not_counted_time += time.time() - start_time

    return res, not_counted_time, part_time


# generate random list
def gen_list(start, end):
    tmp = []
    if start < end:
        tmp = [*range(start, end)]
        random.shuffle(tmp)
    return tmp


# generate chromosome matrix(population)
def gen_population(chromosomeNum, geneNum):
    chromosomeSet = set()
    matrix = []
    for _ in range(chromosomeNum):
        chromosome = gen_list(1, geneNum + 1)
        while str(chromosome) in chromosomeSet:
            chromosome = gen_list(1, geneNum + 1)
        chromosomeSet.add(str(chromosome))
        matrix.append(chromosome)
    return matrix


# calculate all population fitness
def cal_population_fitness(population, data, penalty_factor=1):
    return [cal_fitness(chromosome, data, penalty_factor) for chromosome in population]


# calculate chromosome fitness
def cal_fitness(chromosome, data, penalty_factor=1):
    cur_id = 0
    cost = 0
    for day in range(1, data["days"] + 1):
        prev = 0
        arrive_time = 0
        leave_time = 0
        return_time = 0
        while cur_id < len(chromosome):
            cur = chromosome[cur_id]
            # calculate return home time
            return_time = (
                leave_time
                + data["time_matrix"][prev][cur]
                + data["stay_time"][cur]
                + data["time_matrix"][cur][0]
            )
            # return time exceed allowed time the day
            if return_time > data["day_limit_time"][day]:
                break
            # update params to current point
            arrive_time += data["stay_time"][prev] + data["time_matrix"][prev][cur]
            leave_time += data["time_matrix"][prev][cur] + data["stay_time"][cur]
            early, late = data["time_window"][cur]
            cost += (
                data["time_matrix"][prev][cur]
                + max(early - arrive_time, 0, arrive_time - late) * penalty_factor
            )
            prev = cur
            cur_id += 1

        # all the gene has been calculated
        if cur_id >= len(chromosome):
            arrive_time += data["stay_time"][prev] + data["time_matrix"][prev][0]
            early, late = data["time_window"][0]
            cost += (
                data["time_matrix"][prev][0]
                + max(early - arrive_time, 0, arrive_time - late) * penalty_factor
            )
            break

    # no solution
    if cur_id < len(chromosome):
        cost = -1
    return 1000 * data["gene_num"] / cost if cost > 0 else 0.001


# calculate select probability (acc)
def cal_select_prob(fitness):
    select_prob = []
    f_sum = sum(fitness)
    acc = 0
    for f in fitness:
        acc += f
        select_prob.append(acc / f_sum)
    return select_prob


# select chromosome
def select(population, offspring_percent, selection_prob):
    parentsNum = round(offspring_percent * len(selection_prob) / 2)
    parentList = []
    for _ in range(parentsNum):
        dad = population[rws(selection_prob)].copy()
        mom = population[rws(selection_prob)].copy()
        parentList.append((dad, mom))
    return parentList


# crossover (partial-mapped)
def crossover(parentList):
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
                del map1[t]
        for k in range(len(child2)):
            if len(map2) == 0:
                break
            while child2[k] in map2:
                t = child2[k]
                child2[k], child2[map2[t]] = child2[map2[t]], child2[k]
                del map2[t]
        offspringList.append(child1)
        offspringList.append(child2)
        cuts.append(cut)
    return offspringList, cuts


def cal_mutation_prob(fitness, min_prob=0.06, threshold=5):
    return min_prob + 0.1 * (threshold - np.std(fitness, ddof=1))


# mutation (swap)
def mutation(offsrping_list, fitness, data, min_prob=0.06):
    swap_points = []
    mutation_prob = cal_mutation_prob(fitness)
    for i, offspring in enumerate(offsrping_list):
        tmp = random.random()
        if tmp < mutation_prob:
            swap_point = random.sample(range(len(offspring)), 2)
            offspring[swap_point[0]], offspring[swap_point[1]] = (
                offspring[swap_point[1]],
                offspring[swap_point[0]],
            )
            fitness[i] = cal_fitness(offspring, data)
            swap_points.append(swap_point)
        else:
            swap_points.append(False)
    return swap_points


# recovery excellent chromosome with sorted params
def recovery(parents, parents_fitness, offspring, offspring_fitness, rate=0.4):
    recovery_num = round(len(parents) * rate)
    for i in range(recovery_num):
        offspring[-(i + 1)] = parents[i]
        offspring_fitness[-(i + 1)] = parents_fitness[i]
    return offspring, offspring_fitness


# roulette wheel selection
def rws(selection_prob, rand=0):
    if rand == 0:
        rand = random.random()
    l = 0
    r = len(selection_prob)
    while l < r:
        pos = round((r - l) / 2) + l
        if selection_prob[pos] < rand:
            l = pos + 1
        elif selection_prob[pos] == rand:
            return pos + 1
        else:
            if pos > 0:
                if selection_prob[pos - 1] <= rand:
                    return pos
                else:
                    r = pos
            else:
                return pos
    return l
