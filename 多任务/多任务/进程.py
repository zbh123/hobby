'''

对于操作系统而言，一个任务就是一个进程

进程是系统中程序执行和资源分配的基本单元，每个进程都有自己的
数据段、代码段、和堆栈段
multiprocessing库：跨平台版本的多进程模块，提供了一个Process类代表一个进程对象
'''

from multiprocessing import Process
from time import sleep
import os, time, random

#-------------进程----------------
# #子进程执行的代码
# def run(str):
#     while True:
#         #获取当前子进程号os.getpid(),获得当前进程的父进程号os.getppid()
#         print('1111%s....%s....%s'%(str, os.getpid(), os.getppid()))
#         sleep(1.2)
#
# if __name__ == '__name__':
#     print("主进程启动%s"%(os.getpid()))
#     #创建子进程
#     #target说明进程执行的任务
#     p = Process(target=run, args=('11',))
#     #启动进程
#     p.start()
#     while True:
#         print('sunck is a good man')
#         sleep(1)


#-------------父子进程的先后顺序-------------------

# #子进程执行的代码
# def run(str):
#     print('子进程启动')
#     sleep(3)
#     print('子进程结束')
#
# if __name__ == '__name__':
#     print("主进程启动%s"%(os.getpid()))
#     #创建子进程
#     #target说明进程执行的任务
#     p = Process(target=run, args=('11',))
#     #启动进程
#     p.start()
#     #父进程的结束对子进程没影响
#     #让父进程等待子进程结束之后再执行
#     p.join()
#     print('父进程结束')

#-----------------全局变量在多个进程中不能共享----------------

# num = 100
#
# def run():
#     print('子进程开始')
#     global num
#     num += 1
#     print(num)
#     sleep(3)
#     print('子进程结束')
#
#
# if __name__ == '__main__':
#
#     print('父进程开始')
#     p = Process(target=run)
#     p.start()
#     p.join()
#     #在子进程中修改全局变量，对父进程中的全局变量没有影响
#     #在创建子进程时对全局变量做了一个备份，父进程与子进程的全局变量是两个完全不同的变量
#     print('父进程结束--%d'%num)



#-------------启动大量子进程-----------------

# def run(name):
#     print('子进程%d启动--%s'%(name, os.getpid()))
#     start = time.time()
#     sleep(random.choice([1,2,3]))
#     end = time.time()
#     print('子进程%d结束--%s,耗时：%s'%(name, os.getpid(), end-start))
#
#
# if __name__=='__main__':
#     print('父进程启动')
#
#     #创建多个进程
#     #进程池
#     #表示可以同时执行的进程数量,默认是CPU核心数
#     pp =Pool()
#     for i in range(5):
#         #创建进程，放入进程池同意管理
#         pp.apply_async(run, args=(i,))
#     #在调用join之前必须先调用close,调用close之后不能再继续向进程池添加新的进程了
#     pp.close()
#     #等待子进程结束，在继续执行
#     pp.join()
#
#     print('父进程结束')


#---------拷贝文件------------------


def copyFile(rPath, wPath):
    fr = open(rPath, "rb")
    fw = open(wPath, "wb")
    context = fr.read()
    fw.write(context)
    fr.close()
    fw.close()

Path ="D:\\ruanjian\matplot_test\多任务"
toPath = "D:\\ruanjian\matplot_test\多任务1"



if __name__ == '__main__':
    # 读取path文件夹下的所有文件
    fileList = os.listdir(path)
    pp = Pool()
    # 启动文件的拷贝
    start = time.time()
    for fileName in fileList:
        pp.apply_async(copyFile, args=(os.path.join(path, fileName), os.path.join(toPath, fileName)))
    pp.close()
    pp.join()
    end = time.time()
    print('耗时：%s' % (end - start))

