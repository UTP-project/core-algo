import numpy as np
import random
import json
import math
from common import MyJSONEncoder

decimals = 2


def create_gene_number():
    return int(input("gene number: "))


# create location of points
def create_location(g_num):
    lat_range = [-10, 10]
    long_range = [-10, 10]
    location_set = set("[0, 0]")
    locations = [[0, 0]]
    i = 0
    while i < g_num:
        lati = random.uniform(*lat_range)
        longi = random.uniform(*long_range)
        location = [longi, lati]
        if str(location) not in location_set:
            locations.append(location)
            location_set.add(str(location))
            i += 1
    return locations


def create_dist_and_time_matrix(locations):
    time_dist_ratio = float(input("time cost and distance ratio: "))

    dist_matrix = []
    time_matrix = []
    for i in range(len(locations)):
        i2j_dist = []
        i2j_time = []
        for j in range(len(locations)):
            longi_diff = locations[i][0] - locations[j][0]
            lati_diff = locations[i][1] - locations[j][1]
            i2j_dist.append(math.sqrt(longi_diff ** 2 + lati_diff ** 2))
            i2j_time.append(
                math.sqrt(longi_diff ** 2 + lati_diff ** 2) * time_dist_ratio
            )
        dist_matrix.append(i2j_dist)
        time_matrix.append(i2j_time)

    return (
        dist_matrix,
        time_matrix,
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
    data["locations"] = create_location(data["gene_num"])
    data["dist_matrix"], data["time_matrix"] = create_dist_and_time_matrix(
        data["locations"]
    )
    data["days"], everyday_time, data["day_limit_time"] = create_day_time()
    data["day_limit_time"] = everyday_time
    data["stay_time"] = create_play_time(data["gene_num"])
    data["time_window"] = create_time_window(data["gene_num"], everyday_time)

    json_data = json.dumps(data, indent=4, cls=MyJSONEncoder)

    out_filename = input("generate filename: ")
    with open(f"input_with_location/{out_filename}.in.json", "w") as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
