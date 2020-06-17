'''Python商业爬虫案例实战第16讲：舆情预警系统-自动发送邮件 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''16.2 舆情预警系统实战2 - 自动发送附件'''
import smtplib
from email.mime.text import MIMEText
user = '你自己的qq号@qq.com'
pwd = '你自己的SMTP授权码'
to = '你自己设置的收件人邮箱'

while True:
    # 1.连接数据库 提取所有今天的"阿里巴巴"的新闻信息
    import pymysql
    import time
    db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
    company = '阿里巴巴'
    today = time.strftime("%Y-%m-%d")  # 这边采用标准格式的日期格式

    cur = db.cursor()  # 获取会话指针，用来调用SQL语句
    sql = 'SELECT * FROM test WHERE company = %s AND date = %s'  # 编写SQL语句
    cur.execute(sql, (company,today))  # 执行SQL语句
    data = cur.fetchall()  # 提取所有数据，并赋值给data变量
    print(data)
    db.commit()  # 这个其实可以不写，因为没有改变表结构
    cur.close()  # 关闭会话指针
    db.close()  # 关闭数据库链接

    # 2.设置一个可以添加正文和附件的msg
    from email.mime.multipart import MIMEMultipart
    msg = MIMEMultipart()

    # 3.利用从数据库里提取的内容编写邮件正文内容
    mail_msg = []
    mail_msg.append('<p>尊敬的小主，您好，以下是今天的舆情监控报告，望查阅：</p>')
    mail_msg.append('<p><b>一、阿里巴巴舆情报告</b></p>')
    for i in range(len(data)):
        href = '<p><a href="' + data[i][2] + '">' + str(i+1) + '.' + data[i][1] + '</a></p>'
        mail_msg.append(href)

    mail_msg.append('<p>祝好</p>')
    mail_msg.append('<p>华小智</p>')
    mail_msg = '\n'.join(mail_msg)  # 也可以直接写mail_msg = ''.join(mail_msg)，因为上面的<p> </p>已经自动分段落了
    print(mail_msg)

    # 4.先添加正文内容
    msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    # 5.再添加附件，这里的文件名可以有中文，但下面第三行的filename不可以为中文
    att1 = MIMEText(open('D:\\我的文档\\华小智舆情报告.docx', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 下面的filename是在邮件中显示的名字及后缀名, 这边的文件名可以和之前不同，但不可以为中文！！
    att1["Content-Disposition"] = 'attachment; filename="News_Report.docx"'
    msg.attach(att1)

    # 6.设置邮件主题、发件人、收件人
    msg["Subject"] = "华小智舆情监控报告"
    msg["From"] = user
    msg["To"] = to

    # 7.发送邮件
    s = smtplib.SMTP_SSL('smtp.qq.com',465)  # 选择qq邮箱服务，默认端口为465
    s.login(user, pwd)  # 登录qq邮箱
    s.sendmail(user, to, msg.as_string())  # 发送邮件
    s.quit()  # 退出邮箱服务
    print('Success!')

    time.sleep(86400)  # 一天共86400秒
