#!python3
# -*- coding:utf-8 -*-

import cx_Oracle
import os, sys
import xlrd, time

os.environ["NLS_LANG"] = ".AL32UTF8"

path = r'D:\0RPA\合规部\监管案例'
now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
path = os.path.join(path, now_time)

excel_file = os.path.join(path, '监管案例.xls')
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
    con = cx_Oracle.connect('smp_em_ql', 'smp_em_ql', '10.29.182.15:1521/orcl')  # 修改数据库名称-20201204
    cursor = con.cursor()

    book = open_excel(excel_file)  # 打开excel文件
    sh = book.sheet_by_index(0)  # 打开第一张表
    row_num = sh.nrows
    num = 0

    # 遍历表格内容
    for i in range(1, row_num):
        row_data = sh.row_values(i)  # 按行获取excel的值
        value = []
        value.append(i + 8)
        for j in range(len(row_data)):
            value.append(row_data[j].strip())
        print(value)
        # sql = "insert when (not exists (select 1 from HG_JGAL_JGJGAL t1 where t1.BT='{2}'" \
        #       " and t1.FWRQ=to_date('{3}', 'yyyy-MM-dd') and t1.XQDZ='{4}')) then into HG_JGAL_JGJGAL " \
        #       "(ID, FWJG, BT, FWRQ, XQDZ) select {0}, {1}, '{2}', to_date('{3}', 'yyyy-MM-dd'), " \
        #       "'{4}' from dual".format(int(value[0]), int(value[1]),
        #                     value[2], value[3].replace('年', '-').replace('月', '-').replace('日', ''), value[4])
        sql = "merge into HG_JGAL_JGJGAL t1 using dual t2 on (t1.FWJG = {1} and t1.BT = '{2}' " \
              "and t1.XQDZ = '{4}') when not matched then insert (ID, FWJG, BT, FWRQ, XQDZ) " \
              "values ({0}, {1}, '{2}', to_date('{3}', 'yyyy-MM-dd'), '{4}')".format(int(value[0]), int(value[1]),
                            value[2], value[3].replace('年', '-').replace('月', '-').replace('日', ''), value[4])

        # sql = "insert into HG_JGAL_JGJGAL (ID, FWJG, BT, FWRQ, XQDZ) values (%d, %d," \
        #       " '%s', to_date('%s', 'yyyy-MM-dd'), '%s')" % (int(value[0]), int(value[1]), value[2], value[3].replace('年', '-').replace('月', '-').replace('日', ''), value[4])

        print(sql)
        try:
            cursor.execute(sql)  # 执行sql语句
            num += 1
            print(num)
        except Exception as e:
            print('写入数据库失败,失败信息：', e)
        con.commit()  # 提交
    print("worksheets has been inserted " + str(num) + " datas!")
except Exception as e:
    print('写入数据库失败,失败信息：', e)
finally:
    cursor.close()
    con.close()
    # pass
