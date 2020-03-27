'''设计类
类名：首字母大写
属性：
行为（方法/功能）：
'''

'''
创建类
类：一种数据类型，本身不占内存，实例化的对象（变量），对象占内存
格式：
class 类名（父类列表）
    属性
    行为

'''

# object:基类，超类，所有类的父类
class Person(object):
    #定义属性
    name = ""
    age = 0
    height = 0
    weight = 0
    def __init__(self,name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        print(name,age,height,weight)
    #定义行为(方法)
    def run(self):
        print("run")
    def eat(self, food):
        print("eat " + food)
    def say(self):
        print("Hello, my name is %s, I am %d years old"%(self.name,self.age))
    def openDoor(self):
        print('打开冰箱门')
    def fillEle(self):
        print('load')
    def closeDoor(self):
        print('close')
    def __del__(self):
        '''
        析构函数：
        自动释放对象，释放之后就不能再访问了
        函数内部的定义对象，在函数结束后就自动释放了
        '''
        print('这是析构函数')


'''
实例化对象
格式 对象名 = 类名（参数列表）
'''

# per1 = Person()
# print(per1)
# print(id(per1))
#
# per2 = Person()
# print(per2)
# print(id(per2))
#
# per = Person()

'''
访问属性
格式：对象名.属性名
访问方法
格式：对象名.方法名（参数列表）
'''

# per.name = 'tom'
# per.age = 18
# per.height = 160
# per.weight = 80
# print(per.name,per.age,per.height,per.weight)
#
# per.openDoor()
# per.fillEle()
# per.closeDoor()
# per.eat('apple')

per3 = Person('lili',25,175,50)

per3.say()





class Person(object):
    '''
    __str__()：在调用print的时候自动调用，是给用户用的，是一个描述对象的方法
    __repr__():是给机器用的，在Python解释器里面直接敲对象名，在回车后调用的方法
    '''
    def __init__(self, name, age, height, weight, money):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        # 如果要让类的内部属性不被外部直接访问,就在属性名前面加双下划线
        self.__money = money
    def run(self):
        print(self.__money)
    def __str__(self):
        '''
        优点，自动打印对象的属性，简化实现功能
        :return:
        '''
        return "%s-%d-%d-%d"%(self.name, self.age, self.height, self.weight)

per = Person('hanmeomoe', 20, 175, 50, 10000)
print(per)
# per.money = 0
print(per.run())



