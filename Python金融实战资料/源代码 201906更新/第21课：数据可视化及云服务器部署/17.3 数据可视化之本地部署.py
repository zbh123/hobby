'''Python商业爬虫案例实战第17讲：数据可视化及云端部署实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''17.3 数据可视化之本地部署'''
import requests
import re
import time
import pymysql

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

    score = []
    keywords = ['违约', '诉讼', '兑付', '阿里', '百度', '京东', '互联网']
    for i in range(len(title)):
        num = 0
        try:
            article = requests.get(href[i], timeout=10).text
        except:
            article = '爬取失败'

        try:
            article = article.encode('ISO-8859-1').decode('utf-8')  # 方法3
        except:
            try:
                article = article.encode('ISO-8859-1').decode('gbk')  # 方法2
            except:
                article = article  # 方法1
        p_article = '<p>(.*?)</p>'
        article_main = re.findall(p_article, article)
        article = ''.join(article_main)
        for k in keywords:
            if (k in article) or (k in title[i]):
                num -= 5
        score.append(num)

        # 打印清洗后的数据以及舆情评分版本4获得的评分
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + ' ' + source[i] + ')')
        print(href[i])
        print('该新闻的舆情评分为' + str(score[i]))  # 注意要加str函数把分数转换成字符串

        # 数据导入数据库及数据去重
        db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong3', charset='utf8')
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
            sql_2 = 'INSERT INTO test(company,title,href,source,date,score) VALUES (%s,%s,%s,%s,%s,%s)'  # 编写SQL语句
            cur.execute(sql_2, (company, title[i], href[i], source[i], date[i], str(score[i])))  # 执行SQL语句
            db.commit()  # 当改变表结构后，更新数据表的操作
        cur.close()  # 关闭会话指针
        db.close()  # 关闭数据库链接
    print('------------------------------------')  # 分割符


companys = ['华能信托', '阿里巴巴', '百度集团', '腾讯', '京东', '万科集团']
for company in companys:
    try:
        baidu(company)
        print(company + '爬取并导入数据库成功')
    except:
        print(company + '爬取并导入数据库失败')