'''4.2-1 舆情评分系统版本1 by 王宇韬'''
import requests
import re
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company  # 其中rtt参数是关键，rtt=4则是按时间顺序爬取，rtt=1为按焦点排序
    res = requests.get(url, headers=headers).text
    # print(res)

    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)

    score = []
    keywords = ['违约', '诉讼', '兑付', '阿里', '百度', '京东', '互联网']
    for i in range(len(title)):
        num = 0
        article = requests.get(href[i], headers=headers).text
        for k in keywords:
            if (k in article) or (k in title[i]):
                num -= 5
        score.append(num)

    for i in range(len(title)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        print(str(i + 1) + '.' + title[i])
        print('舆情评分为' + str(score[i]))
        print(href[i])
    print('——————————————————————————————')  # 这个是当分隔符使用

companys = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companys:
    try:
        baidu(i)
        print(i + '该公司百度新闻爬取成功')
    except:
        print(i + '该公司百度新闻爬取失败')