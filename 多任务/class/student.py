from person import Person

class Student(Person):
    def __init__(self, name, age, stuId):
        #调用父类的init
        super(Student, self).__init__(name, age)
        self.stuId = stuId