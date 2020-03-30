import json


class printColor:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class MyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(MyJSONEncoder, self).__init__(*args, **kwargs)
        self.current_indent = 0
        self.current_indent_str = ""

    def encode(self, o):
        # Special Processing for lists
        if isinstance(o, (list, tuple)):
            primitives_only = True
            for item in o:
                if isinstance(item, (list, tuple, dict)):
                    primitives_only = False
                    break
            output = []
            if primitives_only:
                for item in o:
                    output.append(json.dumps(item))
                return "[ " + ", ".join(output) + " ]"
            else:
                self.current_indent += self.indent
                self.current_indent_str = "".join(
                    [" " for x in range(self.current_indent)]
                )
                for item in o:
                    output.append(self.current_indent_str + self.encode(item))
                self.current_indent -= self.indent
                self.current_indent_str = "".join(
                    [" " for x in range(self.current_indent)]
                )
                return "[\n" + ",\n".join(output) + "\n" + self.current_indent_str + "]"
        elif isinstance(o, dict):
            output = []
            self.current_indent += self.indent
            self.current_indent_str = "".join([" " for x in range(self.current_indent)])
            for key, value in o.items():
                output.append(
                    self.current_indent_str
                    + json.dumps(key)
                    + ": "
                    + self.encode(value)
                )
            self.current_indent -= self.indent
            self.current_indent_str = "".join([" " for x in range(self.current_indent)])
            return "{\n" + ",\n".join(output) + "\n" + self.current_indent_str + "}"
        else:
            return json.dumps(o)


def SuccessMsg(msg):
    return printColor.OKGREEN + msg + printColor.ENDC


def ErrorMsg(msg):
    return printColor.FAIL + msg + printColor.ENDC


def WarningMsg(msg):
    return printColor.WARNING + msg + printColor.ENDC


def BoldMsg(msg):
    return printColor.BOLD + msg + printColor.ENDC


def printList(lst, deep=2, indent=2, layer=0, name="", prefix=""):
    if name:
        print(f"{prefix}{name}:")
    if deep <= 1:
        print(lst)
        return
    curPrefix = "".rjust(layer * 2, " ")
    for i, v in enumerate(lst):
        if deep <= 2:
            print(f"{prefix}{curPrefix}{i}: {v}")
        else:
            print(f"{prefix}{curPrefix}{i}:")
            printList(lst[i], deep - 1, indent, layer + 1, prefix=prefix)


def printSuccessMsg(name):
    print(SuccessMsg(BoldMsg(f"[Success {name}] output test OK")))


def printErrorMsg(name, detail, expect, actual, other={}):
    header = f"[Error {name}]"
    prefix = "".rjust(len(header) + 1, " ")
    print(ErrorMsg(BoldMsg(f"{header} {detail}")))
    print(f"{prefix}expect: {SuccessMsg(str(expect))}, actual: {ErrorMsg(str(actual))}")
    for k in other.items():
        print(prefix + "{}: {}".format(*k))
    return prefix


def sort2List(key, val, reverse=False):
    tmp = list(zip(key, val))
    tmp.sort(reverse=reverse)
    unzipped = list(zip(*tmp))
    return list(unzipped[0]), list(unzipped[1])
