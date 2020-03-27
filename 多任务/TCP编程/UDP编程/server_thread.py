
import socket
import threading
'''
传输数据时要encode编码，接受到的数据要decode解码
'''

#创建socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定IP端口
server.bind(('192.168.132.214',8081))
#监听
server.listen(5)
print("服务器启动成功。。。。。。。")

def run(ck):
    data = ck.recv(1024)
    print('客户端说：' + str(ck) + data.decode("utf-8"))
    info = input('请输入给服务器端的回复：')
    clientSocket.send(info.encode("utf-8"))


while True:
    # 等待连接
    clientSocket, clientAddress = server.accept()
    # print("连接成功。。。。。。。")
    t = thrading.Thread(target=run, args=(clientSocket,))
    t.start()




