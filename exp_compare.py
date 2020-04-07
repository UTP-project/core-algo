from GA import GA

import json
import time


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


def print_res(base, compare):
    print(base)
    for k, v in compare.items():
        print(k, v)


def param_compare():
    # use default 20 points data
    with open("test_20_0.in.json") as f:
        data = json.load(f)
    # offspring_percent, recovery_rate, pop_num=50, pfih_rate=0, rws_rate=0.5, iteration=500
    base_params = [1, 0.04, 50, 0, 1, 500]
    compare_params_dict = {
        "00-recovery": [1, 0, 50, 0, 1, 500],
        "08-recovery": [1, 0.08, 50, 0, 1, 500],
        "12-recovery": [1, 0.12, 50, 0, 1, 500],
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
        compare_res[k] = (tmp[0] - base_res[0], tmp[1] - base_res[1])
    print_res(base_res, compare_res)


def main():
    param_compare()


if __name__ == "__main__":
    main()
