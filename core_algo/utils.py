import random


def gen_list(start, end):
    tmp = []
    if start < end:
        tmp = [*range(start, end)]
        random.shuffle(tmp)
    return tmp


def sort2List(key, val, reverse=False):
    tmp = list(zip(key, val))
    tmp.sort(reverse=reverse)
    unzipped = list(zip(*tmp))
    return list(unzipped[0]), list(unzipped[1])
