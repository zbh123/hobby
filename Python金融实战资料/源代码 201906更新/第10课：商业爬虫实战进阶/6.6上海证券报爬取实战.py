'''Python商业爬虫案例实战第6节：舆情监控实战进阶1 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''6.6节：上证搜索爬取实战'''
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def szss(company):
    url = 'http://search.cnstock.com/search/result?k=' + company + '&t=0'
    res = requests.get(url, headers=headers, timeout=10).text
    # print(res)

    p_title = '<a href=".*?" target="_blank">(.*?)</a>.*?<span>'
    p_href = '<h3 class="t".*?<a href="(.*?)" target="_blank">.*?</a>.*?<span>'
    p_date = '<span class="g">.*?&nbsp;(.*?)</span>'
    title = re.findall(p_title, res, re.S)
    href = re.findall(p_href, res, re.S)
    date = re.findall(p_date, res)
    # print(title)
    # print(len(title))
    # print(date)
    # print(len(date))
    # print(href)
    # print(len(href))

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[0]
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

companys = ['华能信托','阿里巴巴','万科集团','百度','腾讯','京东']
for i in companys:
    try:
        szss(i)
        print(i + '该公司上证搜索爬取成功')
    except:
        print(i + '该公司上证搜索爬取失败')

