
import unittest
from element_test import mySum
from element_test import mySub


class Test(unittest.TestCase):
    def setUp(self):
        print('Start test')
    def tearDown(self):
        print('Test end')

    #测试mySum
    def test_mySum(self):
        self.assertEqual(mySum(1,2),3,'加法有误')
    def test_mySub(self):
        self.assertEqual(mySub(1,2),-1,'减法有误')

if __name__ == '__main__':

    unittest.main()



