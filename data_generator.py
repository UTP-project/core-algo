import numpy as np
import random
import json
from common import MyJSONEncoder

decimals = 2

g_num = int(input("gene number: "))

dist_low = int(input("distance low number: "))
dist_high = int(input("distance high number: "))

dist = np.random.randint(dist_low, dist_high, (g_num + 1, g_num + 1))
i = [*range(g_num + 1)]
dist[i, i] = 0
dist = np.round((dist + dist.T) / 2, decimals)

time_dist_ratio = float(input(("time cost and distance ratio: ")))
time_cost = np.round(dist * time_dist_ratio, decimals)

day_num = int(input("day number: "))
everyday_time = float(input("everyday time: "))
route_time = np.ones(day_num + 1) * everyday_time
route_time[0] = 0

play_time_low = int(input("play time low: "))
play_time_high = int(input("play time high: "))
play_time = np.round(
    np.random.rand(g_num + 1) * (play_time_high - play_time_low) + play_time_low,
    decimals,
)

time_window = []
for i in range(g_num + 1):
    time_window.append(
        sorted(
            [
                round(random.uniform(0, everyday_time), decimals),
                round(random.uniform(0, everyday_time), decimals),
            ]
        )
    )
time_window[0] = [0, 24]

data = {
    "g_num": g_num,
    "dist": dist.tolist(),
    "time_cost": time_cost.tolist(),
    "route_time": route_time.tolist(),
    "play_time": play_time.tolist(),
    "time_window": time_window,
}

json_data = json.dumps(data, indent=4, cls=MyJSONEncoder)

out_filename = input("generate filename: ")
with open(f"{out_filename}.in.json", "w") as f:
    f.write(json_data)
