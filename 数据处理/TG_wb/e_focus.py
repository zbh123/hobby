#!python3
# -*- coding:utf-8 -*-

import cx_Oracle
import os, sys
import xlrd, time

os.environ["NLS_LANG"] = ".AL32UTF8"

path = r'D:\0RPA\托管部'
now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
path = os.path.join(path, now_time)

excel_file = os.path.join(path, '管理人录单入库.xls')
if not os.path.exists(path):
    print('没有数据')
    sys.exit(-1)

print(excel_file)


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


try:
    con = cx_Oracle.connect('zhywpt', 'zhywpt', '10.29.185.72:1521/tgwbdb')  # 修改数据库名称-20201204
    cursor = con.cursor()

    book = open_excel(excel_file)  # 打开excel文件
    sh = book.sheet_by_index(0)  # 打开每一张表
    row_num = sh.nrows
    num = 0
    # 选出库里的所有内容，查看插入是否去重
    # cursor.execute("select * from T_RPA_EFOCS_ORDER_INFO")
    # data = cursor.fetchall()
    # print(data)
    # 遍历表格内容
    for i in range(1, row_num):
        row_data = sh.row_values(i)  # 按行获取excel的值
        value = []

        for j in range(len(row_data)):
            value.append(row_data[j].strip())
        print(value)
        # 去重插入数据库
        sql = "insert when (not exists (select 1 from T_RPA_EFOCS_ORDER_INFO where BUSI_DATE='" + value[0] + "' and" \
                                                                                                             " CPDM='" + \
              value[1] + "' and CPMC='" + value[2] + "' and BUSI_TYPE='" + value[3] + "' and APPLY_COUNT=" \
                                                                                      "%d and DEAL_COUNT=%d and DISABLE_COUNT=%d)) then into T_RPA_EFOCS_ORDER_INFO (BUSI_DATE, CPDM, CPMC," \
                                                                                      " BUSI_TYPE, APPLY_COUNT, DEAL_COUNT, DISABLE_COUNT) select '%s', '%s', '%s', " \
                                                                                      "'%s', %d, %d, %d from dual" % (
                  int(value[4]), int(value[5]), int(value[6]),
                  value[0], value[1], value[2], value[3], int(value[4]), int(value[5]), int(value[6]))

        print(sql)
        try:
            cursor.execute(sql)  # 执行sql语句
            num += 1
        except Exception as e:
            print('写入数据库失败,失败信息：', e)
        con.commit()  # 提交
    print("worksheets has been inserted " + str(num) + " datas!")
except Exception as e:
    print('写入数据库失败,失败信息：', e)
finally:
    cursor.close()
    con.close()
