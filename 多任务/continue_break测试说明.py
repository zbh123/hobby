
'''
continue：说明当循环条件满足时，跳过这个条件，不执行之后的步骤，直接重新开始新的循环
continue：说明当循环条件满足时，不执行之后的步骤，直接退出循环
pass：可以认为没有这个循环条件，对后续步骤没有影响
'''


for i in range(0,5):
    if i == 2:
        continue
    print(i)

for i in range(0,5):
    if i == 3:
        break
    print(i)

for i in range(0,5):
    if i == 3:
        pass
    print(i)











