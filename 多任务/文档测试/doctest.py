import doctest
#doctest可以提取注释中的代码执行
#doctest严格按照交互模式的输入格式

def mySum(x, y):
    '''
    add
    :param x:
    :param y:
    :return:

    example:

    >>> print(mySum(1,2))
    3
    '''
    return x + y



doctest.testmod(1+2)










