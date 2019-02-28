'''
排序：冒泡，选择  快速，插入，计数器
sorted 排序,默认升序

'''


#普通排序
list1 = [6,5,4,1,3,1]
list2 = sorted(list1)
print(list1)
print(list2)

#按绝对值大小排序
list3 = [6,-5,4,-1,3,1]
list4 = sorted(list3, key=abs)
print(list3)
print(list4)

#降序
list5 = [6,5,4,1,3,1]
list6 = sorted(list5, reverse=True)
print(list5)
print(list6)

#字母排序，按长度排序
list7 = ['a','c','h','b']

def myLen(str):
    return len(str)

list8 = sorted(list7, key=myLen)
print(list7)
print(list8)



