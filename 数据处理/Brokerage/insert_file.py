import MySQLdb
from sshtunnel import SSHTunnelForwarder
import xlrd
import time
import os


def mysql_link(de_name):
    """
      连接数据库
      args：db_name（数据库名称）
      returns:db
    """
    try:
        server = SSHTunnelForwarder(
            ("10.29.24.47", 222),  # ssh IP和port
            ssh_password="zts000000",  # ssh 密码
            ssh_username="tianyj",  # ssh账号
            remote_bind_address=("10.29.129.94", 3306),  # 数据库所在的IP和端口
            local_bind_address=('0.0.0.0', 10008)
        )

        server.start()
        # 打印本地端口，已检查是否配置正确
        # print(server.local_bind_port)

        db = MySQLdb.connect(host="127.0.0.1",  # 固定写法
                             port=server.local_bind_port,
                             user="rpa",  # 数据库账号
                             passwd="zts000",  # 数据库密码
                             db=de_name,
                             charset='utf8',
                             connect_timeout=1000)  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
        return db, server
    except:
        print("could not connect to mysql server")


def open_excel(excel_file):
    """
      读取excel函数
      args：excel_file（excel文件，目录在py文件同目录）
      returns：book
    """
    try:
        book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
        # print(sys.getsizeof(book))
        return book
    except:
        print("open excel file failed!")


def generate_sql(table_name, value):
    """
        生成sql语句
        :param table_name:
        :return:
    """
    now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    now_time = '2020-12-29'
    if table_name == 'shenzhen_month':
        sql = "INSERT INTO " + table_name + " (month, total_amount, market_share, stock_trading_amount, " \
                                            "fund_trading_amount, bond_trading_amount, warrants_trading_amount, " \
                                            "`current_time`) SELECT %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and month = '" + \
              value[0] + "')"

    elif table_name == 'sse_month':
        sql = "INSERT INTO " + table_name + "(member_name, number_seats, total, stock, investment_funds," \
                                            "ETF, treasury, amount_lgd, corporate_bonds, convertible_bonds," \
                                            "repurchase_bonds, warrants, current_month, `current_time`) SELECT" \
                                            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and member_name = '" + \
              value[0] + "')"
    elif table_name == 'shenzhen_total_day':
        sql = "INSERT INTO " + table_name + "(types_bond, number, transaction_amount, turnover, total_equity," \
                                            "total_market_value, negotiable_capital, circulation_market_value," \
                                            "`current_time`) SELECT" \
                                            " %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and types_bond = '" + \
              value[0] + "')"
    elif table_name == 'sse_stock_day':
        sql = "INSERT INTO " + table_name + "(single_day_situation, stock, mainboard_A, mainboard_B, ipo," \
                                            "repurchase_bonds, `current_time`) SELECT" \
                                            " %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and stock = '" + \
              value[1] + "')"
    elif table_name == 'sse_fund_day':
        sql = "INSERT INTO " + table_name + "(single_day_situation, fund, closed_fund, ETF, LOF," \
                                            "trading_fund, repurchase_fund, `current_time`) SELECT" \
                                            " %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and fund = '" + \
              value[1] + "')"
    return sql


def store_to(db_name, table_name, excel_file):
    """
      执行插入操作
      args:db_name（数据库名称）
         table_name(表名称）
         excel_file（excel文件名，把文件与py文件放在同一目录下）

    """
    db, server = mysql_link(db_name)  # 打开数据库连接
    try:
        now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        now_time = '2020-12-29'
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        book = open_excel(excel_file)  # 打开excel文件
        sheets = book.sheet_names()  # 获取所有sheet表名
        for sheet in sheets:
            sh = book.sheet_by_name(sheet)  # 打开每一张表
            row_num = sh.nrows
            num = 0  # 用来计数
            flag = 0  # 失败标志
            count = 0  # 控制失败次数
            i = 1
            while i < row_num:
                if flag == 1:
                    pass
                else:
                    count = 0
                if count == 3:  # 失败3次，跳过该行数据
                    i += 1
                    count = 0
                flag = 0
                row_data = sh.row_values(i)  # 按行获取excel的值
                value = []
                if row_data[2] == '':
                    i += 1
                    continue
                for j in range(len(row_data)):
                    ctype = sh.cell(i, j).ctype  # 获取单元格格式
                    # ctype =3,为日期
                    if ctype == 3:
                        date = xlrd.xldate.xldate_as_datetime(row_data[j], 0)
                        cell = date.strftime('%Y-%m-%d')  # ('%Y/%m/%d %H:%M:%S')
                        # print(cell)
                        value.append(cell)
                    else:
                        value.append(row_data[j])
                value.append(now_time)
                value = tuple(value)
                sql = generate_sql(table_name, value)
                # print(sql)
                try:
                    cursor.execute(sql, value)  # 执行sql语句
                    db.commit()  # 提交
                    num += 1
                    i += 1
                except Exception as e:
                    print('写入数据库失败,失败信息：', e)
                    flag = 1
                    count += 1
                    db.close()
                    server.close()
                    db, server = mysql_link(db_name)  # 打开数据库连接
                    db.rollback()
                    cursor = db.cursor()
            # db.commit()  # 提交
            cursor.close()  # 关闭连接
            print("worksheets: " + sheet + " has been inserted " + str(num) + " datas!")
    except Exception as e:
        db.rollback()
        print('写入数据库失败,失败信息：', e)
    finally:
        db.close()
        server.close()


if __name__ == '__main__':
    path_db = {'深交所普通专区市场总貌': 'shenzhen_total_day'
               # '上交所股票成交概况': 'sse_stock_day', '上交所基金成交概况': 'sse_fund_day'
               }

    path = r'D:\0RPA\计划财务部\经纪业务'
    now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    now_time = '20201229'
    path = os.path.join(path, now_time)
    fileList = os.listdir(path)
    for fileName in fileList:
        fileAbsPath = os.path.join(path, fileName)
        if not os.path.isdir(fileAbsPath):
            print('file name:' + fileName)
            base_dir = fileName.split('.')[0]
            # print(base_dir)
            for key, value in path_db.items():
                if key in base_dir:
                    store_to('brokerage', value, fileAbsPath)
    # store_to('credit', 'wind_mmo_month', path)
