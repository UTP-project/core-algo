import random

from . import toolbox

# pmx part
#
# partial mapped crossover
def pmx(parents):
    offspring = []
    for parent in parents:
        child1 = parent[0].copy()
        child2 = parent[1].copy()
        cut = random.sample(range(1, len(child1)), 2)
        cut.sort()
        map1 = {}
        map2 = {}
        for j in range(*cut):
            map1[child2[j]] = j
            map2[child1[j]] = j
        for j in range(len(child1)):
            if len(map1) == 0:
                break
            while child1[j] in map1:
                t = child1[j]
                child1[j], child1[map1[t]] = child1[map1[t]], child1[j]
                del map1[t]
        for k in range(len(child2)):
            if len(map2) == 0:
                break
            while child2[k] in map2:
                t = child2[k]
                child2[k], child2[map2[t]] = child2[map2[t]], child2[k]
                del map2[t]
        offspring.append(child1)
        offspring.append(child2)
    return offspring


# cbx part
#
# cost based crossover
def cbx(
    parents,
    day_limit_time,
    stay_time,
    dur_matrix,
    time_window,
    x_num=4,
    penalty_factor=1,
):
    offspring = []
    rand = random.randint(0, x_num)
    for parent in parents:
        if len(parent[0]) < rand:
            offspring.extend(parent)
            continue
        # random cut position
        cut = random.sample(range(0, len(parent[0])), rand)
        cut.sort()
        # record remove points
        rm_list1, rm_list2 = [], []
        for idx in cut:
            rm_list2.append(parent[0][idx])
            rm_list1.append(parent[1][idx])
        child1, child2 = [], []
        for i in range(len(parent[0])):
            if parent[0][i] not in rm_list1:
                child1.append(parent[0][i])
            if parent[1][i] not in rm_list2:
                child2.append(parent[1][i])
        random.shuffle(rm_list1)
        random.shuffle(rm_list2)

        # calculate child1 insert cost
        for ins_targ in rm_list1:
            min_cost1 = float("inf")
            min_cost_idx1 = -1
            for ins_idx in range(len(child1)):
                tmp = child1.copy()
                tmp.insert(ins_idx, ins_targ)
                # calculate cost
                route = toolbox.route_decode(day_limit_time, dur_matrix, stay_time, tmp)
                cost = toolbox.cal_cost(
                    route, stay_time, dur_matrix, time_window, penalty_factor
                )
                if cost < min_cost1:
                    min_cost1 = cost
                    min_cost_idx1 = ins_idx
            child1.insert(min_cost_idx1, ins_targ)

        # calculate child2 insert cost
        for ins_targ in rm_list2:
            min_cost2 = float("inf")
            min_cost_idx2 = -1
            for ins_idx in range(len(child2)):
                tmp = child2.copy()
                tmp.insert(ins_idx, ins_targ)
                # calculate cost
                route = toolbox.route_decode(day_limit_time, dur_matrix, stay_time, tmp)
                cost = toolbox.cal_cost(
                    route, stay_time, dur_matrix, time_window, penalty_factor
                )
                if cost < min_cost2:
                    min_cost2 = cost
                    min_cost_idx2 = ins_idx
            child2.insert(min_cost_idx2, ins_targ)
        offspring.extend([child1, child2])
    return offspring


def use_crossover(name):
    if name == "pmx":
        return pmx
    if name == "cbx":
        return cbx
    return pmx
