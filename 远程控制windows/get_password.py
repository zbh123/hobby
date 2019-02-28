'''

全排列

'''

import itertools
import time
#排列
mylist = list(itertools.permutations([1,2,3,4],3))
#组合
mylist = list(itertools.combinations([1,2,3,4],3))
#排列组合
mylist = list(itertools.product([1,2,3,4],repeat=4))

passwd = (''.join(x) for x in itertools.product('0123456789', repeat=5))
while True:
    try:
        time.sleep(0.5)
        str = next(passwd)
        print(str)
    except StopIteration as e:
        break

print(next(passwd))

print(mylist)






