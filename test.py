import random
import copy
import json
import numpy as np
from common import printList, printErrorMsg, printSuccessMsg, sort2List
from GA import (
    rws,
    cal_select_prob,
    gen_population,
    select,
    crossover,
    mutation,
    cal_population_fitness,
    recovery,
    cal_mutation_prob,
    gen_list,
)

# generate chromosome matrix test
def gcm_test():
    g_num = random.randint(10, 100)
    c_num = g_num
    m = gen_population(c_num, g_num)
    c_set = set()
    info = {"c_num": c_num, "g_num": g_num}
    for i in range(len(m)):
        c_set.add(str(m[i]))
        g_set = set(m[i])
        if len(g_set) != g_num:
            indent = printErrorMsg(
                "gcm", "gene number is not right!", g_num, len(g_set), info
            )
            printList(m, name="matrix", prefix=indent)
            return
    if len(c_set) != c_num:
        indent = printErrorMsg(
            "gcm", "chromosome number is not right!", c_num, len(c_set), info
        )
        printList(m, name="matrix", prefix=indent)
        return
    printSuccessMsg("gcm")


# fitness calculate test
def cal_fitness_test():
    population = gen_population(test_data["gene_num"], test_data["gene_num"])
    cal_population_fitness(population, test_data)
    printSuccessMsg("calculate fitness")


# roulette wheel selection test
def rws_test():
    inputData = [
        [0.1, 0.3, 0.6, 0.9, 1],
        [0.6, 0.7, 1],
        [0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [0.001, 0.101, 0.378, 0.413, 0.4999, 0.9, 0.99, 1],
        [0.001, 0.3333, 0.499, 0.5, 0.511, 0.677, 0.899, 0.901, 0.956, 0.991, 1],
    ]
    expect = [2, 0, 1, 5, 4]
    for i, v in enumerate(inputData):
        outputData = rws(v, 0.5)
        info = {"inputData": v}
        if outputData != expect[i]:
            printErrorMsg("rws", "index not right", expect[i], outputData, info)
    printSuccessMsg("rws")


def cal_select_prob_test():
    inputData = [[1, 2, 3, 4]]
    expect = [[0.1, 0.3, 0.6, 1]]
    for i, v in enumerate(inputData):
        outputData = cal_select_prob(v)
        info = {"inputData": v}
        for j in range(len(v)):
            if outputData[j] != expect[i][j]:
                printErrorMsg(
                    "select probability", "not right", expect[i], outputData, info
                )
    printSuccessMsg("select probability")


def select_test():
    random.seed()
    offspring_p = random.random()
    selection_p = [
        [0.1, 0.3, 0.6, 0.9, 1],
        [0.6, 0.7, 1],
        [0.5, 0.6, 0.7, 0.8, 0.9, 1],
        [0.001, 0.101, 0.378, 0.413, 0.4999, 0.9, 0.99, 1],
        [0.001, 0.3333, 0.499, 0.5, 0.511, 0.677, 0.899, 0.901, 0.956, 0.991, 1],
    ]
    for v in selection_p:
        num = len(v)
        m = gen_population(num, num)
        parents = select(m, offspring_p, v)
        if len(parents) != round(offspring_p * num / 2):
            indent = printErrorMsg(
                "select",
                "parents number is not right",
                round(offspring_p * num / 2),
                len(parents),
            )
            printList(parents, 3, name="parents list", prefix=indent)
    printSuccessMsg("select")


def crossover_test():
    random.seed()
    g_num = random.randint(10, 100)
    p_num = g_num
    parentList = []
    for i in range(p_num):
        parentList.append((gen_list(1, g_num + 1), gen_list(1, g_num + 1)))
    offspringList, cuts = crossover(parentList)

    if len(offspringList) != p_num * 2:
        indent = printErrorMsg(
            "cross", "offspring number is not right", p_num * 2, len(offspringList)
        )
        printList(offspringList, name="offspring list", prefix=indent)

    for i in range(len(parentList)):
        for j in range(*cuts[i]):
            if offspringList[i * 2][j] != parentList[i][1][j]:
                printErrorMsg(
                    "cross",
                    f"offspring not match parent on the pos {j}",
                    parentList[i][1][j],
                    offspringList[i * 2][j],
                    {
                        "cuts": cuts[i],
                        "parent": parentList[i],
                        "offspring": (offspringList[i * 2], offspringList[i * 2 + 1]),
                    },
                )
                return
            if offspringList[i * 2 + 1][j] != parentList[i][0][j]:
                printErrorMsg(
                    "cross",
                    f"offspring not match parent on the pos {j}",
                    parentList[i][0][j],
                    offspringList[i * 2 + 1][j],
                    {
                        "cuts": cuts[i],
                        "parent": parentList[i],
                        "offspring": (offspringList[i * 2], offspringList[i * 2 + 1]),
                    },
                )
                return

    for i in range(len(offspringList)):
        if len(set(offspringList[i])) != g_num:
            printErrorMsg(
                "cross",
                "offspring gene number not right or has repeated value",
                g_num,
                len(set(offspringList[i])),
                {"offspring": offspringList[i]},
            )

    printSuccessMsg("cross")


def mutation_test():
    random.seed()
    g_num = random.randint(10, 100)
    o_num = g_num
    offspringList = []
    for i in range(o_num):
        offspringList.append(gen_list(1, g_num + 1))
    o_offspringList = copy.deepcopy(offspringList)
    fitness = gen_list(0, o_num)

    sp = mutation(offspringList, fitness, test_data)

    for i in range(o_num):
        if sp[i]:
            if (
                o_offspringList[i][sp[i][0]] != offspringList[i][sp[i][1]]
                or o_offspringList[i][sp[i][1]] != offspringList[i][sp[i][0]]
            ):
                expect = o_offspringList[i].copy()
                expect[sp[i][0]], expect[sp[i][1]] = expect[sp[i][1]], expect[sp[i][0]]
                printErrorMsg(
                    "mutation",
                    "swap value is not right",
                    expect,
                    offspringList[i],
                    {"swap_point": sp[i]},
                )

    printSuccessMsg("mutation")


def sort_test():
    key = [3, 2, 4, 1]
    val = ["a", "b", "d", "c"]
    key_expect = [1, 2, 3, 4]
    val_expect = ["c", "b", "a", "d"]
    output_key, output_val = sort2List(key, val)
    for i in range(len(output_key)):
        if output_key[i] != key_expect[i]:
            printErrorMsg(
                "sort",
                f"key output not right on pos {i}",
                key_expect[i],
                output_key[i],
                {"key": key, "expect_key": key_expect, "output": output_key},
            )
            return
        if output_val[i] != val_expect[i]:
            printErrorMsg(
                "sort",
                f"val output not right on pos {i}",
                val_expect[i],
                output_val[i],
                {"val": val, "expect_val": val_expect, "output": output_val},
            )
            return

    output_key, output_val = sort2List(key, val, True)
    key_expect.reverse()
    val_expect.reverse()
    for i in range(len(output_key)):
        if output_key[i] != key_expect[i]:
            printErrorMsg(
                "sort",
                f"key output not right on pos {i} while reverse",
                key_expect[i],
                output_key[i],
                {"key": key, "expect_key": key_expect, "output": output_key},
            )
            return
        if output_val[i] != val_expect[i]:
            printErrorMsg(
                "sort",
                f"val output not right on pos {i} while reverse",
                val_expect[i],
                output_val[i],
                {"val": val, "expect_val": val_expect, "output": output_val},
            )
            return
    printSuccessMsg("sort")


def recovery_test():
    p = [1, 2, 3, 4]
    pf = [10, 9, 2, 1]
    o = [5, 6, 3, 4]
    of = [4, 3, 2, 1]
    e_o = [5, 6, 2, 1]
    e_of = [4, 3, 9, 10]
    o, of = recovery(p, pf, o, of, 0.4)
    for i in range(len(o)):
        if o[i] != e_o[i]:
            printErrorMsg("recovery", "offspring not right", e_o, o)
        if of[i] != e_of[i]:
            printErrorMsg("recovery", "offspring fitness not right", e_of, of)
    printSuccessMsg("recovery")


def cal_mutation_prob_test():
    f = [1, 2, 3, 4]
    tmp = np.array(f)
    s = np.sqrt(((tmp - np.mean(tmp)) ** 2).sum() / (tmp.size - 1))
    expect = 0.06 + 0.1 * (5 - s)
    actual = cal_mutation_prob(f)

    if expect != actual:
        printErrorMsg("mutation probability", "not right", expect, actual)

    printSuccessMsg("mutation probability")


def main():
    rws_test()
    cal_select_prob_test()
    cal_fitness_test()
    gcm_test()
    select_test()
    crossover_test()
    mutation_test()
    sort_test()
    recovery_test()
    cal_mutation_prob_test()


filename = input("test data filename: ")
test_data = ""
with open(f"{filename}.in.json") as f:
    test_data = json.load(f)

main()
