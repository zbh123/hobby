
import unittest
from class_test import Person

class Test(unittest.TestCase):
    def test_init(self):
        p =Person('haha', 20)
        self.assertEqual(p.name, 'haha', '属性赋值有误')
    def test_getAge(self):
        p =Person('haha', 20)
        self.assertDictEqual(p.getAge, p.age, 'getAge函数有误')

if __name__ == '__main__':
    unittest.main()



