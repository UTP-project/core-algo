import random
import time
import numpy as np
from common import sort2List


def main(
    dist,
    time_cost,
    route_time,
    play_time,
    time_window,
    offspring_percent,
    recovery_rate,
    iteration,
):
    res = []
    not_counted_time = 0
    g_num = len(play_time) - 1
    population = gen_population(max(g_num, 100), g_num)
    fitness, _ = cal_fitness(
        population, dist, time_cost, route_time, play_time, time_window
    )
    fitness, population = sort2List(fitness, population, True)
    start_time = time.time()
    res.append((population.copy(), fitness.copy()))
    not_counted_time += time.time() - start_time

    part_time = {}

    for _ in range(1, iteration + 1):
        # select
        start_time = time.time()
        selection_prob = [x / sum(fitness) for x in fitness]
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
        offspring_fitness, _ = cal_fitness(
            offspring, dist, time_cost, route_time, play_time, time_window
        )
        mutation(offspring, cal_mutation_prob(offspring_fitness))
        run_time = time.time() - start_time
        part_time["mutation"] = (
            part_time["mutation"] + run_time if "mutation" in part_time else run_time
        )

        # fitness calculate
        start_time = time.time()
        offspring_fitness, _ = cal_fitness(
            offspring, dist, time_cost, route_time, play_time, time_window
        )
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
    for _ in range(chromosomeNum):
        chromosome = gen_list(1, geneNum + 1)
        while str(chromosome) in chromosomeSet:
            chromosome = gen_list(1, geneNum + 1)
        chromosomeSet.add(str(chromosome))
        matrix.append(chromosome)
    return matrix


# calculate chromosome fitness
def cal_fitness(
    population, dist, time_cost, route_time, play_time, time_window, penalty_factor=1
):
    fitness = []
    total_cost = []
    days = len(route_time) - 1

    for chromosome in population:
        cur_id = 0
        cost = 0
        for day in range(1, days + 1):
            prev = 0
            arrive_time = 0
            leave_time = 0
            return_time = 0
            while cur_id < len(chromosome):
                cur = chromosome[cur_id]
                # calculate return home time
                return_time = (
                    leave_time
                    + time_cost[prev][cur]
                    + play_time[cur]
                    + time_cost[cur][0]
                )
                # return time exceed allowed time the day
                if return_time > route_time[day]:
                    break
                # update params to current point
                arrive_time += play_time[prev] + time_cost[prev][cur]
                leave_time += time_cost[prev][cur] + play_time[cur]
                early, late = time_window[cur]
                cost += (
                    time_cost[prev][cur]
                    + max(early - arrive_time, 0, arrive_time - late) * penalty_factor
                )
                prev = cur
                cur_id += 1

            # all the gene has been calculated
            if cur_id >= len(chromosome):
                arrive_time += play_time[prev] + time_cost[prev][0]
                early, late = time_window[0]
                cost += (
                    time_cost[prev][0]
                    + max(early - arrive_time, 0, arrive_time - late) * penalty_factor
                )
                break

        # no solution
        if cur_id < len(chromosome):
            cost = -1
        total_cost.append(cost)
        fitness.append(1000 * len(time_window) / cost if cost > 0 else 0.001)

    return fitness, total_cost


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
def mutation(offsrping_list, mutation_prob=0.06):
    random.seed()
    swap_points = []
    for offspring in offsrping_list:
        tmp = random.random()
        if tmp > mutation_prob:
            swap_point = random.sample(range(len(offspring)), 2)
            offspring[swap_point[0]], offspring[swap_point[1]] = (
                offspring[swap_point[1]],
                offspring[swap_point[0]],
            )
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
