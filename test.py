import random
from common import printList, printErrorMsg, printSuccessMsg
from GA import rws, gen_population, select, crossover, gen_list

# generate chromosome matrix test
def gcm_test():
    c_num = 5
    g_num = 20
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
    num = random.randrange(100)
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
    c_num = random.randrange(100)
    g_num = random.randrange(100)
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
    p_num = random.randrange(100)
    g_num = random.randrange(100)
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

def main():
    rws_test()
    gcm_test()
    select_test()
    crossover_test()

main()
    