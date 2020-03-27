
'''
Python 对协程的支持是通过generator实现的

'''

def run():
    #空变量，存储的作用data始终为空
    data = ""
    r = yield data
    print(1, r, data)
    r = yield data
    print(2, r, data)
    r = yield data
    print(3, r, data)
    r = yield data

#协程最简单的风格，控制函数的阶段执行 ，节约线程或者进程的切换
#返回值是一个生成器
m = run()
#启动m
print(m.send(None))
print(m.send("a"))
# print(next(m))
# print(next(m))
# print(next(m))
