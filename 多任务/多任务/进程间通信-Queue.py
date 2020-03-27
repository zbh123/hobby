from multiprocessing import Process, Queue
import os,time

def write(q):
    print('启动写子进程%s'%(os.getpid()))
    for chr in ["a","b","c",'d']:
        q.put(chr)
        time.sleep()
    print('结束写子进程%s'%(os.getpid()))



def read(q):
    print('启动读子进程%s'%(os.getpid()))
    while True:
        value = q.get(True)
        print("value="+value)

    print('启动读子进程%s'%(os.getpid()))

if __name__ == '__main__':
    #父进程创建队列
    q = Queue()
    #创建进程
    pw = Process(target=write, args=(q,))

    pr = Process(target=read, args=(q,))

    pw.start()
    pr.start()
    pw.join()
    #pr进程是死循环，只能强制结束
    pr.terminate()
    print('父进程结束')

