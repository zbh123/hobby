
from functools import reduce
'''
map(fn, lsd):fn是函数，f2是列表
将传入的函数一次作用在序列中的每一个元素，并把结果作为新的Iterator返回
'''

def chr2int(chr):
    return{'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[chr]

list1 = ["1","4","6","9"]
res = map(chr2int, list1)
print(res)
print(list(res))

res = map(str, list1)
print(list(res))

'''
reduce(fn, lsd)，fn是函数，lsd是列表
功能：一个函数作用在序列上，这个函数必须接受两个参数，reduce把结果继续和序列的下一个元素累计运算
'''

#求一个序列的和
list2 = [1,2,3,4,5]

def mySum(x, y):
    return x+y

r = reduce(mySum, list2)
print(r)

def str2int(str):
    def fc(x, y):
        return x*10 + y
    def fs(chr):
        return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[chr]

    return reduce(fc, map(fs, list(str)))

print(str2int('1238546'))



