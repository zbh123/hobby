
#给人员编号
people = {}
for i in range(1,31):
    people[i] = i

#设置限制条件
count = 0
index = 1
terminal = 0
#先考虑那些极限和退出情况，
#多出来的31是为了方便控制循环的编号为1的情况

while index <= 31:
    if index == 31:
        index = 1
    elif terminal == 15:
        break
    else:
        if people[index]==0:
            index+=1
            continue
        else:
            count += 1
            if count == 9:
                people[index] = 0
                count = 0
                print('{}号下船'.format(index))
                terminal += 1
            else:
                index+=1
                continue



