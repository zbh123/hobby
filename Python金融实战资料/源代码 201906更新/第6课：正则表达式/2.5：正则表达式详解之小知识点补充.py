'''2 正则表达式详解 - by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释后运行

'''2.5 正则表达式小知识点补充'''

#1.之前讲过的replace方法
title = ['<em>阿里巴巴</em>电商脱贫成“教材” 累计培训逾万名县域干部']
title[0] = title[0].replace('<em>','')
title[0] = title[0].replace('</em>','')
print(title[0])

#2.新学的sub方法
title = ['<em>阿里巴巴</em>电商脱贫成“教材” 累计培训逾万名县域干部']
title[0] = re.sub('<.*?>', '', title[0])
print(title[0])

#3.新学的sub方法 - 我当初刚学的时候的写法，挺低效的一个写法
title = ['<em>阿里巴巴</em>电商脱贫成“教材” 累计培训逾万名县域干部']
title[0] = re.sub('<em>', '', title[0])
title[0] = re.sub('</em>', '', title[0])
print(title[0])

#4.中括号[]的用法(了解即可，不需深究)
#4.1 中括号[]的用法1 - 在中括号里的内容不再有特殊含义
company = '*华能信托'
company1 = re.sub('[*]','',company)
print(company1)

#4.2 中括号[]的用法2 - 表示某几个的范围
date = '2018年12月12日'
date = re.sub('[年月日]', '-', date)
date = date[:-1]
print(date)

#4.3 其实并不需要用到[]，直接像下面这样写可能更容易理解
date = '2018年12月12日'
date = re.sub('年', '-', date)
date = re.sub('月', '-', date)
date = re.sub('日', '', date)
print(date)
