class printColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def SuccessMsg(msg):
    return printColor.OKGREEN + printColor.BOLD + msg + printColor.ENDC

def ErrorMsg(msg):
    return printColor.FAIL + printColor.BOLD + msg + printColor.ENDC


def printList(lst, deep = 2, indent = 2, layer = 0):
    if deep <= 1:
        print(lst)
        return
    prefix = ''.rjust(layer * 2, ' ')
    for i, v in enumerate(lst):
        if deep <= 2:
            print(f'{prefix}{i}: {v}')
        else:
            print(f'{prefix}{i}:')
            printList(lst[i], deep - 1, indent, layer + 1)
