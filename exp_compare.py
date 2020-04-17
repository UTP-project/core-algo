from core_algo.SGA import SGA
import alarm

import sys
import json
import time
from tabulate import tabulate


def average_res(ga, cal_times=100, **params):
    cost_sum = 0
    runtime_sum = 0
    for _ in range(cal_times):
        # solve the question
        res, runtime, _ = ga.solve(**params)
        # update data
        cost_sum += res[-1][1][0]
        runtime_sum += runtime
    return (cost_sum / cal_times, runtime_sum / cal_times)


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
    with open(f"input_with_location/test_{filename}.in.json") as f:
        data = json.load(f)
    xo_method = input("choose a crossover method(*pmx, cbx): ") or "pmx"
    average_times = int(input("average times: ") or 100)
    # offspring_percent, recovery_rate, pop_num=50, pfih_rate=0, rws_rate=0.5, iteration=500
    base_inst_params = {
        "recovery_rate": 0.1,
        "pop_num": 50,
        "pfih_rate": 0,
        "data": data,
        "select_method": "rws",
        "xo_method": xo_method,
    }
    solve_params = {"max_gen": 1000, "min_gen": 100, "observe_gen": 100, "mode": "dev"}
    compare_params_dict = {
        "base": {},
        "05-recovery": {"recovery_rate": 0.05},
        "15-recovery": {"recovery_rate": 0.15},
        "20-recovery": {"recovery_rate": 0.2},
        "30-pop": {"pop_num": 30},
        "40-pop": {"pop_num": 40},
        "60-pop": {"pop_num": 60},
        "70-pop": {"pop_num": 70},
        "02-pfih": {"pfih_rate": 0.02},
        "04-pfih": {"pfih_rate": 0.04},
        "06-pfih": {"pfih_rate": 0.06},
    }
    compare_res = []
    base_res = []
    for k, v in compare_params_dict.items():
        inst_params = {**base_inst_params, **v}
        ga = SGA(**inst_params)
        cost, runtime = average_res(ga, average_times, **solve_params)
        if k == "base":
            base_res = [cost, runtime]
            compare_res.append([k, cost, runtime])
        else:
            base_cost, base_runtime = base_res
            compare_res.append(
                [
                    k,
                    round((cost - base_cost) * 100 / base_cost, 2),
                    round((runtime - base_runtime) * 100 / base_runtime, 2),
                ]
            )
    headers = ["", "cost(%)", "runtime(%)"]
    tbl = tabulate(compare_res, headers=headers)
    print(tbl)

    with open(f"param_tbl/{filename}_{xo_method}_{round(time.time())}.tbl", "w") as f:
        f.write(tbl)


# def method_compare():
#     # init test data file
#     filenames = ["test_10_1", "test_20_1", "test_50_1", "test_100_1"]
#     # init method params
#     method_dict = {
#         # offspring_percent, recovery_rate, pop_num=50, pfih_rate=0, rws_rate=0.5, iteration=500
#         "SGA": [1, 0, 50, 0, 0.6, 600],
#         "RGA": [1, 0.04, 50, 0, 0.6, 600],
#         "GGA": [1, 0, 50, 0.2, 0.6, 600],
#         "GRGA": [1, 0.04, 50, 0.2, 0.6, 600],
#     }
#     header = ["", "SGA", "RGA", "GGA", "GRGA"]
#     tabular_fitness = []
#     tabular_runtime = []
#     for filename in filenames:
#         # get test data filename
#         data = {}
#         with open(f"input_data/{filename}.in.json") as f:
#             data = json.load(f)

#         # init GA
#         ga = SGA(data)

#         base_fitness = 0
#         base_runtime = 0
#         fitness_res = [filename]
#         runtime_res = [filename]
#         for k, params in method_dict.items():
#             tmp = average_res(ga, 200, *params)
#             if k == "SGA":
#                 base_fitness = tmp[0]
#                 base_runtime = tmp[1]
#             fitness_res.append(
#                 f"{round(tmp[0], 2)}({round((tmp[0] - base_fitness) * 100 / base_fitness, 1)}%)"
#             )
#             runtime_res.append(
#                 f"{round(tmp[1], 2)}({round((tmp[1] - base_runtime) * 100 / base_runtime, 1)}%)"
#             )
#         tabular_fitness.append(fitness_res)
#         tabular_runtime.append(runtime_res)
#     # make a table of result
#     fitness_table = tabulate(tabular_fitness, headers=header)
#     runtime_table = tabulate(tabular_runtime, headers=header)

#     print(fitness_table)
#     print("\n\n")
#     print(runtime_table)

#     with open(f"method_tbl/{round(time.time())}.tbl", "w") as f:
#         f.write("fitness table\n")
#         f.write(fitness_table)
#         f.write("\n\n")
#         f.write("runtime table\n")
#         f.write(runtime_table)


def main():
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == "param":
    #         param_compare()
    #     elif sys.argv[1] == "method":
    #         method_compare()
    #     else:
    #         param_compare()
    #         method_compare()
    # else:
    #     param_compare()
    #     method_compare()
    param_compare()

    # notify program is finished
    alarm.main()


if __name__ == "__main__":
    main()
