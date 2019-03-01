'''
概念：一种保存数据的格式
作用：可以保存本地的json文件，也可以将json进行数据传输，将json称为轻量级的传输方式
json文件的组成：
{} 代表字典
[] 代表列表
： 代表键值对
， 分隔两个部分
'''

import json

jsonStr = '{"name":"heheh", "gae":18, "hobby":"sleep"}'
print(jsonStr)
#将python数据类型的对象转成json格式的字符串
jsonData = json.loads(jsonStr)
print(jsonData)
print(type(jsonData))
print(jsonData['name'])

#将json格式字符串转成python数据类型的对象
jsonData2 = {'name':'heheh', 'gae':18, 'hobby':'sleep'}

jsonStr2 = json.dumps(jsonData2)
print(jsonStr2)
print(type(jsonStr2))

#读取本地的json文件

path1 = r"******.json"

with open(path1, 'rb') as f:
    data = json.load(f)
    print(data)
    print(type(data))

#写本地json
path2 = r"****.json"
with open(path2,'w') as f:
    json.dump(jsonData2, f)

