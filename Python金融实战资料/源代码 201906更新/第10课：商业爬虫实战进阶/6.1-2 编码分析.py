# =============================================================================
# 5.3 舆情评分系统搭建 by 王宇韬
# =============================================================================

import requests  # 首先导入requests库和正则表达式re库
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

'''编码知识1 - 查看Python获得的数据编码及数据的原始编码'''
# 查看Python获得的数据编码
import requests
url = 'https://www.baidu.com'
code = requests.get(url).encoding
print(code)

# 数据转码
res = requests.get(url).text
# res = requests.get(url, headers=headers).text  # 加上headers显示的内容更多一些
res = res.encode('ISO-8859-1').decode('utf-8')
print(res)

# encode编码与decode解码
res = '华小智'  # 中文字符串
res = res.encode('utf-8')  # encode编码将中文字符串转为二进制
print(res)

res = b'\xe5\x8d\x8e\xe5\xb0\x8f\xe6\x99\xba'  # 二进制字符
res = res.decode('utf-8')  # decode解码将二进制字符转为字符串
print(res)


'''编码知识2 - 万金油方法'''
import requests
url = 'https://www.baidu.com'
res = requests.get(url).text
# res = requests.get(url, headers=headers).text  # 加上headers显示的内容更多一些
try:
    res = res.encode('ISO-8859-1').decode('utf-8')  # 方法3
except:
    try:
        res = res.encode('ISO-8859-1').decode('gbk')  # 方法2
    except:
        res = res  # 方法1
print(res)
