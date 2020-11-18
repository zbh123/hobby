import os
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
        ("10.29.24.47", 222),  # ssh IP和port
        ssh_password="zts000000",  # ssh 密码
        ssh_username="tianyj",  # ssh账号
        remote_bind_address=("10.29.129.95", 3306),
        local_bind_address=('0.0.0.0', 3306)) as server:  # 数据库所在的IP和端口

    server.start()
    # 打印本地端口，已检查是否配置正确
    print(server.local_bind_port)
    os.system('python manage.py runserver 0:8080')
