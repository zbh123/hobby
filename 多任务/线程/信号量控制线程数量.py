import threading,time

#控制线程数量
# sem = threading.Semaphore(2)
#
# def run():
#     with sem:
#         for i in range(10):
#             print("%s--%d"%(threading.current_thread().name, i))
#             time.sleep(1)



##凑够一定数量才能执行
# bar = threading.Barrier(4)
#
# def run():
#
#     print("%s--start"%(threading.current_thread().name))
#     time.sleep(1)
#     bar.wait()
#     print("%s--end" % (threading.current_thread().name))



# if __name__ =='__main__':
#     for i in range(5):
#         threading.Thread(target=run).start()


#-----------------定时线程----------------------


#延时执行
t = threading.Timer(5, run)
t.start()
t.join()




