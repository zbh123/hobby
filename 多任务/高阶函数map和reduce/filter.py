

'''
filter（fn，lsd）fn是函数，lsd是序列
功能：用于过滤
'''

list1 = [1,2,3,4,5,6,7,8,9]

def func(num):
    if num % 2 ==0:
        return True
    return False

l = filter(func, list1)
print(list(l))

data = [['name','age','hooby'],['tom',25,'none'],['hana',26,'money']]

def func2(v):
    v = str(v)
    if v == 'none':
        return False
    return True

for line in data:
    m = filter(func2, line)
    print(list(m))