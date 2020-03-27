
'''


'''
import re

def checkPhone(str):
    if len(str) != 11:
        return False
    elif str[0] != 1:
        return False
    elif str[1:3] != '30':
        return False
    for i in range(3, 11):
        if str[i] < '0' or str[i]>'9':
            return False
    return True

def checkPhone2(str):
    #正则化是以1开头，以数字结尾
    pat = r"^(1(([34578]\d)|(47))\d{8})"
    res = re.findall(pat, str)
    print(res)


def checkQQ(str):
    re_QQ = re.compile(r'^[1-9]\d{5,9}\d$')
    res = re_QQ.search(str)
    print(res)

def checkMail(str):
    re_Mail = re.compile(r'^[0-9a-zA-Z]\w*[@.][0-9a-zA-Z]{2,3}[.][a-zA-Z]{2,4}')
    res = re_Mail.search(str)
    print res


print(checkPhone2('asfads1234567896125fdhgjyr13569841546sfg'))






