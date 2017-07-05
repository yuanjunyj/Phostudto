import math


def List2Str(num_list):
    length = len(num_list)
    str_result = ""
    for i in range(length - 1):
        str_result += str(num_list[i])
        str_result += "_"
    str_result += str(num_list[length - 1])
    return str_result


def Str2List(str_origin):
    str_list = str_origin.split("_")
    # print(str_list)
    return [float(x) for x in str_list]
