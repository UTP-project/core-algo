import random
from GA import rws

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
        print('rws output test OK')

def main():
    rws_test()

main()
    