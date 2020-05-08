from core_algo.SGA import SGA
import alarm

import sys
import json
import time
from tabulate import tabulate


def average_res(ga, cal_times=100, **params):
    cost_sum = 0
    runtime_sum = 0
    gen_sum = 0
    speed_sum = 0
    for _ in range(cal_times):
        # solve the question
        res, runtime, last_gen = ga.solve(**params)
        # update data
        cost_sum += res[-1][1][0]
        runtime_sum += runtime
        gen_sum += last_gen
        speed_sum += (res[0][1][0] - res[-1][1][0]) / last_gen
    return (
        cost_sum / cal_times,
        runtime_sum / cal_times,
        gen_sum / cal_times,
        speed_sum / cal_times,
    )


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
        select_args = [4, 0.7]
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
        # "convergence": {
        #     "max_gen": 500,
        #     "min_gen": 100,
        #     "observe_gen": 100,
        #     "mode": "dev",
        # },
        "time-2500": {"max_gen": 1800, "limit_time": 2.5, "mode": "dev"},
    }

    # init compare params
    compare_params_dict = {
        "00r-50p-00pf-100el": {},
        "04-recovery": {"recovery_rate": 0.04},
        "08-recovery": {"recovery_rate": 0.08},
        "04-pfih": {"pfih_rate": 0.04},
        "08-pfih": {"pfih_rate": 0.08},
        "12-pfih": {"pfih_rate": 0.12},
    }

    for iteration_mode, param in solve_params.items():
        compare_res = []
        base_res = []
        for k, v in compare_params_dict.items():
            inst_params = {**base_inst_params, **v}
            ga = SGA(**inst_params)
            cost, runtime, gen, _ = average_res(ga, average_times, **param)
            if k == "00r-50p-00pf-100el":
                base_res = [cost, runtime]
                compare_res.append([k, cost, runtime, gen])
            else:
                base_cost, base_runtime = base_res
                compare_res.append(
                    [
                        k,
                        round((cost - base_cost) * 100 / base_cost, 2),
                        round((runtime - base_runtime) * 100 / base_runtime, 2),
                        gen,
                    ]
                )
        headers = ["", "cost(%)", "runtime(%)", "generation"]
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
            "max_gen": 500,
            "min_gen": 100,
            "observe_gen": 100,
            "mode": "dev",
        },
        "time-2500": {"max_gen": 1800, "limit_time": 2.5, "mode": "dev"},
    }

    # init compare params
    compare_params_dict = {
        "obx-rws": {},
        "obx-tourn": {"select_method": "tourn", "select_args": [4, 0.7]},
        "cbx-rws": {"xo_method": "cbx"},
        "cbx-tourn": {
            "select_method": "tourn",
            "select_args": [4, 0.7],
            "xo_method": "cbx",
        },
        "cbx-rws-rec03": {"xo_method": "cbx", "recovery_rate": 0.03},
        "cbx-tourn-rec03": {
            "select_method": "tourn",
            "select_args": [4, 0.7],
            "xo_method": "cbx",
            "recovery_rate": 0.03,
        },
    }

    for iteration_mode, param in solve_params.items():
        compare_res = []
        base_res = []
        for k, v in compare_params_dict.items():
            inst_params = {**base_inst_params, **v}
            ga = SGA(**inst_params)
            cost, runtime, gen, speed = average_res(ga, average_times, **param)
            if k == "obx-rws":
                base_res = [cost, runtime]
                compare_res.append([k, cost, 0, runtime, 0, gen, speed])
            else:
                base_cost, base_runtime = base_res
                compare_res.append(
                    [
                        k,
                        cost,
                        round((cost - base_cost) * 100 / base_cost, 2),
                        runtime,
                        round((runtime - base_runtime) * 100 / base_runtime, 2),
                        gen,
                        speed,
                    ]
                )
        headers = [
            "",
            "cost",
            "cost(%)",
            "runtime",
            "runtime(%)",
            "generation",
            "con speed",
        ]
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
