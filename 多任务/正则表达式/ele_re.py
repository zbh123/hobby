import re


print('------------匹配单个字符与数字------------')
'''
   .          匹配除换行符以外的任意字符
[0123456789],[0-9],\d    表示匹配数字
[good]                     匹配g,o,o,d中的任意字符
[a-z] [A-Z]                任意小写字母
[0-9a-zA-Z]                匹配任意字母、数字
[0-9a-zA-Z_],\w               匹配任意字母、数字和下划线
[^good]                    匹配除了g,o,o,d以外的所有字符
^                          称为脱字符，表示不匹配集合中的字符
[^0-9],\D                匹配所有非数字字符
\W           匹配非数字字母下划线
\s           匹配任意空白符（空格，换行，换页，回车，制表）同[ \f\n\r\t]
\S           匹配任意非空白符
[^, ]*?        匹配任意不是，和空格的字符串
.*?        非贪婪匹配任意字符

'''
print(re.search('\d','good good study 666'))



print('-----------------------锚字符（边界字符）------------------')
'''
^  行首匹配，判断开头
$  行尾匹配
\A  匹配字符串开始，它和^的区别是，\A只匹配整个字符串的开头，即使在re.M模式下也不会匹配它行的行首
\Z  匹配字符串结束，同上
\b 匹配一个单词的边界，单词和空格间的位置
    'er\b'，匹配以给定字母为边界
\B 匹配非单词边界
'''

print(re.findall('^good','good good study\ngood',re.M))
print(re.findall('\Agood','good good study\ngood',re.M))

print(re.search(r'er\b','never'))
print(re.search(r'er\b','nerve'))
print(re.search(r'er\B','never'))
print(re.search(r'er\B','nerve'))



print('------------------匹配多个字符-----------------')

'''
说明：下方的x，y，z均为假设的普通字符，不是正则表达式的元字符
(xyz)   匹配xyz（作为整体去匹配）
x?  匹配0个或1个x
x* 匹配0个或任意多个x
x+ 匹配至少一个x
x{n}  匹配确定的n个x（n是非负整数）
x{n,} 匹配至少n个x
x{n, m} 匹配至少n个，最多m个x
x|y 匹配x或y
'''

print(re.findall(r'good','good good study'))
print(re.findall(r'a?','aaa'))   #非贪婪匹配（尽可能少的匹配）
print(re.findall(r'a*','aaabaa'))   #贪婪匹配（尽可能多的匹配）
print(re.findall(r'a+','aaabaa'))   #至少一个a
print(re.findall(r'a{3}','aaabaa'))
print(re.findall(r'a{3,}','aaabaa'))
print(re.findall(r'a{3,5}','aaabaa'))
print(re.findall(r'((g|G)ood)','Good good study'))

#提取sunck..................man
str = "sunck is a good man? sunck is a nice man"
print(re.findall(r'sunck.*?man', str))   #  *？解决贪婪匹配的问题



print('----------------特殊------------------')
'''
*? +? x?   最小匹配，通常都是尽可能多的匹配，可以使用这种解决贪婪模式

(?:)     类似（xyz），但不表示一个组
'''

#匹配注释

print(re.findall(r"//*.*?/*/", r"/*   part1    */  /*      part2    */"))









