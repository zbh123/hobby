'''Python商业爬虫案例实战第14章：数据库基础与实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''14.5节：深度分析-数据清洗及优化'''

import requests
import re
import pymysql
import time

def baidu(company):
    url = 'http://news.baidu.com/ns?word=' + company + '&tn=news&from=news&cl=2&rn=20&ct=0'
    res = requests.get(url).text
    # print(res)

    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    p_info = '<p class="c-author">(.*?)</p>'
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)
    info = re.findall(p_info, res, re.S)

    source = []
    date = []
    for i in range(len(title)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        if '&nbsp;&nbsp;' in info[i]:
            source.append(info[i].split('&nbsp;&nbsp;')[0])
            date.append(info[i].split('&nbsp;&nbsp;')[1])
        else:
            source.append('百度新闻')
            date.append(info[i])
        date[i] = date[i].strip()
        source[i] = source[i].strip()

        # 统一日期格式
        date[i] = date[i].split(' ')[0]
        date[i] = re.sub('年', '-', date[i])
        date[i] = re.sub('月', '-', date[i])
        date[i] = re.sub('日', '', date[i])
        if ('小时' in date[i]) or ('分钟' in date[i]):
            date[i] = time.strftime("%Y-%m-%d")
        else:
            date[i] = date[i]

        # 打印清洗后的数据
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ')')
        print(href[i])

        # 数据导入数据库及数据去重
        db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
        cur = db.cursor()  # 获取会话指针，用来调用SQL语句

        # 1.查询数据为数据去重做准备
        sql_1 = 'SELECT * FROM test WHERE company =%s'
        cur.execute(sql_1, company)
        data_all = cur.fetchall()
        # print(data_all)
        title_all = []
        for j in range(len(data_all)):
            title_all.append(data_all[j][1])

        # 2.判断数据是否在原数据库中，不在的话才进行数据存储
        if title[i] not in title_all:
            sql_2 = 'INSERT INTO test(company,title,href,source,date) VALUES (%s,%s,%s,%s,%s)'  # 编写SQL语句
            cur.execute(sql_2, (company, title[i], href[i], source[i], date[i]))  # 执行SQL语句
            db.commit()  # 当改变表结构后，更新数据表的操作
        cur.close()  # 关闭会话指针
        db.close()  # 关闭数据库链接
    print('------------------------------------')  # 分割符


companys = ['华能信托', '阿里巴巴', '百度集团', '腾讯', '京东']
for company in companys:  # 注意要记得写冒号
    try:
        baidu(company)
        print(company + '数据爬取并导入数据库成功')
    except:
        print(company + '数据爬取并导入数据库失败')

