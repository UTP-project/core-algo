import random
import copy
import json
from common import printList, printErrorMsg, printSuccessMsg, sort2List
from GA import rws, gen_population, select, crossover, mutation, cal_fitness, recovery, gen_list, main as ga

# generate chromosome matrix test
def gcm_test():
    g_num = random.randint(10, 100)
    c_num = g_num
    m = gen_population(c_num, g_num)
    c_set = set()
    info = {
        'c_num': c_num,
        'g_num': g_num
    }
    for i in range(len(m)):
        c_set.add(str(m[i]))
        g_set = set(m[i])
        if len(g_set) != g_num:
            indent = printErrorMsg('gcm', 'gene number is not right!', g_num, len(g_set), info)
            printList(m, name='matrix', prefix=indent)
            return
    if len(c_set) != c_num:
        indent = printErrorMsg('gcm', 'chromosome number is not right!', c_num, len(c_set), info)
        printList(m, name='matrix', prefix=indent)
        return
    printSuccessMsg('gcm')

# fitness calculate test
def cal_fitness_test():
    population = gen_population(test_data['g_num'], test_data['g_num'])
    fitness, cost = cal_fitness(population, test_data['dist'], test_data['time_cost'], test_data['route_time'], test_data['play_time'], test_data['time_window'])
    printSuccessMsg('calculate fitness')

# generate rws list
def rws_rand_list(num):
    random.seed()
    res = []
    acc = 0
    for i in range(num):
        res.append(random.random())
        acc += res[i]
    for i in range(num):
        res[i] = res[i] / acc
    return res

# roulette wheel selection test
def rws_test():
    random.seed()
    num = random.randint(10, 100)
    inputData = rws_rand_list(num)
    outputData = rws(inputData)
    info = {
        'inputData': inputData,
        'sum': sum(inputData)
    }
    if 0 <= outputData < num:
        printSuccessMsg('rws')
    else:
        printErrorMsg('rws', 'index out of range', '0 <= output < input', outputData, info)

def select_test():
    random.seed()
    g_num = random.randint(10, 100)
    c_num = g_num
    offspring_p = random.random()
    selection_p = rws_rand_list(c_num)
    m = gen_population(c_num, g_num)
    parents = select(m, offspring_p, selection_p)
    if len(parents) != round(offspring_p * c_num / 2):
        indent = printErrorMsg('select', 'parents number is not right', round(offspring_p * c_num / 2), len(parents))
        printList(parents, 3, name='parents list', prefix=indent)
    printSuccessMsg('select')

def crossover_test():
    random.seed()
    g_num = random.randint(10, 100)
    p_num = g_num
    parentList = []
    for i in range(p_num):
        parentList.append((gen_list(1, g_num + 1), gen_list(1, g_num + 1)))
    offspringList, cuts = crossover(parentList)

    if len(offspringList) != p_num * 2:
        indent = printErrorMsg('cross', 'offspring number is not right', p_num * 2, len(offspringList))
        printList(offspringList, name='offspring list', prefix=indent)

    for i in range(len(parentList)):
        for j in range(*cuts[i]):
            if offspringList[i * 2][j] != parentList[i][1][j]:
                printErrorMsg('cross', f'offspring not match parent on the pos {j}', parentList[i][1][j], offspringList[i * 2][j], { 'cuts': cuts[i], 'parent': parentList[i], 'offspring': (offspringList[i * 2], offspringList[i * 2 + 1]) })
                return
            if offspringList[i * 2 + 1][j] != parentList[i][0][j]:
                printErrorMsg('cross', f'offspring not match parent on the pos {j}', parentList[i][0][j], offspringList[i * 2 + 1][j], { 'cuts': cuts[i], 'parent': parentList[i], 'offspring': (offspringList[i * 2], offspringList[i * 2 + 1]) })
                return
    
    for i in range(len(offspringList)):
        if len(set(offspringList[i])) != g_num:
            printErrorMsg('cross', 'offspring gene number not right or has repeated value', g_num, len(set(offspringList[i])), { "offspring": offspringList[i] })
    
    printSuccessMsg('cross')

def mutation_test():
    random.seed()
    g_num = random.randint(10, 100)
    o_num = g_num
    mutation_prob = random.random()
    offspringList = []
    for i in range(o_num):
        offspringList.append(gen_list(1, g_num + 1))
    o_offspringList = copy.deepcopy(offspringList)

    sp = mutation(offspringList, mutation_prob)

    for i in range(o_num):
        if sp[i]:
            if o_offspringList[i][sp[i][0]] != offspringList[i][sp[i][1]] or o_offspringList[i][sp[i][1]] != offspringList[i][sp[i][0]]:
                expect = o_offspringList[i].copy()
                expect[sp[i][0]], expect[sp[i][1]] = expect[sp[i][1]], expect[sp[i][0]]
                printErrorMsg('mutation', 'swap value is not right', expect, offspringList[i], { 'swap_point': sp[i] })
    
    printSuccessMsg('mutation')

def sort_test():
    key = [3, 2, 4, 1]
    val = ['a', 'b', 'd', 'c']
    key_expect = [1, 2, 3, 4]
    val_expect = ['c', 'b', 'a', 'd']
    output_key, output_val = sort2List(key, val)
    for i in range(len(output_key)):
        if output_key[i] != key_expect[i]:
            printErrorMsg('sort', f'key output not right on pos {i}', key_expect[i], output_key[i], {
                'key': key,
                'expect_key': key_expect,
                'output': output_key
            })
            return
        if output_val[i] != val_expect[i]:
            printErrorMsg('sort', f'val output not right on pos {i}', val_expect[i], output_val[i], {
                'val': val,
                'expect_val': val_expect,
                'output': output_val
            })
            return
    
    output_key, output_val = sort2List(key, val, True)
    key_expect.reverse()
    val_expect.reverse()
    for i in range(len(output_key)):
        if output_key[i] != key_expect[i]:
            printErrorMsg('sort', f'key output not right on pos {i} while reverse', key_expect[i], output_key[i], {
                'key': key,
                'expect_key': key_expect,
                'output': output_key
            })
            return
        if output_val[i] != val_expect[i]:
            printErrorMsg('sort', f'val output not right on pos {i} while reverse', val_expect[i], output_val[i], {
                'val': val,
                'expect_val': val_expect,
                'output': output_val
            })
            return
    printSuccessMsg('sort')

def recovery_test():
    p = [1, 2, 3, 4]
    pf = [10, 9, 2 ,1]
    o = [5, 6, 3, 4]
    of = [4, 3, 2, 1]
    e_o = [5, 6, 2, 1]
    e_of = [4, 3, 9, 10]
    o, of = recovery(p, pf, o, of, 0.4)
    for i in range(len(o)):
        if o[i] != e_o[i]:
            printErrorMsg('recovery', 'offspring not right', e_o, o)
        if of[i] != e_of[i]:
            printErrorMsg('recovery', 'offspring fitness not right', e_of, of)
    printSuccessMsg('recovery')

def final_test():
    print()
    population, fitness = ga(test_data['dist'], test_data['time_cost'], test_data['route_time'], test_data['play_time'], test_data['time_window'], 1, recovery_rate, interation)

def main():
    rws_test()
    cal_fitness_test()
    gcm_test()
    select_test()
    crossover_test()
    mutation_test()
    sort_test()
    recovery_test()
    final_test()


filename = input('test data filename: ')
test_data = ''
with open(f'{filename}.in.json') as f:
    test_data = json.load(f)

recovery_rate = float(input('recovery rate: '))
interation = int(input('interation: '))

main()
    