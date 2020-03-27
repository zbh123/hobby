import tkinter

win = tkinter.TK()
win.title('QQ服务器')
win.geometry("400x400+200+20")

users = {}

def run(ck, ca):
    userName = ck.recv(1024)
    users[userName.decode("utf-8")] = ck


    while True:
        rData = ck.recv(1024)
        dataStr = rData.decode("utf-8")
        infolist = dataStr.split(":")
        users[infolist[0]].send((userName.decode("utf-8") + ":" + infolist[1]).encode("utf-8"))
    printStr = userName + "连接"
    text.insert(tkinter.END, str)


    print('客户端说：' + str(ck) + data.decode("utf-8"))
    info = input('请输入给服务器端的回复：')
    clientSocket.send(info.encode("utf-8"))

def start():
    ipStr = eip.get()
    port = eport.get()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ipStr, port))
    server.listen(5)
    printStr = "服务器启动成功"
    text.insert(tkinter.INSERT, printStr)
    while True:
        # 等待连接
        clientSocket, clientAddress = server.accept()
        # print("连接成功。。。。。。。")
        t = thrading.Thread(target=run, args=(clientSocket, clientAddress))
        t.start()



def startServer():
    s = threading.Thread(target = start)
    ipStr = eip.get()
    port = eport.get()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ipStr, port))
    server.listen(5)
    while True:
        # 等待连接
        clientSocket, clientAddress = server.accept()
        # print("连接成功。。。。。。。")
        t = thrading.Thread(target=run, args=(clientSocket, clientAddress))
        t.start()
labelIP = tkinter.Label(win, text='ip').grid(row=0, column=0)
labelPort = tkinter.Label(win, text='port').grid(row=1, column=0)
eip = tkinter.Variable()
eport = tkinter.Variable()
entryIP = tkinter.Entry(win, textvariable=eip).grid(row=1, column=1)
entryPort = tkinter.Entry(win, textvariable=eport).grid(row=2, column=0)
button = tkinter.Button(win, text="启动", command=startServer).pack()
text = tkinter.Text(win, width=30, height=10)
text.grid(row=3, column=0)










win.mainloop()
