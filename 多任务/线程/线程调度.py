import threading, time

#线程调度
cond = threading.Condition()

def run1():
    with cond:
        for i in range(1,10,2):
            print(threading.current_thread().name, i)
            time.sleep(1)
            cond.wait()
            #线程等待，等待run2
            cond.notify()

def run2():
    with cond:
        for i in range(1,10,2):
            print(threading.current_thread().name, i)
            time.sleep(1)
            #run1完成，会等待run2，run2执行完，给run1发消息，让run1运行
            cond.notify()
            cond.wait()

threading.Thread(target=run1).start()
threading.Thread(target=run2).start()



