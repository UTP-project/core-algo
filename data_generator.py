import numpy as np
import random
import json
from common import MyJSONEncoder

decimals = 2


def create_gene_number():
    return int(input("gene number: "))


def create_dist_and_time_matrix(g_num):
    dist_low = int(input("distance low number: "))
    dist_high = int(input("distance high number: "))

    dist = np.random.randint(dist_low, dist_high, (g_num + 1, g_num + 1))
    i = [*range(g_num + 1)]
    dist[i, i] = 0

    dist = np.round((dist + dist.T) / 2, decimals)

    time_dist_ratio = float(input("time cost and distance ratio: "))

    return (
        dist.tolist(),
        np.round(dist * time_dist_ratio, decimals).tolist(),
    )


def create_day_time():
    day_num = int(input("day number: "))
    everyday_time = float(input("everyday time: "))
    route_time = np.ones(day_num + 1) * everyday_time
    route_time[0] = 0
    return day_num, everyday_time, route_time.tolist()


def create_play_time(g_num):
    play_time_low = int(input("play time low: "))
    play_time_high = int(input("play time high: "))
    play_time = np.round(
        np.random.rand(g_num + 1) * (play_time_high - play_time_low) + play_time_low,
        decimals,
    )
    play_time[0] = 0
    return play_time.tolist()


def create_time_window(g_num, everyday_time):
    time_window = []
    for _ in range(g_num + 1):
        time_window.append(
            sorted(
                [
                    round(random.uniform(0, everyday_time), decimals),
                    round(random.uniform(0, everyday_time), decimals),
                ]
            )
        )
    time_window[0] = [0, 24]
    return time_window


def main():
    data = {}

    data["gene_num"] = create_gene_number()
    data["dist_matrix"], data["time_matrix"] = create_dist_and_time_matrix(
        data["gene_num"]
    )
    data["days"], everyday_time, data["day_limit_time"] = create_day_time()
    data["day_limit_time"] = everyday_time
    data["stay_time"] = create_play_time(data["gene_num"])
    data["time_window"] = create_time_window(data["gene_num"], everyday_time)

    json_data = json.dumps(data, indent=4, cls=MyJSONEncoder)

    out_filename = input("generate filename: ")
    with open(f"{out_filename}.in.json", "w") as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
