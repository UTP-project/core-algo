from core_algo.SGA import SGA
import alarm

import sys
import json
import time
from tabulate import tabulate


def average_res(ga, cal_times=100, *params):
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
    base_params = [1, 0.04, 50, 0, 0, 500]
    compare_params_dict = {
        "00-recovery": [1, 0, 50, 0, 0, 500],
        "02-recovery": [1, 0.02, 50, 0, 0, 500],
        "06-recovery": [1, 0.06, 50, 0, 0, 500],
        "08-recovery": [1, 0.08, 50, 0, 0, 500],
        "10-recovery": [1, 0.10, 50, 0, 0, 500],
        "30-pop": [1, 0.04, 30, 0, 0, 500],
        "40-pop": [1, 0.04, 40, 0, 0, 500],
        "60-pop": [1, 0.04, 60, 0, 0, 500],
        "70-pop": [1, 0.04, 70, 0, 0, 500],
        "80-pop": [1, 0.04, 80, 0, 0, 500],
        "05-pfih": [1, 0.04, 50, 0.05, 0, 500],
        "10-pfih": [1, 0.04, 50, 0.1, 0, 500],
        "15-pfih": [1, 0.04, 50, 0.15, 0, 500],
        "20-pfih": [1, 0.04, 50, 0.2, 0, 500],
        "80-rws": [1, 0.04, 50, 0, 0.8, 500],
        "60-rws": [1, 0.04, 50, 0, 0.6, 500],
        "40-rws": [1, 0.04, 50, 0, 0.4, 500],
        "20-rws": [1, 0.04, 50, 0, 0.2, 500],
    }
    ga = SGA(data)
    compare_res = {}
    base_res = average_res(ga, 100, *base_params)
    for k, params in compare_params_dict.items():
        tmp = average_res(ga, 100, *params)
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
    print_table(base_res, compare_res, header, f"param_tbl/{filename}.tbl")


def method_compare():
    # init test data file
    filenames = ["test_10_1", "test_20_1", "test_50_1", "test_100_1"]
    # init method params
    method_dict = {
        # offspring_percent, recovery_rate, pop_num=50, pfih_rate=0, rws_rate=0.5, iteration=500
        "SGA": [1, 0, 50, 0, 0.6, 600],
        "RGA": [1, 0.04, 50, 0, 0.6, 600],
        "GGA": [1, 0, 50, 0.2, 0.6, 600],
        "GRGA": [1, 0.04, 50, 0.2, 0.6, 600],
    }
    header = ["", "SGA", "RGA", "GGA", "GRGA"]
    tabular_fitness = []
    tabular_runtime = []
    for filename in filenames:
        # get test data filename
        data = {}
        with open(f"input_data/{filename}.in.json") as f:
            data = json.load(f)

        # init GA
        ga = SGA(data)

        base_fitness = 0
        base_runtime = 0
        fitness_res = [filename]
        runtime_res = [filename]
        for k, params in method_dict.items():
            tmp = average_res(ga, 200, *params)
            if k == "SGA":
                base_fitness = tmp[0]
                base_runtime = tmp[1]
            fitness_res.append(
                f"{round(tmp[0], 2)}({round((tmp[0] - base_fitness) * 100 / base_fitness, 1)}%)"
            )
            runtime_res.append(
                f"{round(tmp[1], 2)}({round((tmp[1] - base_runtime) * 100 / base_runtime, 1)}%)"
            )
        tabular_fitness.append(fitness_res)
        tabular_runtime.append(runtime_res)
    # make a table of result
    fitness_table = tabulate(tabular_fitness, headers=header)
    runtime_table = tabulate(tabular_runtime, headers=header)

    print(fitness_table)
    print("\n\n")
    print(runtime_table)

    with open(f"method_tbl/{round(time.time())}.tbl", "w") as f:
        f.write("fitness table\n")
        f.write(fitness_table)
        f.write("\n\n")
        f.write("runtime table\n")
        f.write(runtime_table)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "param":
            param_compare()
        elif sys.argv[1] == "method":
            method_compare()
        else:
            param_compare()
            method_compare()
    else:
        param_compare()
        method_compare()

    # notify program is finished
    alarm.main()


if __name__ == "__main__":
    main()
