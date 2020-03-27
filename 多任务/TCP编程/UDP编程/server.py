


import socket
import time
udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udpServer.bind(('192.168.132.214',8081))


while True:
    data, addr = udpServer.recvfrom(1024)
    print('客户端：', data.decode('utf-8'))
    info = input('输入数据：')
    udpServer.sendto(info.encode('utf-8'), addr)

