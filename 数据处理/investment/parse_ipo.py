import pandas as pd
import os
import time

path1 = r'D:\0RPA\计划财务部\投行业务\20200918\科创板IPO审核申报企业情况.xls'
path2 = r'D:\0RPA\计划财务部\投行业务\20200918\科创板IPO审核申报企业情况_整理.xls'

path = r'D:\0RPA\计划财务部\投行业务'
now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
path = os.path.join(path, now_time)
path1 = os.path.join(path, '科创板IPO审核申报企业情况.xls')
path2 = os.path.join(path, '科创板IPO审核申报企业情况_整理.xls')

if os.path.exists(path2):
    os.remove(path2)

dataframe = pd.read_excel(path1)
status_list = ['报送证监会', '已审核通过', '待上会', '已回复(第三次)', '已回复(第二次)', '已回复', '暂缓表决', '已问询', '已受理']
print(dataframe.shape)


print(dataframe[dataframe.审核状态.isin(status_list)].shape)
data = dataframe[dataframe.审核状态.isin(status_list)]
# for i in range(418)[::-1]:
#     print(dataframe.loc[i]['审核状态'], type(dataframe.loc[i]['审核状态']))
#     if dataframe.loc[i]['审核状态'] not in status_list:
#         print(dataframe.loc[i]['审核状态'].index)
#         dataframe.drop(i)
# print(dataframe.shape)
data.to_excel(path2, index=None)
