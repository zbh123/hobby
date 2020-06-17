'''2 正则表达式详解'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释后运行

'''2.1 findall方法'''
import re
content = 'Hello 123 world'
result = re.findall('\d\d\d',content)
print(result)

import re
content = 'Hello 123 world 456 华小智python基础教学135'
result = re.findall('\d\d\d',content)
print(result)

a1 = result[0] #注意列表的一个元素的序号是0
print(a1)
a2 = result[1]
print(a2)
a3 = result[2]
print(a3)

a = type(result[0])
print(a)

for i in result:
    print(i)




