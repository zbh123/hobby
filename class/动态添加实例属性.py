class Animal(object):
    def __init__(self, name):
        self.name = name
    def eat(self):
        print(self.name + '吃')

class Cat(Animal):
    def __init__(self, name):
        super(Cat, self).__init__(name)
    # def eat(self):
    #     print(self.name + '吃')

class Mouse(Animal):
    def __init__(self, name):
        super(Mouse, self).__init__(name)
    # def eat(self):
    #     print(self.name + '吃')

class Person(object):
    # def __init__(self):
    #     self.name = name
    def feedAnimal(self, animal):
        print('food')
        animal.eat()
    def feedMouse(self, mouse):
        print('food')
        dog.eat()

tom = Cat('tom')
#
# jerry = Mouse('jerry')
#
# tom.eat()
# jerry.eat()

per = Person()
per.feedAnimal(tom)




###动态添加属性和方法
from types import MethodType

class Idel(object):

    #限制动态添加属性的方法，现在只能添加name，age属性
    __slots__ = ('name', 'age')

def say(self):
    print('my name is ' + self.name)

id = Idel()
#动态添加属性
id.name = 'tom'
#动态添加方法
id.speak = MethodType(say, id)
id.speak()

class Person(object):
    def __init__(self, age):
        #属性直接对外暴露
        self.__age = age

    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        if age < 0:
            age = 0
        self.__age = age

per = Person(18)
per.age = 20
print(per.age)