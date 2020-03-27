import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.132.214',8081))

count = 0
while True:
    data = input('输入数据：')
    # client.send(data.decode("utf-8"))
    client.send(data.encode("utf-8"))
    info = client.recv(1024)
    print('服务器返回信息：', info.decode('utf-8'))
    count += 1













