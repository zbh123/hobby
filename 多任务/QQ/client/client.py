import tkinter
import socket
import threading

ck = None

def getInfo():
    while True:
        data = ck.recv(1024)
        text.insert(tkinter.INSERT, data.decode("utf-8"))


def connectServer():
    ipStr = eip.get()
    port = eport.get()
    user = euser.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipStr, port))
    client.send(user.encode("utf-8"))
    ck = clinet
    t = threading.Thread(target=getInfo)
    t.start()
def sendMail():
    friend = efriend.get()
    sendStr = esend.get()
    sendStr = friend + ':' +sendStr

    ck.send(sendStr.encode("utf-8"))

labelUser = tkinter.Label(win, text='用户名').grid(row=0, column=0)
labelIP = tkinter.Label(win, text='ip').grid(row=1, column=0)
labelPort = tkinter.Label(win, text='port').grid(row=2, column=0)

euser = tkinter.Variable()
eip = tkinter.Variable()
eport = tkinter.Variable()

entryIP = tkinter.Entry(win, textvariable=euser).grid(row=0, column=1)
entryIP = tkinter.Entry(win, textvariable=eip).grid(row=1, column=1)
entryPort = tkinter.Entry(win, textvariable=eport).grid(row=2, column=0)

button1 = tkinter.Button(win, text="连接", command=connectServer).grid(row=3, column=0)
text = tkinter.Text(win, width=30, height=10)
text.grid(row=4, column=0)

esend = tkinter.Variable()
entrySend = tkinter.Entry(win, textvariable=esend).grid(row=5, column=0)

efriend = tkinter.Variable()
entryFriend = tkinter.Entry(win, textvariable=efriend).grid(row=6, column=0)
button2 = tkinter.Button(win, text="发送", command=sendMail).grid(row=6, column=1)

win.mainloop()










