import random
import time
import copy
import numpy as np
from . import toolbox
from .select import use_select
from .crossover import use_crossover


class SGA:
    def __init__(
        self,
        recovery_rate,
        pop_num,
        pfih_rate,
        data={},
        select_method="rws",
        select_args=[],
        xo_method="pmx",
        xo_args=[],
    ):
        # init basic param
        self.recovery_rate = recovery_rate
        self.pop_num = pop_num
        self.pfih_rate = pfih_rate

        # init calculate data
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
        if xo_method == "cbx":
            xo_args = [
                self.day_limit_time,
                self.stay_time,
                self.time_matrix,
                self.time_window,
                *xo_args,
            ]
        self.xo_args = xo_args

        # init final data
        self.solution = []

        # init experimental result data
        self.solve_runtime = 0

    def solve(
        self,
        max_gen,
        min_gen=None,
        observe_gen=0,
        compare_res=None,
        limit_time=None,
        mode="dev",
    ):
        is_dev = mode == "dev"
        if is_dev:
            self.solve_runtime = time.time()

        # generation param preprocess
        if min_gen is None:
            min_gen = max_gen

        res = []

        # handle points num less than pop_num
        num = self.pop_num
        for i in range(2, self.gene_num):
            num /= i
            if num < 1:
                break
        else:
            pop_num = round(pop_num / num - 1)

        # init population
        population = self.gen_population()
        fitness = self.cal_population_fitness(population)
        fitness, population = toolbox.map_sort(fitness, population)

        res.append((population.copy(), fitness.copy()))

        # init observe generation param
        cur_observe_gen = 0
        last_best = 0

        for gen in range(1, max_gen + 1):
            # update convergence observation
            cur_best = res[-1][1][0]
            if cur_best == last_best:
                cur_observe_gen += 1
            else:
                cur_observe_gen = 0
            last_best = cur_best
            # check terminate condition
            # result has converged
            if gen > min_gen and cur_observe_gen > observe_gen:
                break
            # reach the compare best
            if compare_res and cur_best < compare_res:
                break
            # out of limit time
            if limit_time and time.time() - self.solve_runtime > limit_time:
                break

            # formal process
            # select
            parents = self.select(population, fitness, *self.select_args)

            # crossover
            offspring = self.crossover(parents, *self.xo_args)

            # fitness calculate
            offspring_fitness = self.cal_population_fitness(offspring)

            # mutation
            self.mutation(offspring, offspring_fitness)

            # fitness sort
            offspring_fitness, offspring = toolbox.map_sort(
                offspring_fitness, offspring
            )

            # recovery
            population, fitness = self.recovery(
                population, fitness, offspring, offspring_fitness
            )

            # final sort
            fitness, population = toolbox.map_sort(fitness, population)

            self.solution = population[0]

            if is_dev:
                res.append((population.copy(), fitness.copy()))

        if is_dev:
            self.solve_runtime = time.time() - self.solve_runtime
            return res, self.solve_runtime, gen

    def get_solution(self):
        route = toolbox.route_decode(
            self.day_limit_time, self.time_matrix, self.stay_time, self.solution
        )
        with0_route = []
        for sub_route in route:
            with0_route.append([0, *sub_route, 0])
        return with0_route

    def pfih(self):
        ind = []
        # init random idx of gene
        remain_idx = [*range(1, self.gene_num + 1)]
        random.shuffle(remain_idx)

        start = 0
        prev = None
        while len(remain_idx) > 0:
            if prev is None:
                # pick the last idx
                ind.append(remain_idx.pop())
                continue

            # find the min distance point
            min_idx = remain_idx[0]
            min_cost = self.time_matrix[prev][min_idx]
            for idx in remain_idx:
                cost = self.time_matrix[prev][idx]
                if cost < min_cost:
                    min_idx = idx
                    min_cost = cost

            # check feasible
            encoded_route = [*ind[start:], min_idx]
            decoded_route = toolbox.route_decode(
                self.day_limit_time, self.time_matrix, self.stay_time, encoded_route
            )

            # out the day limit
            if len(decoded_route) > 1:
                start = len(ind)
                prev = remain_idx.pop()
                ind.append(prev)
                continue

            # update individul and remain idx
            prev = min_idx
            ind.append(min_idx)
            remain_idx.remove(min_idx)

        return ind

    # generate random list
    def gen_list(self, start, end):
        tmp = []
        if start < end:
            tmp = [*range(start, end)]
            random.shuffle(tmp)
        return tmp

    # generate chromosome matrix(population)
    def gen_population(self):
        pfih_num = round(self.pfih_rate * self.pop_num)
        chromosomeSet = set()
        matrix = []
        for _ in range(self.pop_num - pfih_num):
            chromosome = self.gen_list(1, self.gene_num + 1)
            while str(chromosome) in chromosomeSet:
                chromosome = self.gen_list(1, self.gene_num + 1)
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
        return total_cost

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
    def recovery(self, parents, parents_fitness, offspring, offspring_fitness):
        recovery_num = round(len(parents) * self.recovery_rate)
        for i in range(recovery_num):
            offspring[-(i + 1)] = parents[i]
            offspring_fitness[-(i + 1)] = parents_fitness[i]
        return offspring, offspring_fitness
