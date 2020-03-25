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


def printList(lst):
    print('\n'.join('{}: {}'.format(*k) for k in enumerate(lst)))
