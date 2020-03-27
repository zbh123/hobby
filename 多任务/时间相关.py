import time

c = time.time() #时间戳

t = time.gmtime(c) #python元组表示的格林尼治时间
print(t)

#将时间戳转为本地时间
b = time.localtime(c)
print(b)
#将本地时间转为时间戳

m = time.mktime(b)
print(m)

#将时间元组转成字符串

s = time.asctime(b)
print(s)

#将时间戳转成字符串
p = time.ctime(c)
print(p)

#将时间元组转成给定格式的字符串
q = time.strftime("%Y-%m-%d %H:%M:%S",b)
print(q)

#返回当前程序cpu执行时间
#Uix始终返回全部的运行时间
#widows从第二次开始，都是以第一次调用此函数的开始时间戳为计数
y1 = time.process_time()
print(y1)
time.sleep(1)
y2 = time.process_time()
print(y2)

import time

time.clock()
sum = 0

for i in range(10000000):
    sum += i

print(time.clock())


import datetime

"""
datetime


1、datetime
2、timedelta  主要用于计算时间的跨度
3、tzinfo 时区相关
4、time
5、date
"""

d1 = datetime.datetime.now()
print(d1)

#获取指定时间
d2 = datetime.datetime(1999,10,1,1,2,2,123456)
print(d2)

d5 = d1 - d2

#seconds是去除间隔天数以外的秒数
print(d5,d5.days,d5.seconds)

#将时间转为字符串
d3 = d1.strftime("%Y-%m-%d %H:%M:%S")
print(d3)

#将格式化字符串转为datetime对象
#注意：转换的格式要与字符串一致

d4 = datetime.datetime.strptime(d3,"%Y-%m-%d %X")
print(d4)


