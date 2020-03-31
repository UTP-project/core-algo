import matplotlib.pyplot as plt
from GA import main as ga

import time
import json


def create_data():
    data = {}

    data["dist"] = test_data["dist"]
    data["time_cost"] = test_data["time_cost"]
    data["route_time"] = test_data["route_time"]
    data["play_time"] = test_data["play_time"]
    data["time_window"] = test_data["time_window"]
    data["days"] = len(data["route_time"]) - 1

    return data


def print_solution(data, solution):
    print()
    total_time = 0
    cur_id = 0
    for day in range(1, data["days"] + 1):
        su_prev = 0
        prev = 0
        day_time = 0
        return_time = 0
        plan = f"route for day {day}:\n"

        while cur_id < len(solution) and return_time <= data["route_time"][day]:
            day_time += data["time_cost"][su_prev][prev] + data["play_time"][prev]
            plan += f" {prev} ->"

            cur = solution[cur_id]
            return_time = (
                day_time
                + data["time_cost"][prev][cur]
                + data["play_time"][cur]
                + data["time_cost"][cur][0]
            )

            su_prev = prev
            prev = cur
            cur_id += 1

        if return_time > data["route_time"][day]:
            day_time += data["time_cost"][su_prev][0]
            cur_id -= 1
        else:
            day_time += (
                data["time_cost"][su_prev][prev]
                + data["play_time"][prev]
                + data["time_cost"][prev][0]
            )
            plan += f" {prev} ->"

        plan += " 0\n"
        plan += f"time spent: {day_time}h\n"
        print(plan)

        total_time += day_time

        if cur_id >= len(solution):
            break

    print(f"total time spent: {total_time}h\n")


def draw_plot(fitness):
    # preprocessing
    generation = [*range(len(fitness))]
    unzipped_fitness = [*zip(*fitness)]
    best_fitness = unzipped_fitness[0]
    worst_fitness = unzipped_fitness[-1]

    # draw scatter
    for xe, ye in zip(generation, fitness):
        plt.scatter([xe] * len(ye), ye, s=1000 / (4 * (interation + 1)), c="#F44336")
    # plt.xticks([*range(len(fitness))])

    # draw best and worst fitness plot
    plt.plot(generation, best_fitness, c="#F9A825")
    plt.plot(generation, worst_fitness)

    # set label of axis
    plt.xlabel("generation")
    plt.ylabel("fitness")

    # show plot
    plt.show()


def main():
    # init data
    data = create_data()

    # mark start time
    start_time = time.time()

    # main
    res, not_counted_time, part_time = ga(
        data["dist"],
        data["time_cost"],
        data["route_time"],
        data["play_time"],
        data["time_window"],
        1,
        recovery_rate,
        interation,
    )
    cal_time = time.time() - start_time - not_counted_time

    unzipped_res = [*zip(*res)]
    fitness = unzipped_res[1]

    print_solution(data, res[-1][0][0])

    print(f"run time: {cal_time}s")

    for k, v in part_time.items():
        print(f"{k}:", f"{v}s")

    draw_plot(fitness)


filename = input("test data filename: ")
test_data = {}
with open(f"{filename}.in.json") as f:
    test_data = json.load(f)

recovery_rate = float(input("recovery rate: "))
interation = int(input("interation: "))

if __name__ == "__main__":
    main()
