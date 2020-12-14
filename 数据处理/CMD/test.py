import pandas as pd
import time
import os

path = r'D:\0RPA\合规部\IP地址监控'
now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
path = os.path.join(path, now_time)
if not os.path.exists(path):
    os.mkdir(path)
file = os.path.join(path, 'IP地址监控.xls')
# 读取数据
df = pd.read_excel(file)
for index, line in enumerate(df['ip']):
    print(line)
    if '/' in line:
        df = df.append({'lib': 0, 'qty1': 0, 'qty2': 0}, ignore_index=True)
# # 将一列炸裂成多列
# df[["类型1", "类型2", "类型3"]] = df["ip"].str.split(".", expand=True)
# # 选取想要的列
# df_final = df[["电影名", "类型1", "类型2", "类型3"]]
# # 将行转列
# df_final = df_final.melt(id_vars=["电影名"], value_name="类型")
# # 对“电影名”字段进行排序
# df_final = df_final[["电影名", "类型"]]
# df_final.sort_values(by="电影名", inplace=True)
# # 删除“类型==None”的行
# for index, value in enumerate(df_final["类型"]):
#     if value == None:
#         df_final.drop(df_final.index[index], inplace=True)


