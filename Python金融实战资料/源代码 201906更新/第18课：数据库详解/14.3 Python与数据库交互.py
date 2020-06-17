'''Python商业爬虫案例实战第14章：数据库基础与实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''14.3节：Python与数据库交互'''

'''1.连接数据库并插入数据'''

# 先预定义些变量
company = '阿里巴巴'
title = '测试标题'
href = '测试链接'
source = '测试来源'
date = '测试日期'

# 连接数据库
import pymysql
db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')

# 插入数据
cur = db.cursor()  # 获取会话指针，用来调用SQL语句
sql = 'INSERT INTO test(company,title,href,source,date) VALUES (%s,%s,%s,%s,%s)'  # 编写SQL语句
cur.execute(sql, (company, title, href, source, date))  # 执行SQL语句
db.commit()  # 当改变表结构后，更新数据表的操作
cur.close()  # 关闭会话指针
db.close()  # 关闭数据库链接


'''2.连接数据库并提取数据'''
# 根据1个条件查找并提取
import pymysql
db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')

company = '阿里巴巴'

cur = db.cursor()  # 获取会话指针，用来调用SQL语句
sql = 'SELECT * FROM test WHERE company = %s'  # 编写SQL语句
cur.execute(sql,company)  # 执行SQL语句
data = cur.fetchall()  # 提取所有数据，并赋值给data变量
print(data)
db.commit()  # 这个其实可以不写，因为没有改变表结构
cur.close()  # 关闭会话指针
db.close()  # 关闭数据库链接


# 根据2个条件查找并提取
import pymysql
db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
company = '阿里巴巴'
title = '标题1'

cur = db.cursor()  # 获取会话指针，用来调用SQL语句
sql = 'SELECT * FROM test WHERE company = %s AND title = %s'  # 编写SQL语句
cur.execute(sql, (company, title))  # 执行SQL语句
data = cur.fetchall()  # 提取所有数据，并赋值给data变量
print(data)
db.commit()  # 这个其实可以不写，因为没有改变表结构
cur.close()  # 关闭会话指针
db.close()  # 关闭数据库链接

'''3.连接数据库并删除数据'''
# import pymysql
# db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
#
# company = '阿里巴巴'
#
# cur = db.cursor()  # 获取会话指针，用来调用SQL语句
# sql = 'DELETE FROM test WHERE company = %s'  # 编写SQL语句
# cur.execute(sql, title) # 执行SQL语句
# db.commit()  # 因为改变了表结构，这一行必须要加
# cur.close()  # 关闭会话指针
# db.close()  # 关闭数据库链接