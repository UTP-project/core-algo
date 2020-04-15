import random


def gen_list(start, end):
    tmp = []
    if start < end:
        tmp = [*range(start, end)]
        random.shuffle(tmp)
    return tmp


def map_sort(key, val, reverse=False):
    tmp = list(zip(key, val))
    tmp.sort(reverse=reverse)
    unzipped = list(zip(*tmp))
    return list(unzipped[0]), list(unzipped[1])


# decode the encoded route
def route_decode(day_limit_time, dur_matrix, stay_time, encoded_route):
    route = []
    sub_route = []
    prev = 0
    leave_time = 0
    for cur in encoded_route:
        # calculate return home time
        return_time = dur_matrix[cur][0]
        back_to_home_time = (
            leave_time + dur_matrix[prev][cur] + stay_time[cur] + return_time
        )

        # judge sub route end or not
        if back_to_home_time > day_limit_time:
            route.append(sub_route)
            sub_route = [cur]
            leave_time = dur_matrix[0][cur] + stay_time[cur]
        else:
            sub_route.append(cur)
            leave_time = back_to_home_time - return_time
        # update prev id
        prev = cur
    if len(sub_route) > 0:
        route.append(sub_route)
    return route


# calculate additional cost of new points use formular
def additional_cost(duration, early=0, late=0, cur_time=0, penalty_factor=0):
    return duration + max(early - cur_time, 0, cur_time - late) * penalty_factor


# calculate total cost of route
def cal_cost(route, stay_time, dur_matrix, time_window, penalty_factor=1):
    total_cost = 0
    for sub_route in route:
        prev = 0
        cur_time = 0
        for cur in sub_route:
            cur_time += stay_time[prev] + dur_matrix[prev][cur]
            early, late = time_window[cur]
            total_cost += additional_cost(
                dur_matrix[prev][cur], early, late, cur_time, penalty_factor
            )
            prev = cur
        total_cost += additional_cost(dur_matrix[prev][0])
    return total_cost
