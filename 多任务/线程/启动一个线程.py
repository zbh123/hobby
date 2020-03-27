import threading
import time


#------------启动一个线程------------------------
# def run(num):
#     print('子线程（%s）开始'%(threading.current_thread().name))
#     time.sleep(2)
#     print('打印')
#     time.sleep(2)
#     print('子线程（%s）结束' % (threading.current_thread().name))
#
# if __name__ == '__main__':
#     #任何进程默认就会启动一个线程，成为主进程，主线程可以启动新的子线程
#     print('主线程（%s）启动'%(threading.current_thread().name))
#
#     #创建子线程
#     t = threading.Thread(target= run, name='runThread', args = (1,))
#     t.start()
#     t.join()
#     print('主线程（%s）结束'%(threading.current_thread().name))

#-------------------线程间共享数据-------------------------
'''
线程和进程最大的不同在于，进程中的变量不共享
线程之间所有变量都由所有线程共享，因此线程之间共享数据最大的
危险在于多线程同时修改一个变量，容易把内容改乱了
'''

# num = 100
# def run(n):
#     global num
#     for i in range(10000):
#         num = num + n
#         num = num - n
#
# if __name__=='__main__':
#     t1 = threading.Thread(target=run, args=(6,))
#     t2 = threading.Thread(target=run, args=(9,))
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#     print('num=' + num)

#-------------线程锁解决数据混乱------------------------
#锁对象
# lock = threading.Lock()
#
# num = 100
# def run(n):
#     global num
#     #加锁
#     # lock.acquire()
#     # try:
#     #     for i in range(10000):
#     #         num = num + n
#     #         num = num - n
#     # except:
#     #     pass
#     # lock.release()
#
#     #功能同上，减少死锁的可能
#     with lock:
#         for i in range(10000):
#             num = num + n
#             num = num - n
#
# if __name__=='__main__':
#     t1 = threading.Thread(target=run, args=(6,))
#     t2 = threading.Thread(target=run, args=(9,))
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#     print('num=' + num)

#----------------threadLocal---------------------------

'''
作用，为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用
到的处理函数都可以非常方便的访问这些资源
'''

num = 0
#创建一个全局的ThreadLocal对象
#让每个线程有独立的存储空间
#每个线程对ThreadLocal都可以读写，但互不影响
lock = threading.Lock()

def run(x, n):

    x = x + n
    x = x - n

def func(n):
    #每个线程都有local.x，就是线程的局部变量
    local.x = num
    for i in range(100000000):
        run(loacl.x, n)
    print("%s--%d"%(threading.current_thread().name, local.x))

if __name__ == '__main__':
    t1 = threading.Thread(target=run, args=(6,))
    t2 = threading.Thread(target=run, args=(9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('num=' + num)






