import random
import time
import copy
import numpy as np
from common import sort2List


class GA:
    def __init__(self, data={}):
        self.gene_num = data.get("gene_num", 0)
        self.days = data.get("days", 0)
        self.dist_matrix = data.get("dist_matrix")
        self.time_matrix = data.get("time_matrix")
        self.day_limit_time = data.get("day_limit_time")
        self.stay_time = data.get("stay_time")
        self.time_window = data.get("time_window")

    def solve(self, offspring_percent, recovery_rate, iteration):
        res = []
        not_counted_time = 0
        population = self.gen_population(max(self.gene_num, 100), self.gene_num)
        fitness = self.cal_population_fitness(population)
        fitness, population = sort2List(fitness, population, True)
        start_time = time.time()
        res.append((population.copy(), fitness.copy()))
        not_counted_time += time.time() - start_time

        part_time = {}

        for _ in range(1, iteration + 1):
            # select
            start_time = time.time()
            selection_prob = self.cal_select_prob(fitness)
            parents = self.select(population, offspring_percent, selection_prob)
            run_time = time.time() - start_time
            part_time["select"] = (
                part_time["select"] + run_time if "select" in part_time else run_time
            )

            # crossover
            start_time = time.time()
            offspring, _ = self.crossover(parents)
            run_time = time.time() - start_time
            part_time["crossover"] = (
                part_time["crossover"] + run_time
                if "crossover" in part_time
                else run_time
            )

            # fitness calculate
            start_time = time.time()
            offspring_fitness = self.cal_population_fitness(offspring)
            run_time = time.time() - start_time
            part_time["fitness_calculate"] = (
                part_time["fitness_calculate"] + run_time
                if "fitness_calculate" in part_time
                else run_time
            )

            # mutation
            start_time = time.time()
            self.mutation(offspring, offspring_fitness)
            run_time = time.time() - start_time
            part_time["mutation"] = (
                part_time["mutation"] + run_time
                if "mutation" in part_time
                else run_time
            )

            # fitness sort
            start_time = time.time()
            offspring_fitness, offspring = sort2List(offspring_fitness, offspring, True)
            run_time = time.time() - start_time
            part_time["fitness_sort"] = (
                part_time["fitness_sort"] + run_time
                if "fitness_sort" in part_time
                else run_time
            )

            # recovery
            start_time = time.time()
            population, fitness = self.recovery(
                population, fitness, offspring, offspring_fitness, recovery_rate
            )
            fitness, population = sort2List(fitness, population, True)
            run_time = time.time() - start_time
            part_time["recovery"] = (
                part_time["recovery"] + run_time
                if "recovery" in part_time
                else run_time
            )

            start_time = time.time()
            res.append((population.copy(), fitness.copy()))
            not_counted_time += time.time() - start_time

        return res, not_counted_time, part_time

    # generate random list
    def gen_list(self, start, end):
        tmp = []
        if start < end:
            tmp = [*range(start, end)]
            random.shuffle(tmp)
        return tmp

    # generate chromosome matrix(population)
    def gen_population(self, chromosomeNum, geneNum):
        chromosomeSet = set()
        matrix = []
        for _ in range(chromosomeNum):
            chromosome = self.gen_list(1, geneNum + 1)
            while str(chromosome) in chromosomeSet:
                chromosome = self.gen_list(1, geneNum + 1)
            chromosomeSet.add(str(chromosome))
            matrix.append(chromosome)
        return matrix

    # calculate all population fitness
    def cal_population_fitness(self, population, penalty_factor=1):
        return [
            self.cal_fitness(chromosome, penalty_factor) for chromosome in population
        ]

    # calculate chromosome fitness
    def cal_fitness(self, chromosome, penalty_factor=1):
        cur_id = 0
        cost = 0
        for day in range(1, self.days + 1):
            prev = 0
            arrive_time = 0
            leave_time = 0
            return_time = 0
            while cur_id < len(chromosome):
                cur = chromosome[cur_id]
                # calculate return home time
                return_time = (
                    leave_time
                    + self.time_matrix[prev][cur]
                    + self.stay_time[cur]
                    + self.time_matrix[cur][0]
                )
                # return time exceed allowed time the day
                if return_time > self.day_limit_time[day]:
                    break
                # update params to current point
                arrive_time += self.stay_time[prev] + self.time_matrix[prev][cur]
                leave_time += self.time_matrix[prev][cur] + self.stay_time[cur]
                early, late = self.time_window[cur]
                cost += (
                    self.time_matrix[prev][cur]
                    + max(early - arrive_time, 0, arrive_time - late) * penalty_factor
                )
                prev = cur
                cur_id += 1

            # all the gene has been calculated
            if cur_id >= len(chromosome):
                arrive_time += self.stay_time[prev] + self.time_matrix[prev][0]
                early, late = self.time_window[0]
                cost += (
                    self.time_matrix[prev][0]
                    + max(early - arrive_time, 0, arrive_time - late) * penalty_factor
                )
                break

        # no solution
        if cur_id < len(chromosome):
            cost = -1
        return 1000 * self.gene_num / cost if cost > 0 else 0.001

    # calculate select probability (acc)
    def cal_select_prob(self, fitness):
        select_prob = []
        f_sum = sum(fitness)
        acc = 0
        for f in fitness:
            acc += f
            select_prob.append(acc / f_sum)
        return select_prob

    # select chromosome
    def select(self, population, offspring_percent, selection_prob):
        parentsNum = round(offspring_percent * len(selection_prob) / 2)
        parentList = []
        for _ in range(parentsNum):
            dad = population[self.rws(selection_prob)].copy()
            mom = population[self.rws(selection_prob)].copy()
            parentList.append((dad, mom))
        return parentList

    # crossover (partial-mapped)
    def crossover(self, parentList):
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

    def cal_mutation_prob(self, fitness, min_prob=0.06, threshold=5):
        return min_prob + 0.1 * (threshold - np.std(fitness, ddof=1))

    # mutation (swap)
    def mutation(self, offsrping_list, fitness, min_prob=0.06):
        swap_points = []
        mutation_prob = self.cal_mutation_prob(fitness)
        for i, offspring in enumerate(offsrping_list):
            tmp = random.random()
            if tmp < mutation_prob:
                swap_point = random.sample(range(len(offspring)), 2)
                offspring[swap_point[0]], offspring[swap_point[1]] = (
                    offspring[swap_point[1]],
                    offspring[swap_point[0]],
                )
                fitness[i] = self.cal_fitness(offspring)
                swap_points.append(swap_point)
            else:
                swap_points.append(False)
        return swap_points

    # recovery excellent chromosome with sorted params
    def recovery(
        self, parents, parents_fitness, offspring, offspring_fitness, rate=0.4
    ):
        recovery_num = round(len(parents) * rate)
        for i in range(recovery_num):
            offspring[-(i + 1)] = parents[i]
            offspring_fitness[-(i + 1)] = parents_fitness[i]
        return offspring, offspring_fitness

    # roulette wheel selection
    def rws(self, selection_prob, rand=0):
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
