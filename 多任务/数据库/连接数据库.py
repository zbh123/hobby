import pymysql
#链接数据库
#参数1：mysql服务器IP
#参数2：用户名
#参数3：密码
#参数4要连接的数据库名


db = pymysql.connect('localhost', 'root', 'zzzz', '123456')

#创建cursor对象
cursor = db.cursor()
sql = "select version()"
#bandcard数据库表，如果存在则删除
sql_1 = "drop table if exists bandcard"
cursor.excute(sql)
data = cursor.fetchall()
print(data)






