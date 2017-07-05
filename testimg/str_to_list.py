# -*- coding: utf-8 -*-

def add_str(inputStr, add_str):
    #add str to inputStr
    if inputStr == '':
        return(add_str)
    if add_str == '':
        return inputStr
    strlists = inputStr.split(',')
    if add_str not in strlists:
        strlists.append(add_str)
    res_str = ','.join(strlists)
   # print(res_str)
    return res_str

def delete_str(inputStr, delete_str):
    #delete delete_str from inputStr
    if inputStr == '':
        return ''
    strlists = inputStr.split(',')
    if delete_str in strlists:
        strlists.remove(delete_str)
    res_str = ','.join(strlists)
   # print(res_str)
    return res_str

def decode_str(inputStr):
    #str to list
    if inputStr == '':
        return []
    strlists = inputStr.split(',')
    return strlists

def encode_str(like_list):
    #list to str
    if not like_list:
        return ''
    like_str = ','.join(map(str, like_list))
    return like_str
