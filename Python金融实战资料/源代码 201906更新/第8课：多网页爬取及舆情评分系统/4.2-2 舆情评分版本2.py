'''4.2-2 舆情评分系统版本2 by 王宇韬'''
import requests
import re
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company  # 其中rtt参数是关键，rtt=4则是按时间顺序爬取，rtt=1为按焦点排序
    res = requests.get(url, headers=headers).text
    # print(res)

    # 正则编写
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)

    # 舆情评分
    score = []
    keywords = ['违约', '诉讼', '兑付', '阿里', '百度', '腾讯', '京东']
    for i in range(len(title)):
        num = 0
        try:
            article = requests.get(href[i], headers=headers).text
        except:
            article = '爬取失败'

        for k in keywords:
            if (k in article) or (k in title[i]):
                num -= 5  # 就是num = num -5
        score.append(num)

    # 数据清洗及打印输出
    for i in range(len(title)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        title[i] = re.sub('&quot;', '', title[i])
        print(str(i + 1) + '.' + title[i])
        print('舆情评分为' + str(score[i]))  # 这边千万注意加str转换一下
        print(href[i])
    print('——————————————————————————————')  # 这个是当分隔符使用


companys = ['阿里巴巴', '万科集团', '百度', '腾讯', '京东']
for i in companys:
    try:
        baidu(i)
        print(i + '该公司百度新闻爬取成功')
    except:
        print(i + '该公司百度新闻爬取失败')