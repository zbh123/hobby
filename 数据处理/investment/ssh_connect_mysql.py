import MySQLdb
from sshtunnel import SSHTunnelForwarder

# with SSHTunnelForwarder(
#         ("10.29.24.47", 222),  # ssh IP和port
#         ssh_password="zts000000",  # ssh 密码
#         ssh_username="tianyj",  # ssh账号
#         remote_bind_address=("10.29.129.94", 3306)) as server:  # 数据库所在的IP和端口
#
#     server.start()
#     # 打印本地端口，已检查是否配置正确
#     print(server.local_bind_port)
#
#     conn = MySQLdb.connect(host="127.0.0.1",  # 固定写法
#                            port=server.local_bind_port,
#                            user="rpa",  # 数据库账号
#                            passwd="zts000",  # 数据库密码
#                            db='investment_banks',
#                            charset='utf8')  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
#
#
#     print('连接成功')
#     cur = conn.cursor()
#     sql = """CREATE TABLE wind_dcm_without_gb (
#              organization CHAR(150) NOT NULL,
#              total_amount CHAR(150),
#              total_ranking CHAR(150),
#              market_share CHAR(150),
#              number CHAR(150),
#              average_amount CHAR(150),
#              remark CHAR(150),
#              amount_npfb CHAR(150),
#              market_share_npfb CHAR(150),
#              number_npfb CHAR(150),
#              amount_ed CHAR(150),
#              market_share_ed CHAR(150),
#              number_ed CHAR(150),
#              amount_cd CHAR(150),
#              market_share_cd CHAR(150),
#              number_cd CHAR(150),
#              amount_stfb CHAR(150),
#              market_share_stfb CHAR(150),
#              number_stfb CHAR(150),
#              amount_mtn CHAR(150),
#              market_share_mtn CHAR(150),
#              number_mtn CHAR(150),
#              amount_ot CHAR(150),
#              market_share_ot CHAR(150),
#              number_ot CHAR(150),
#              amount_iad CHAR(150),
#              market_share_iad CHAR(150),
#              number_iad CHAR(150),
#              amount_gbib CHAR(150),
#              market_share_gbib CHAR(150),
#              number_gbib CHAR(150),
#              amount_abs CHAR(150),
#              market_share_abs CHAR(150),
#              number_abs CHAR(150),
#              amount_exd CHAR(150),
#              market_share_exd CHAR(150),
#              number_exd CHAR(150),
#              amount_other CHAR(150),
#              market_share_other CHAR(150),
#              number_other CHAR(150))"""
#
#     cur.execute(sql)
#     print("CREATE TABLE OK")
#     # 关闭数据库连接
#     cur.close()
#     # 关闭连接
#     conn.close()

import pymysql
import xlrd
import sys

'''
  连接数据库
  args：db_name（数据库名称）
  returns:db

'''


def mysql_link(de_name):
    try:
        db = pymysql.connect(host="172.16.90.95", user="xxx",
                             passwd="xxx",
                             db=xxx,
                             charset='utf8')
        return db
    except:
        print("could not connect to mysql server")


'''
  读取excel函数
  args：excel_file（excel文件，目录在py文件同目录）
  returns：book
'''


def open_excel(excel_file):
    try:
        book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
        print(sys.getsizeof(book))
        return book
    except:
        print("open excel file failed!")


'''
  执行插入操作
  args:db_name（数据库名称）
     table_name(表名称）
     excel_file（excel文件名，把文件与py文件放在同一目录下）

'''


def store_to(db_name, table_name, excel_file):
    db = mysql_link(db_name)  # 打开数据库连接
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

    book = open_excel(excel_file)  # 打开excel文件
    sheets = book.sheet_names()  # 获取所有sheet表名
    for sheet in sheets:
        sh = book.sheet_by_name(sheet)  # 打开每一张表
        row_num = sh.nrows
        print(row_num)
        list = []  # 定义列表用来存放数据
        num = 0  # 用来控制每次插入的数量
        for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
            row_data = sh.row_values(i)  # 按行获取excel的值
            value = (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6], row_data[7], row_data[8], row_data[9], row_data[10], row_data[11], row_data[12],
                     row_data[13], row_data[14])
            list.append(value)  # 将数据暂存在列表
            num += 1
            if (num >= 10000):  # 每一万条数据执行一次插入
                print(sys.getsizeof(list))
                sql = "INSERT INTO " + table_name + " (time, xingbie, afdd, xzb, yzb, cfbj, jjlbmc, \
        bjlbmc, bjlxmc, bjlxxlmc, gxqymc,gxdwmc, afql, afxqxx, cjdwmc)\
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.executemany(sql, list)  # 执行sql语句

                num = 0  # 计数归零
                list.clear()  # 清空list
                print("worksheets: " + sheet + " has been inserted 10000 datas!")

    print("worksheets: " + sheet + " has been inserted " + str(row_num) + " datas!")
    db.commit()  # 提交
    cursor.close()  # 关闭连接
    db.close()

#
# if __name__ == '__main__':
#     store_to('demo', 'demo_yangben', 'xxx.xlsx')


conn = MySQLdb.connect(host="172.16.90.95",  # 固定写法
                           port=3306,
                           user="rpa",  # 数据库账号
                           passwd="zts000",  # 数据库密码
                           db='investment_banks',
                           charset='utf8')  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
