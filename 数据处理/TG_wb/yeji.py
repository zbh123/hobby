#!python3
# -*- coding:utf-8 -*-
import cx_Oracle


# TA数据库连接读数
# con = cx_Oracle.connect('ta4', 'ta4', '10.29.182.47:1521/tacs1')
# cursor = con.cursor()
# cursor.execute('select t.c_fundcode,t.d_date,t.d_factdate from TUNIPROFITRULE_TMP t')
# data = cursor.fetchall()
# cursor.close()
# con.close()

# 研发数据库操作
# print(data)
con = cx_Oracle.connect('zhywpt', 'zhywpt', '10.32.231.30:1521/tgwbdb2')
cursor = con.cursor()

# cursor.execute('delete from ta_uni_profit_rule_current t')

sql = 'select * from ta_uni_profit_rule_current'
cursor.execute(sql)
data1 = cursor.fetchall()
print(data1)

# for line in data:
#     print(line)
#     sql = "insert into ta_uni_profit_rule_current (fund_code, d_date, d_fact_date) values('%s','%s','%s')" % (line[0],
#                                                                                                               line[1],
#                                                                                                               line[2])
#     print(sql)
#     cursor.execute(sql)
con.commit()
cursor.close()
con.close()
