import re

'''
re.match函数
原型：(pattern, string ,flags=0)
pattern：匹配的正则表达式
string：要匹配的字符串
flags：标志位，用于控制正则表达式的匹配方式(re.I(忽略大小写),
re.L,re.M（多行匹配，影响^和$）,re.S(.匹配任何字符)
re.U， re.X(使我们以更灵活的方式理解正则表达式))
参数：
功能：尝试从字符串的起始位置匹配一个模式，否则都是失败，返回None
'''


print(re.match("www", 'www.baidu.com'))
print(re.match("www", 'ww.baidu.com'))
print(re.match("www", '.baidu.com.www'))
print(re.match("www", 'wwW.baidu.com',flags=re.I))
print('------------------------------------------')

'''
re.search函数
原型
参数：同上
功能：扫描整个字符串，并返回第一个成功的匹配
'''
print(re.search('good','good good study'))
print('------------------------------------------')
'''
re.findall函数
原型
参数：同上
功能：扫描整个字符串，并返回结果列表
'''
print(re.findall('good','good good study'))

print('------------------------------------------')






