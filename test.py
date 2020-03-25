import random
from common import SuccessMsg, ErrorMsg, printList
from GA import rws, generateChromosomeMatrix

# generate chromosome matrix test
def gcm_test():
    c_num = 5
    g_num = 20
    m = generateChromosomeMatrix(c_num, g_num)
    c_set = set()
    for i in range(len(m)):
        c_set.add(str(m[i]))
        g_set = set(m[i])
        if len(g_set) != g_num:
            print(f'{ErrorMsg("[Error gcm]")} output test Error: gene number is not right!\nexpect: {g_num}, actual: {len(g_set)}\nc_num: {c_num}\ng_num: {g_num}\nmatix:')
            printList(m)
            return
    if len(c_set) != c_num:
        print(f'{ErrorMsg("[Error gcm]")} output test Error: chromosome number is not right!\nexpect: {c_num}, actual: {len(c_set)}\nc_num: {c_num}\ng_num: {g_num}\nmatix:')
        printList(m)
        return
    print(f'{SuccessMsg("[Success gcm]")} output test OK')
    

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
    # print(sum(inputData), inputData, outputData)
    if 0 <= outputData < num:
        print(f'{SuccessMsg("[Success rws]")} output test OK')

def main():
    rws_test()
    gcm_test()

main()
    