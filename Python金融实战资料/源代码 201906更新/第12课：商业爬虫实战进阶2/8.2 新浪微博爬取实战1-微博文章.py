'''Python商业爬虫案例实战第8节：舆情监控实战进阶2 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''8.2节：新浪微博文章爬取实战'''
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def weibo1(company):
    url = 'https://s.weibo.com/article?q=' + company + '&Refer=weibo_article'
    res = requests.get(url, headers=headers, timeout=10).text
    # print(res)

    p_title = '<h3><a href=".*?" target="_blank" title="(.*?)" suda-data'
    p_href = '<h3><a href="(.*?)" target="_blank" title=".*?" suda-data'
    p_date = '<span>.*?</span>.*?<span>(.*?)</span>'
    title = re.findall(p_title, res)
    href = re.findall(p_href, res)
    date = re.findall(p_date, res, re.S)
    # print(title)
    # print(href)
    # print(date)

    import time
    year = time.strftime("%Y")
    today = time.strftime("%Y-%m-%d")
    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        if '年' in date[i]:
            date[i] = date[i]
        else:
            date[i] = year + '-' + date[i]
        date[i] = date[i].split(' ')[0]
        date[i] = re.sub('年', '-', date[i])
        date[i] = re.sub('月', '-', date[i])
        date[i] = re.sub('日', '', date[i])
        if '今天' in date[i]:
            date[i] = today
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

companys = ['华能信托','阿里巴巴','万科集团','百度','腾讯','京东']
for i in companys:
    try:
        weibo1(i)
        print(i + '该公司新浪微博文章爬取成功')
    except:
        print(i + '该公司新浪微博文章爬取失败')

'''获取当前时间'''
# import time
# year = time.strftime("%Y")
# month = time.strftime("%m")
# day = time.strftime("%D")
# print(year)
# print(month)
# print(day)
# today = time.strftime("%Y-%m-%d")
# print(today)