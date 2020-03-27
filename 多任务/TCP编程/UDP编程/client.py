import socket
import time


udpclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    data = input('请输入内容')
    udpclient.sendto(data.encode("utf-8"), ('192.168.132.214',8081))
    data, addr = udpclient.recvfrom(1024)
    print('服务器说：' + data.decode('utf-8'))


