'''
客户端：
服务端：

'''

import socket

#1、创建socket
#参数1、指定协议  AF_INET或AF_INET6
#指数2、SOCK_STREAM执行使用面向流的TCP协议
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#2、建立连接
#参数为元组，第一个为IP地址，第二个为端口
sk.connect(("www.baidu.com",80))

sk.send(b'GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection:close\r\n\r\n')

#等待接受数据
data = []
while True:
    #每次接受1k数据
    tempData = sk.recv(1024)
    if tempData:
        data.append(tempData)
    else:
        break
dataStr = (b''.join(data)).decode("utf-8")

#断开连接
sk.close()
# print(dataStr)

headers, HTML = dataStr.split('\r\n\r\n',1)
print(headers)
print(HTML)

