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

    # get output filename
    output_filename = input("output filename: ")

    # init output file
    print_file = f"param_tbl/{output_filename}_{filename}_{round(time.time())}.tbl"

    # get params by input
    select_method = input("choose a select method(*rws, tourn): ") or "rws"
    select_args = []
    if select_method == "tourn":
        set_size = int(input("set size of tourn(*2): ") or 2)
        select_args = [set_size, 1]
    xo_method = input("choose a crossover method(*pmx, cbx): ") or "pmx"

    # get average times
    average_times = int(input("average times(*100): ") or 100)

    # init base params while create new GA instance
    base_inst_params = {
        "recovery_rate": 0,
        "pop_num": 50,
        "pfih_rate": 0,
        "data": data,
        "select_method": select_method,
        "select_args": select_args,
        "xo_method": xo_method,
    }

    # init solve params
    solve_params = {
        "convergence": {
            "max_gen": 300,
            "min_gen": 100,
            "observe_gen": 80,
            "mode": "dev",
        },
        "exact-300": {"max_gen": 300, "mode": "dev"},
    }

    # init compare params
    compare_params_dict = {
        "00r-50p-00pf": {},
        "02-recovery": {"recovery_rate": 0.02},
        "06-recovery": {"recovery_rate": 0.06},
        "04-pfih": {"pfih_rate": 0.04},
        "08-pfih": {"pfih_rate": 0.08},
        "12-pfih": {"pfih_rate": 0.12},
    }

    #
    if select_method == "tourn":
        compare_params_dict["60-elite"] = {"select_args": [select_args[0], 0.6]}
        compare_params_dict["70-elite"] = {"select_args": [select_args[0], 0.7]}
        compare_params_dict["80-elite"] = {"select_args": [select_args[0], 0.8]}
        compare_params_dict["90-elite"] = {"select_args": [select_args[0], 0.9]}

    for iteration_mode, param in solve_params.items():
        compare_res = []
        base_res = []
        for k, v in compare_params_dict.items():
            inst_params = {**base_inst_params, **v}
            ga = SGA(**inst_params)
            cost, runtime = average_res(ga, average_times, **param)
            if k == "00r-50p-00pf":
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

        with open(print_file, "a") as f:
            f.write(f"{iteration_mode}\n")
            f.write(f"{tbl}\n\n")


def method_compare():
    # get test data filename
    data = {}
    filename = input("test data file: ")
    with open(f"input_with_location/test_{filename}.in.json") as f:
        data = json.load(f)

    # get output filename
    output_filename = input("output filename: ")

    # init output file
    print_file = f"method_tbl/{output_filename}_{filename}_{round(time.time())}.tbl"

    # get average times
    average_times = int(input("average times(*100): ") or 100)

    # init base params while create new GA instance
    base_inst_params = {
        "recovery_rate": 0,
        "pop_num": 50,
        "pfih_rate": 0,
        "data": data,
        "select_method": "rws",
        "select_args": [],
        "xo_method": "pmx",
    }

    # init solve params
    solve_params = {
        "convergence": {
            "max_gen": 300,
            "min_gen": 100,
            "observe_gen": 80,
            "mode": "dev",
        },
        "exact-300": {"max_gen": 300, "mode": "dev"},
    }

    # init compare params
    compare_params_dict = {
        "rws-pmx": {},
        "tourn-pmx": {"select_method": "tourn", "select_args": [4, 0.9]},
        "rws-cbx": {"xo_method": "cbx"},
        "tourn-cbx": {
            "select_method": "tourn",
            "select_args": [4, 0.9],
            "xo_method": "cbx",
        },
    }

    for iteration_mode, param in solve_params.items():
        compare_res = []
        base_res = []
        for k, v in compare_params_dict.items():
            inst_params = {**base_inst_params, **v}
            ga = SGA(**inst_params)
            cost, runtime = average_res(ga, average_times, **param)
            if k == "rws-pmx":
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

        with open(print_file, "a") as f:
            f.write(f"{iteration_mode}\n")
            f.write(f"{tbl}\n\n")


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
