'''Python商业爬虫案例实战第14章：数据库基础与实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''14.4节：实战！把舆情监控数据导入到数据库中'''

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
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
        print(href[i])
    print('——————————————————————————————')  # 这个是当分隔符使用

    # 数据导入数据库
    for i in range(len(title)):
        import pymysql
        db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')

        # 插入数据
        cur = db.cursor()  # 获取会话指针，用来调用SQL语句
        sql = 'INSERT INTO test(company,title,href,source,date) VALUES (%s,%s,%s,%s,%s)'  # 编写SQL语句
        cur.execute(sql, (company, title[i], href[i], source[i], date[i]))  # 执行SQL语句
        db.commit()  # 当改变表结构后，更新数据表的操作
        cur.close()  # 关闭会话指针
        db.close()  # 关闭数据库链接


baidu('阿里巴巴')

