'''
特点：把数据拼接到请求路径的后面传递给服务器
优点：速度快
缺点：数据小，不安全
'''

import urllib.request
url = "http://www.baidu.com"
response = urllib.request.urlopen(url)
data = response.read()
print(data)











