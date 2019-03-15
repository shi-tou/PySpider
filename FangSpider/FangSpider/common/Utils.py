import re

def filter_html(param):
    return ''.join(param.strip())


def str_to_int(param):
    v = re.findall(r"\d+", param)
    if (len(v)) > 0:
        return int(v[0])
    else:
        return 0


def str_to_float(param):
    v = re.findall(r"\d+\.?\d*", param)
    if (len(v)) > 0:
        return float(v[0])
    else:
        return 0.0
