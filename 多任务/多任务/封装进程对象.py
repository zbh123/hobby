from Zbh进程二次封装 import ZbhProcess

if __name__ == '__main__':

    print('父进程启动')

    p = ZbhProcess('zbh')

    p.start()
    p.join()
    print('父进程结束')


