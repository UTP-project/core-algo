from GA import GA

import json
import time
from tabulate import tabulate


def average_res(ga, *params):
    cal_times = 100
    fitness_sum = 0
    runtime_sum = 0
    for _ in range(cal_times):
        # mark start time
        start_time = time.time()
        # solve the question
        res, not_counted_time, _ = ga.solve(*params)
        runtime = time.time() - start_time - not_counted_time
        # update data
        fitness_sum += res[-1][1][0]
        runtime_sum += runtime
    return (fitness_sum / cal_times, runtime_sum / cal_times)


def print_table(base, compare, header, filename=""):
    tabular_data = []
    tabular_data.append(["base", *base])
    for k, v in compare.items():
        tabular_data.append([k, *v])
    table = tabulate(tabular_data, headers=["", *header])
    print(table)

    if filename:
        with open(filename, "w") as f:
            f.write(table)


def param_compare():
    # get test data filename
    data = {}
    filename = input("test data file: ")
    with open(f"{filename}.in.json") as f:
        data = json.load(f)
    # offspring_percent, recovery_rate, pop_num=50, pfih_rate=0, rws_rate=0.5, iteration=500
    base_params = [1, 0.04, 50, 0, 1, 500]
    compare_params_dict = {
        "00-recovery": [1, 0, 50, 0, 1, 500],
        "02-recovery": [1, 0.02, 50, 0, 1, 500],
        "06-recovery": [1, 0.06, 50, 0, 1, 500],
        "08-recovery": [1, 0.08, 50, 0, 1, 500],
        "10-recovery": [1, 0.10, 50, 0, 1, 500],
        "30-pop": [1, 0.04, 30, 0, 1, 500],
        "40-pop": [1, 0.04, 40, 0, 1, 500],
        "60-pop": [1, 0.04, 60, 0, 1, 500],
        "70-pop": [1, 0.04, 70, 0, 1, 500],
        "80-pop": [1, 0.04, 80, 0, 1, 500],
        "05-pfih": [1, 0.04, 50, 0.05, 1, 500],
        "10-pfih": [1, 0.04, 50, 0.1, 1, 500],
        "15-pfih": [1, 0.04, 50, 0.15, 1, 500],
        "20-pfih": [1, 0.04, 50, 0.2, 1, 500],
        "80-rws": [1, 0.04, 50, 0, 0.8, 500],
        "60-rws": [1, 0.04, 50, 0, 0.6, 500],
        "40-rws": [1, 0.04, 50, 0, 0.4, 500],
        "20-rws": [1, 0.04, 50, 0, 0.2, 500],
        "00-rws": [1, 0.04, 50, 0, 0, 500],
    }
    ga = GA(data)
    compare_res = {}
    base_res = average_res(ga, *base_params)
    for k, params in compare_params_dict.items():
        tmp = average_res(ga, *params)
        fitness_diff = tmp[0] - base_res[0]
        runtime_diff = tmp[1] - base_res[1]
        compare_res[k] = (
            round(fitness_diff, 2),
            round(fitness_diff * 100 / base_res[0], 2),
            round(runtime_diff, 2),
            round(runtime_diff * 100 / base_res[1], 2),
        )
    base_res = (round(base_res[0], 2), 0, round(base_res[1], 2), 0)
    header = ["fitness", "fitness growth(%)", "runtime", "runtime growth(%)"]
    print_table(base_res, compare_res, header, f"{filename}.tbl")


def main():
    param_compare()


if __name__ == "__main__":
    main()
