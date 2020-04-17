import matplotlib.pyplot as plt
from core_algo.SGA import SGA

import time
import json


def create_data(test_data):
    data = {}

    data["gene_num"] = test_data["gene_num"]
    data["locations"] = test_data["locations"]
    data["dist_matrix"] = test_data["dist_matrix"]
    data["time_matrix"] = test_data["time_matrix"]
    data["day_limit_time"] = test_data["day_limit_time"]
    data["stay_time"] = test_data["stay_time"]
    data["time_window"] = test_data["time_window"]
    data["days"] = test_data["days"]

    return data


def print_solution(data, solution):
    print()
    total_cost_time = 0
    in_time_window = []
    for day, sub_route in enumerate(solution):
        cost_time = 0
        prev = 0
        for i, cur in enumerate(sub_route):
            if i == 0:
                prev = cur
                continue
            cost_time += data["stay_time"][prev] + data["time_matrix"][prev][cur]
            if data["time_window"][cur][0] <= cost_time <= data["time_window"][cur][1]:
                if cur != 0:
                    in_time_window.append(cur)
            prev = cur
        total_cost_time += cost_time
        print(f"The {day + 1} day:")
        print(" -> ".join([str(x) for x in sub_route]))
        print(f"cost time: {cost_time}h\n")

    in_time_window.sort()
    print(f"total time spent: {total_cost_time}h")
    print(f"point in time window: {in_time_window}\n")


def draw_plot(fitness, real_gen):
    plt.figure(1)
    # preprocessing
    generation = [*range(len(fitness))]
    # unzipped_fitness = [*zip(*fitness)]
    # best_fitness = unzipped_fitness[0]
    # worst_fitness = unzipped_fitness[-1]

    # draw scatter
    for xe, ye in zip(generation, fitness):
        plt.scatter(
            [xe] * len(ye), ye, s=400 / (4 * (real_gen + 1)), c="#F44336",
        )
    # plt.xticks([*range(len(fitness))])

    # draw best and worst fitness plot
    # plt.plot(generation, best_fitness, c="#F9A825")
    # plt.plot(generation, worst_fitness)

    # set label of axis
    plt.xlabel("generation")
    plt.ylabel("fitness")

    # show plot
    plt.show()


# draw routes with locations
def draw_route(data, solution):
    plt.figure(2)

    for sub_route in solution:
        route_x = [data["locations"][point][0] for point in sub_route]
        route_y = [data["locations"][point][1] for point in sub_route]
        plt.plot(route_x, route_y)

    plt.show()


def main(test_data, inst_params, iteration_params):
    # init data
    data = create_data(test_data)
    inst_params["data"] = data

    # main
    ga = SGA(**inst_params)
    res, cal_time, last_gen = ga.solve(**iteration_params)

    unzipped_res = [*zip(*res)]
    fitness = unzipped_res[1]

    solution = ga.get_solution()
    print_solution(data, solution)

    print("fitness:", fitness[-1][0], "\n")
    print("generation:", last_gen, "\n")

    print(f"runtime: {cal_time}s")

    draw_plot(fitness, last_gen)

    draw_route(data, solution)


def get_params():
    # init test data
    # get test data from json file
    filecode = input("test data filecode: ")
    test_data = {}
    with open(f"input_with_location/test_{filecode}.in.json") as f:
        test_data = json.load(f)

    # init instantiation params
    inst_params = {}
    inst_params["select_method"] = (
        input("choose a select method(*rws, tourn): ") or "rws"
    )
    if inst_params["select_method"] == "tourn":
        set_size = int(input("set size of tourn(*2): ") or 2)
        elite_prob = float(input("elite probability of tourn(*0.5): ") or 0.5)
        inst_params["select_args"] = [set_size, elite_prob]
    inst_params["xo_method"] = input("choose a crossover method(*pmx, cbx): ") or "pmx"
    inst_params["recovery_rate"] = float(input("recovery rate(*0.04): ") or 0.04)
    inst_params["pfih_rate"] = float(input("PFIH rate(*0.2): ") or 0.2)
    inst_params["pop_num"] = int(input("population(*50): ") or 50)

    # init GA solve params
    iteration_params = {}
    iteration_mode = (
        input("choose a iteration mode(exact, *convergence, compare): ")
        or "convergence"
    )
    iteration_params["max_gen"] = int(input("max generation(*300): ") or 300)
    if iteration_mode == "convergence":
        iteration_params["min_gen"] = int(input("min generation(*100): ") or 100)
        iteration_params["observe_gen"] = int(input("observe generation(*50): ") or 50)
    elif iteration_mode == "compare":
        iteration_params["compare_res"] = float(input("compare result: "))

    return test_data, inst_params, iteration_params


if __name__ == "__main__":
    main(*get_params())
