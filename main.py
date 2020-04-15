import matplotlib.pyplot as plt
from core_algo.SGA import SGA

import time
import json


def create_data():
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
                in_time_window.append(cur)
            prev = cur
        total_cost_time += cost_time
        print(f"The {day + 1} day:")
        print(" -> ".join([str(x) for x in sub_route]))
        print(f"cost time: {cost_time}h\n")

    print(f"total time spent: {total_cost_time}h")
    print(f"point in time window: {in_time_window}\n")


def draw_plot(fitness):
    plt.figure(1)
    # preprocessing
    generation = [*range(len(fitness))]
    # unzipped_fitness = [*zip(*fitness)]
    # best_fitness = unzipped_fitness[0]
    # worst_fitness = unzipped_fitness[-1]

    # draw scatter
    for xe, ye in zip(generation, fitness):
        plt.scatter([xe] * len(ye), ye, s=400 / (4 * (interation + 1)), c="#F44336")
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


def main():
    # init data
    data = create_data()

    # mark start time
    start_time = time.time()

    # main
    ga = SGA(data, select_method, crossover_method)
    res, not_counted_time, part_time = ga.solve(
        1, recovery_rate, pop_num, pfih_rate, interation
    )
    cal_time = time.time() - start_time - not_counted_time

    unzipped_res = [*zip(*res)]
    fitness = unzipped_res[1]

    solution = ga.get_solution()
    print_solution(data, solution)

    print("fitness:", fitness[-1][0], "\n")

    print(f"run time: {cal_time}s")

    for k, v in part_time.items():
        print(f"{k}:", f"{v}s")

    draw_plot(fitness)

    draw_route(data, solution)


filecode = input("test data filecode: ")
test_data = {}
with open(f"input_with_location/test_{filecode}.in.json") as f:
    test_data = json.load(f)

select_method = input("choose a select method(*rws, tourn): ") or "rws"
crossover_method = input("choose a crossover method(*pmx): ") or "pmx"
recovery_rate = float(input("recovery rate(*0.04): ") or 0.04)
pfih_rate = float(input("PFIH rate(*0.2): ") or 0.2)
pop_num = int(input("population(*50): ") or 50)
interation = int(input("interation(*600): ") or 600)

if __name__ == "__main__":
    main()
