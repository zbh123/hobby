'''
TCP:是建立可靠的连接，并且通信双方都可以以流的形式发送数据，相对于TCP，UDP则是面向无连接的协议


UDP：不需要建立链接，只需要知道对方IP地址和端口号，就可以直接发送数据包，但是不保证能否到达

虽然UDP传输数据不可靠，但是速度快
'''

import socket
import time
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.connect(('192.168.132.214',8081))

str = b"1_1bt4_10#32499#002481627512#0#0#0:1289671407:a:b:288:hahah"
while True:
    client.sendto(str,('192.168.132.214',8081))
    time.sleep(1)


