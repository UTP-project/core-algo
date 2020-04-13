def sort2List(key, val, reverse=False):
    tmp = list(zip(key, val))
    tmp.sort(reverse=reverse)
    unzipped = list(zip(*tmp))
    return list(unzipped[0]), list(unzipped[1])
