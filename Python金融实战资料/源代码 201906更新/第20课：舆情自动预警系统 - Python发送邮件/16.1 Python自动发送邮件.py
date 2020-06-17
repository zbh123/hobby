'''Python商业爬虫案例实战第16讲：舆情预警系统-自动发送邮件 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''1.1 QQ邮箱发送'''
import smtplib  # 引入两个控制邮箱发送邮件的库
from email.mime.text import MIMEText

user = '你自己的qq号@qq.com'  # 发件人邮箱
pwd = '你自己的SMTP授权码'  # 邮箱的SMTP密码
to = '你自己设置的收件人邮箱'  # 收件人，可以写多个收件人，用英文逗号隔开

# 1.邮件正文内容
msg = MIMEText('测试邮件正文内容')

# 2.设置邮件主题、发件人、收件人
msg['Subject'] = '测试邮件主题!'  # 邮件的标题
msg['From'] = user  # 设置发件人
msg['To'] = to  # 设置收件人

# 3.发送邮件
s = smtplib.SMTP_SSL('smtp.qq.com',465)  # 选择qq邮箱服务，默认端口为465
s.login(user, pwd)  # 登录qq邮箱
s.send_message(msg)  # 发送邮件
s.quit()  # 退出邮箱服务
print('Success!')


'''1.2 网易163邮箱发送'''
import smtplib
from email.mime.text import MIMEText
user = '你自己的163邮箱@163.com'  # 发件人，这里为163邮箱了
pwd = 'huaxiaozhi123'  # 163邮箱的SMTP授权码
to = '收件人邮箱'  # 收件人，可以写多个收件人，用英文逗号隔开

# 1.邮件正文内容
msg = MIMEText('测试邮件正文内容')

# 2.设置邮件主题、发件人、收件人
msg['Subject'] = '测试邮件主题!'
msg['From'] = user
msg['To'] = to

# 3.发送邮件
s = smtplib.SMTP_SSL('smtp.163.com',465)  # 选择163邮箱服务，默认端口为465
s.login(user, pwd)  # 登录163邮箱
s.send_message(msg)
s.quit()
print('Success!')


'''1.3 发送HTML格式的邮件-可以在文字里嵌入链接'''
import smtplib
from email.mime.text import MIMEText
user = '你自己的qq号@qq.com'
pwd = '你自己的SMTP授权码'
to = '你自己设置的收件人邮箱'

# 1.编写邮件正文内容
mail_msg = '''
<p>这个是一个常规段落</p>
<p><a href="https://www.baidu.com">这是一个包含链接的段落</a></p>
'''
msg = MIMEText(mail_msg, 'html', 'utf-8')

# 2.设置邮件主题、发件人、收件人
msg['Subject'] = '测试邮件主题!'
msg['From'] = user
msg['To'] = to

# 3.发送邮件
s = smtplib.SMTP_SSL('smtp.qq.com',465)  # 选择qq邮箱服务，默认端口为465
s.login(user, pwd) #登录qq邮箱
s.send_message(msg)  # 发送邮件
s.quit()  # 退出邮箱服务
print('Success!')


'''1.4 发送邮件附件'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
user = '你自己的qq号@qq.com'
pwd = '你自己的SMTP授权码'
to = '你自己设置的收件人邮箱'

# 1.设置一个可以添加正文和附件的msg
msg = MIMEMultipart()

# 2.先添加正文内容，设置HTML格式的邮件正文内容
mail_msg = '''
<p>这个是一个常规段落</p>
<p><a href="https://www.baidu.com">这是一个包含链接的段落</a></p>
'''
msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

# 3.再添加附件，这里的文件名可以有中文，但下面第三行的filename不可以为中文
att1 = MIMEText(open('E:\\test.docx', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 下面的filename是在邮件中显示的名字及后缀名, 这边的文件名可以和之前不同，但不可以为中文！！
att1["Content-Disposition"] = 'attachment; filename="test.docx"'
msg.attach(att1)

# 4.设置邮件主题、发件人、收件人
msg['Subject'] = '测试邮件主题!'
msg['From'] = user
msg['To'] = to

# 5.发送邮件
s = smtplib.SMTP_SSL('smtp.qq.com',465)
s.login(user, pwd)
s.send_message(msg)  # 直接用s.send_message(msg)更方便
s.quit()
print('Success!')
