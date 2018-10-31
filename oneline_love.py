print('\n'.join([''.join([('LOVE!'[(x-y) % len('Love')] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 >= 0 else ' ') 
          for x in range(-30, 30)]) for y in range(15, -15, -1)]))#一行画LOVE心形图
          
#分段解析
for y in range(30, -30, -1):
    lis_love = []
    s = 'Love!'
    for x in range(-30, 30):
        if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0:
            i = (x-y)%len(s)
            lis_love.append(s[i])
        else:
            lis_love.append(" ")
    print "".join(lis_love)
