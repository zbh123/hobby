import telnetlib

def telnetDoSomething(IP, user, password, command):
    try:
        # 连接服务器
        telnet = telnetlib.Telnet(IP)
        # 设置调试级别
        telnet.set_debuglevel(2)

        # 读取信息
        rt = telnet.read_until('Login username:'.encode('utf-8'))
        # 写入用户名
        telnet.write(user + "\r\n").encode('utf-8')

        # 读取信息
        rt = telnet.read_until('Login password:'.encode('utf-8'))
        # 写入密码
        telnet.write(password + "\r\n").encode('utf-8')

        # 读取信息
        rt = telnet.read_until('Domain name:'.encode('utf-8'))
        # 写入IP
        telnet.write(IP + "\r\n").encode('utf-8')

        # 读取信息
        rt = telnet.read_until('>'.encode('utf-8'))
        # 写入指令
        telnet.write(command + "\r\n").encode('utf-8')

        # 上面命令执行成功，会继续>
        rt = telnet.read_until('>'.encode('utf-8'))

        telnet.close()
        return True
    except:
        return False



if __name__ == '__main__':
    IP = '10.0.142.197'
    user = 'shdfhj'
    password = '110'
    command = 'tasklist'
    telnetDoSomething(IP, user, password, command)



