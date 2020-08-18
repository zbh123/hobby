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

    sql = "INSERT INTO " + table_name + " (date_close, shang_shen_balance, shang_balance, shen_balance, " \
                                        "finance_balance, purchase_amount_period, repayment_period, " \
                                        "netpurchase_period, short_interest, margin_securities, sales_period, " \
                                        "sales_period_num, repayment_amount, repayment_amount_num, `current_time`) " \
                                        "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"\
                                        " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and date_close = '" + \
              value[0] + "')"

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
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        book = open_excel(excel_file)  # 打开excel文件
        sheets = book.sheet_names()  # 获取所有sheet表名
        for sheet in sheets:
            sh = book.sheet_by_name(sheet)  # 打开每一张表
            row_num = sh.nrows
            num = 0  # 用来计数
            flag = 0  # 失败标志
            count = 0  # 控制失败次数
            i = 2
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
                    ctype = sh.cell(i, j).ctype    # 获取单元格格式
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
    path_db = {'市场交易统计_天': 'wind_mmo_day', '市场交易统计_月': 'wind_mmo_month'}

    path = r'D:\0RPA\计划财务部\信用业务'
    now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    path = os.path.join(path, now_time)
    fileList = os.listdir(path)
    for fileName in fileList:
        fileAbsPath = os.path.join(path, fileName)
        if not os.path.isdir(fileAbsPath):
            print('file name:' + fileName)
            base_dir = fileName.split('.')[0]
            # print(base_dir)
            for key, value in path_db.items():
                if base_dir in key:
                    store_to('credit', value, fileAbsPath)
    # store_to('credit', 'wind_mmo_month', path)
