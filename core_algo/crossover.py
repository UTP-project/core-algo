import random

from . import toolbox


def preprocess(parents, xo_prob):
    real_parents = []
    offspring = []
    for parent in parents:
        rand = random.random()
        if rand <= xo_prob:
            real_parents.append(parent)
        else:
            offspring.append(parent)
    # check odd length
    if len(real_parents) % 2 != 0:
        offspring.append(real_parents.pop())
    return real_parents, offspring


# pmx part
#
# partial mapped crossover
def pmx(parents, xo_prob=0.8):
    real_parents, offspring = preprocess(parents, xo_prob)
    for parent_id in range(0, len(real_parents), 2):
        child1 = real_parents[parent_id].copy()
        child2 = real_parents[parent_id + 1].copy()
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
    xo_prob=0.8,
):
    real_parents, offspring = preprocess(parents, xo_prob)
    for parent_id in range(0, len(real_parents), 2):
        # get cur route
        dad_route = toolbox.route_decode(
            day_limit_time, dur_matrix, stay_time, real_parents[parent_id]
        )
        mom_route = toolbox.route_decode(
            day_limit_time, dur_matrix, stay_time, real_parents[parent_id + 1]
        )
        # random remove element for other
        rand = random.randint(1, x_num)
        remove_idx = random.sample(range(len(real_parents[parent_id])), rand)
        dad_remove, mom_remove = [], []
        for i in remove_idx:
            dad_remove.append(real_parents[parent_id + 1][i])
            mom_remove.append(real_parents[parent_id][i])
        # remove element of the route
        for remove_el in dad_remove:
            for sub_route in dad_route:
                if remove_el in sub_route:
                    sub_route.remove(remove_el)
                    break

        for remove_el in mom_remove:
            for sub_route in mom_route:
                if remove_el in sub_route:
                    sub_route.remove(remove_el)
                    break

        # check empty sub route
        dad_route = list(filter(None, dad_route))
        mom_route = list(filter(None, mom_route))
        # shuffle the removed element
        random.shuffle(dad_remove)
        random.shuffle(mom_remove)
        # try to insert the removed element
        # insert to dad
        dad_route_cost = [
            toolbox.cal_cost(
                [sub_route], stay_time, dur_matrix, time_window, penalty_factor
            )
            for sub_route in dad_route
        ]
        for ins_el in dad_remove:
            dad_min_cost = float("inf")
            dad_min_total_cost = float("inf")
            dad_min_cost_pos = []
            for sub_idx, sub_route in enumerate(dad_route):
                for ins_idx in range(len(sub_route) + 1):
                    tmp = sub_route.copy()
                    tmp.insert(ins_idx, ins_el)
                    # get new route after insert
                    new_sub_route = toolbox.route_decode(
                        day_limit_time, dur_matrix, stay_time, tmp
                    )
                    # calculate current cost
                    cost = toolbox.cal_cost(
                        new_sub_route,
                        stay_time,
                        dur_matrix,
                        time_window,
                        penalty_factor,
                    )
                    total_cost = cost
                    for i in range(len(dad_route)):
                        if i != sub_idx:
                            total_cost += dad_route_cost[i]
                    # check if min
                    if total_cost < dad_min_total_cost:
                        dad_min_cost = cost
                        dad_min_total_cost = total_cost
                        dad_min_cost_pos = [sub_idx, ins_idx]
            dad_route[dad_min_cost_pos[0]].insert(dad_min_cost_pos[1], ins_el)
            dad_route_cost[dad_min_cost_pos[0]] = dad_min_cost
        child1 = [el for sub_route in dad_route for el in sub_route]
        # insert to mom
        mom_route_cost = [
            toolbox.cal_cost(
                [sub_route], stay_time, dur_matrix, time_window, penalty_factor
            )
            for sub_route in mom_route
        ]
        for ins_el in mom_remove:
            mom_min_cost = float("inf")
            mom_min_total_cost = float("inf")
            mom_min_cost_pos = []
            for sub_idx, sub_route in enumerate(mom_route):
                for ins_idx in range(len(sub_route) + 1):
                    tmp = sub_route.copy()
                    tmp.insert(ins_idx, ins_el)
                    # get new route after insert
                    new_sub_route = toolbox.route_decode(
                        day_limit_time, dur_matrix, stay_time, tmp
                    )
                    # calculate current cost
                    cost = toolbox.cal_cost(
                        new_sub_route,
                        stay_time,
                        dur_matrix,
                        time_window,
                        penalty_factor,
                    )
                    total_cost = cost
                    for i in range(len(mom_route)):
                        if i != sub_idx:
                            total_cost += mom_route_cost[i]
                    # check if min
                    if total_cost < mom_min_total_cost:
                        mom_min_cost = cost
                        mom_min_total_cost = total_cost
                        mom_min_cost_pos = [sub_idx, ins_idx]
            mom_route[mom_min_cost_pos[0]].insert(mom_min_cost_pos[1], ins_el)
            mom_route_cost[mom_min_cost_pos[0]] = mom_min_cost
        child2 = [el for sub_route in mom_route for el in sub_route]
        offspring.extend([child1, child2])
    return offspring


def use_crossover(name):
    if name == "pmx":
        return pmx
    if name == "cbx":
        return cbx
    return pmx
