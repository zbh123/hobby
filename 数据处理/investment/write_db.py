import MySQLdb
from sshtunnel import SSHTunnelForwarder
import xlrd
import time
import sys

'''
  连接数据库
  args：db_name（数据库名称）
  returns:db

'''


def mysql_link(de_name):
    try:
        server = SSHTunnelForwarder(
            ("10.29.24.47", 222),  # ssh IP和port
            ssh_password="zts000000",  # ssh 密码
            ssh_username="tianyj",  # ssh账号
            remote_bind_address=("10.29.129.94", 3306))  # 数据库所在的IP和端口

        server.start()
        # 打印本地端口，已检查是否配置正确
        # print(server.local_bind_port)

        db = MySQLdb.connect(host="127.0.0.1",  # 固定写法
                             port=server.local_bind_port,
                             user="rpa",  # 数据库账号
                             passwd="zts000",  # 数据库密码
                             db='investment_banks',
                             charset='utf8')  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
        return db, server
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
        # print(sys.getsizeof(book))
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
    db, server = mysql_link(db_name)  # 打开数据库连接
    try:
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        book = open_excel(excel_file)  # 打开excel文件
        sheets = book.sheet_names()  # 获取所有sheet表名
        for sheet in sheets:
            sh = book.sheet_by_name(sheet)  # 打开每一张表
            row_num = sh.nrows
            # print(row_num)
            num = 0  # 用来控制每次插入的数量
            for i in range(3, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
                row_data = sh.row_values(i)  # 按行获取excel的值
                value = []
                if row_data[2] == '':
                    continue
                for j in range(len(row_data)):
                    value.append(row_data[j])
                value.append(now_time)
                value = tuple(value)
                # print('value:', value, 'len', len(value))
                num += 1

                # sql = "INSERT INTO " + table_name + " (`organization`, total_amount, total_ranking, market_share, `number`," \
                #                                     "average_amount, remark, amount_lgd, market_share_lgd, number_lgd," \
                #                                     "amount_pbd, market_share_pbd, number_pbd, amount_npfb," \
                #                                     "market_share_npfb, number_npfb, amount_ed, market_share_ed, number_ed," \
                #                                     "amount_cd, market_share_cd, number_cd, amount_stfb, market_share_stfb," \
                #                                     "number_stfb, amount_mtn, market_share_mtn, number_mtn, amount_ot, " \
                #                                     "market_share_ot, number_ot, amount_iad, market_share_iad, number_iad," \
                #                                     "amount_gbib, market_share_gbib, number_gbib, amount_abs, " \
                #                                     "market_share_abs, number_abs, amount_exd, market_share_exd, number_exd," \
                #                                     "amount_other, market_share_other, number_other, `current_time`)" \
                #                                     " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                #                                     "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                #                                     " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                sql = "INSERT INTO " + table_name + " (`organization`, total_amount, total_ranking, market_share, `number`," \
                                                    "average_amount, remark, amount_lgd, market_share_lgd, number_lgd," \
                                                    "amount_pbd, market_share_pbd, number_pbd, amount_npfb," \
                                                    "market_share_npfb, number_npfb, amount_ed, market_share_ed, number_ed," \
                                                    "amount_cd, market_share_cd, number_cd, amount_stfb, market_share_stfb," \
                                                    "number_stfb, amount_mtn, market_share_mtn, number_mtn, amount_ot, " \
                                                    "market_share_ot, number_ot, amount_iad, market_share_iad, number_iad," \
                                                    "amount_gbib, market_share_gbib, number_gbib, amount_abs, " \
                                                    "market_share_abs, number_abs, amount_exd, market_share_exd, number_exd," \
                                                    "amount_other, market_share_other, number_other, `current_time`) " \
                                                   "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                                    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                                   " FROM DUAL WHERE NOT EXISTS(SELECT `organization` FROM " + table_name + " WHERE `current_time` = '" + now_time + "')"
                # print(sql)
                cursor.execute(sql, value)  # 执行sql语句
                # if (num >= 10):  # 每100条数据执行一次插入
                #     print(sys.getsizeof(list))
                #     sql = "INSERT INTO " + table_name + " (`organization`, total_amount, total_ranking, market_share, `number`," \
                #                                     "average_amount, remark, amount_lgd, market_share_lgd, number_lgd," \
                #                                     "amount_pbd, market_share_pbd, number_pbd, amount_npfb," \
                #                                     "market_share_npfb, number_npfb, amount_ed, market_share_ed, number_ed," \
                #                                     "amount_cd, market_share_cd, number_cd, amount_stfb, market_share_stfb," \
                #                                     "number_stfb, amount_mtn, market_share_mtn, number_mtn, amount_ot, " \
                #                                     "market_share_ot, number_ot, amount_iad, market_share_iad, number_iad," \
                #                                     "amount_gbib, market_share_gbib, number_gbib, amount_abs, " \
                #                                     "market_share_abs, number_abs, amount_exd, market_share_exd, number_exd," \
                #                                     "amount_other, market_share_other, number_other, `current_time`)" \
                #                                     " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                #                                     "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                #                                     " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                #     cursor.executemany(sql, list)  # 执行sql语句
                #
                #     num = 0  # 计数归零
                #     list.clear()  # 清空list
                #     print("worksheets: " + sheet + " has been inserted 10000 datas!")

            print("worksheets: " + sheet + " has been inserted " + str(num) + " datas!")
            db.commit()  # 提交
            cursor.close()  # 关闭连接
    finally:
        db.close()
        server.close()


if __name__ == '__main__':
    store_to('investment_banks', 'wind_dcm', r'D:\0RPA\计划财务部\投行业务\20200720\债权承销排名(不含可转债).xls')
