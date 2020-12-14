# python3

import cx_Oracle
import os
import time

path = r'D:\0RPA\托管部'
now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
path = os.path.join(path, now_time)
if not os.path.exists(path):
    os.mkdir(path)
path = os.path.join(path, 'R盘数据库.txt')
print(path)

con = cx_Oracle.connect('ta4', 'ta4', '10.29.182.47:1521/TACS1')
cursor = con.cursor()
cursor.execute(
    "select t.c_agencyno  from tagencyinfo t where t.C_AGENCYTYPE = '1' and t.c_agencyno not in ('001', '660', '301', '303', '007', '502', '346', '674', '348', '653', '326', '368', '393', '525') and t.C_AGENCYSTATUS = 'N'")
data = cursor.fetchall()
print(data)
for i in data:
    print(i[0])

with open(path, 'w') as fp:
    for index in data:
        fp.write(index[0])
        fp.write('\n')

cursor.close()
con.close()
