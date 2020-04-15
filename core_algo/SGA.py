import random
import time
import copy
import numpy as np
from . import toolbox
from .select import use_select
from .crossover import use_crossover


class SGA:
    def __init__(
        self, data={}, select_method="rws", select_args=[], xo_method="pmx", xo_args=[]
    ):
        # init basic data
        self.gene_num = data.get("gene_num", 0)
        self.days = data.get("days", 0)
        self.dist_matrix = data.get("dist_matrix")
        self.time_matrix = data.get("time_matrix")
        self.day_limit_time = data.get("day_limit_time")
        self.stay_time = data.get("stay_time")
        self.time_window = data.get("time_window")

        # init basic method
        self.select = use_select(select_method)
        self.select_args = select_args
        self.crossover = use_crossover(xo_method)
        self.xo_args = xo_args

    def solve(
        self, offspring_percent, recovery_rate, pop_num=50, pfih_rate=0, iteration=500,
    ):
        res = []
        not_counted_time = 0
        # handle points num less than pop_num
        num = pop_num
        for i in range(2, self.gene_num):
            num /= i
            if num < 1:
                break
        else:
            pop_num = round(pop_num / num - 1)

        population = self.gen_population(pop_num, self.gene_num, pfih_rate)
        fitness = self.cal_population_fitness(population)
        fitness, population = toolbox.map_sort(fitness, population, True)
        start_time = time.time()
        res.append((population.copy(), fitness.copy()))
        not_counted_time += time.time() - start_time

        part_time = {}

        for _ in range(1, iteration + 1):
            # select
            start_time = time.time()
            parents = self.select(population, fitness, *self.select_args)
            run_time = time.time() - start_time
            part_time["select"] = (
                part_time["select"] + run_time if "select" in part_time else run_time
            )

            # crossover
            start_time = time.time()
            offspring = self.crossover(parents, *self.xo_args)
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
            offspring_fitness, offspring = toolbox.map_sort(
                offspring_fitness, offspring, True
            )
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
            fitness, population = toolbox.map_sort(fitness, population, True)
            run_time = time.time() - start_time
            part_time["recovery"] = (
                part_time["recovery"] + run_time
                if "recovery" in part_time
                else run_time
            )

            start_time = time.time()
            res.append((population.copy(), fitness.copy()))
            not_counted_time += time.time() - start_time

        self.solution = res[-1][0][0]
        return res, not_counted_time, part_time

    def get_solution(self):
        route = toolbox.route_decode(
            self.day_limit_time, self.time_matrix, self.stay_time, self.solution
        )
        with0_route = []
        for sub_route in route:
            with0_route.append([0, *sub_route, 0])
        return with0_route

    def pfih(self, penalty_factor=1):
        ind = []
        remain_id = [*range(1, self.gene_num + 1)]
        random.shuffle(remain_id)
        prev = 0
        cur_time = 0
        leave_time = 0
        while len(ind) < self.gene_num:
            min_id = 0
            min_additional_cost = float("inf")
            # calculate additional_cost[prev, :] of remain_id and find minimum
            for cur in remain_id:
                arrival_time = (
                    cur_time + self.stay_time[prev] + self.time_matrix[prev][cur]
                )
                early, late = self.time_window[cur]
                additional_cost = toolbox.additional_cost(
                    self.time_matrix[prev][cur],
                    early,
                    late,
                    arrival_time,
                    penalty_factor,
                )
                if additional_cost < min_additional_cost:
                    min_id = cur
                    min_additional_cost = additional_cost
            # check feasibility
            return_time = self.time_matrix[min_id][0]
            next_leave_time = (
                leave_time
                + self.time_matrix[prev][min_id]
                + self.stay_time[min_id]
                + return_time
            )
            if next_leave_time <= self.day_limit_time:
                leave_time = next_leave_time - return_time
                cur_time += self.stay_time[prev] + self.time_matrix[prev][min_id]
                prev = min_id
                ind.append(min_id)
                # remove selected id
                remain_id.remove(min_id)
            else:
                prev = 0
                cur_time = 0
                leave_time = 0
        return ind

    # generate random list
    def gen_list(self, start, end):
        tmp = []
        if start < end:
            tmp = [*range(start, end)]
            random.shuffle(tmp)
        return tmp

    # generate chromosome matrix(population)
    def gen_population(self, chromosomeNum, geneNum, pfih_rate=0):
        pfih_num = round(pfih_rate * chromosomeNum)
        chromosomeSet = set()
        matrix = []
        for _ in range(chromosomeNum - pfih_num):
            chromosome = self.gen_list(1, geneNum + 1)
            while str(chromosome) in chromosomeSet:
                chromosome = self.gen_list(1, geneNum + 1)
            chromosomeSet.add(str(chromosome))
            matrix.append(chromosome)
        for _ in range(pfih_num):
            matrix.append(self.pfih())
        return matrix

    # calculate all population fitness
    def cal_population_fitness(self, population, penalty_factor=1):
        return [
            self.cal_fitness(chromosome, penalty_factor) for chromosome in population
        ]

    # calculate chromosome fitness
    def cal_fitness(self, chromosome, penalty_factor=1):
        route = toolbox.route_decode(
            self.day_limit_time, self.time_matrix, self.stay_time, chromosome
        )
        total_cost = toolbox.cal_cost(
            route, self.stay_time, self.time_matrix, self.time_window, penalty_factor
        )
        return 1000 * self.gene_num / total_cost if total_cost > 0 else 0.001

    def cal_mutation_prob(self, fitness, min_prob=0.06, threshold=5):
        std = np.std(fitness, ddof=1)
        return min_prob if std >= threshold else min_prob + 0.1 * (threshold - std)

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
