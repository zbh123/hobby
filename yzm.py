import random
# 随机数
print(random.random())              # 返回一个随机小数'0.4800545746046827'
print(random.randint(1,5))          # 返回（1-5）随机整型数据
print(random.randrange(1,10))       # 返回（1-10）随机数据

# 生成随机验证码
code = ''
for i in range(4):
    code += str(random.randint(0,9))
    # current = random.randrange(0,4)
    # if current != i:
    #     temp = chr(random.randint(65,90))
    # else:
    #     temp = random.randint(0,9)
    # code += str(temp)
print(code)
