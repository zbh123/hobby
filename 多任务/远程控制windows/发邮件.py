

import smtplib
from email.mime.text import MIMEText

#smtp服务器
SMTPServer = 'smtp.163.com'
#发邮件的地址
sender = 'baihang_zbh@163.com'
#发送邮箱的密码，授权密码
passwd = '1234567890a'

#设置发送内容
message = 'hhh'
#转换成邮件文本
msg = MIMEText(message)
#标题
msg['Subject'] = 'sjkdf'
#发件者
msg['From'] = sender


#创建SMTP服务器
mailServer = smtplib.SMTP(SMTPServer, 25)
#登录邮箱
mailServer.login(sender, passwd)
#发送邮件
mailServer.sendmail(sender, ['baihang_zbh@163.com'], msg.as_string())
#退出邮箱
mailServer.quit()
