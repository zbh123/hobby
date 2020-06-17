'''Python商业爬虫案例实战后续 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''后续1：Tushare调取股票历史数据'''
# 调用一段时间时间内的万科股票数据
import tushare as ts
wanke = ts.get_k_data('000002', start='2016-01-01', end='2019-01-31')
print(wanke)

# 调用60分钟级别的万科股票数据
import tushare as ts
data = ts.get_k_data('000002', ktype='60')
print(data)

# 调用大盘指数信息
import tushare as ts
data2 = ts.get_index()
print(data2)

