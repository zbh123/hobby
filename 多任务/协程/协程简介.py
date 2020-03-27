'''

子程序/函数:在所有语言中都是底层调用，


看上去是子程序，但是执行过程中，在子程序中可以中断
然后执行另一个子程序，不是函数调用，有点类似CPU中断



'''


def C():
    print("C--start")

    print("C--end")


def B():
    print("B--start")

    C()
    print("B--end")


def A():
    print("A--start")

    B()
    print("A--end")

A()


def D():
    print(1)
    print(2)
    print(3)
    print(4)
def E():
    print('a')
    print('b')
    print('c')
'''
结果：
1
2
a
b
c
3
执行出这种结果
但是A中没有B的调用
看起来执行过程中有点像线程，但是协程的特点在于是一个线程执行
与线程相比，协程的执行效率更高，因为只有一个线程也不存在同时写变量的冲突
在协程中共享资源不加锁，只需要判断状态
'''




