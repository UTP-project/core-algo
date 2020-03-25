import random
from common import printList, printErrorMsg, printSuccessMsg
from GA import rws, generateChromosomeMatrix, selectChromosome

# generate chromosome matrix test
def gcm_test():
    c_num = 5
    g_num = 20
    m = generateChromosomeMatrix(c_num, g_num)
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

def main():
    rws_test()
    gcm_test()

main()
    