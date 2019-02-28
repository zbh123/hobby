import re

'''
字符串切割

'''

str1 = "good    good study"
print(str1.split())
print(re.split(r' +', str1))

'''
re.finditer函数
(pattern, string ,flags=0)
flags :标志位，用于控制正则表达式匹配方式
功能：扫描整个字符串，返回迭代器
'''

str3 = "good good study, good is nice,good is handsome"
d = re.finditer(r'(good)',str3)
while True:
    try:
        l = next(d)
        print(d)
    except StopIteration as e:
        break
'''
字符串替换和修改
sub(pattern, repl, string, count=0, flags=0)
subn(pattern, repl, string, count=0, flags=0)
pattern:正则表达式
repl：用来替换的字符串
string：目标字符串
count：最多替换次数
功能：在目标字符串中以正则表达式的规则匹配字符串，再把它们替换为指定的字符串
区别：sub返回值类型与原类型相同，subn返回一个元组
'''
str4 = "good good study, good is nice,good is handsome"
# print(re.sub(r'(good)','beauty',str4))
print(re.subn(r'(good)','beauty',str4))
re.subn()

'''
分组：
概念：除了简单的判断是否匹配之外，正则表达式还有提取子串的功能，
用（）表示的就是提取分组，内部的？P<first>是取名字为first
'''
str5 = "010-52364158"
m = re.match(r'(?P<first>\d{3})-(\d{8})',str5)
#使用序号获取对应组的信息，group（0）代表原始字符串
print(m.group(0))
print(m.group(1))
print(m.group('first'))
print(m.group(2))
#查看匹配的各组的情况
print(m.groups())

'''
编译：当我们使用正则表达式时，re模块会干两件事
1、编译正则表达式，如果正则表达式本身不合法，会报错
2、用编译后的正则表达式去匹配对象
compile(pattern, flags=0)
pattern要编译的表达式
'''

pat = r"^(1(([34578]\d)|(47))\d{8})"
re_telephone = re.compile(pat)
#此时re_telephone成为re的对象，可以使用re的所有方法
re_telephone.match('1630222222')



#re模块的调用和对象的调用
# re.match(pattern, str)
# re_telephone.match(str)

# re.reseach(pattern, str)
# re_telephone.reseach(str)

# re.findall(pattern, str)
# re_telephone.findall(str)







