'''3.1 百度新闻爬虫实战之爬取标题、网址、来源、发布日期等信息 by 王宇韬'''
# 下面有的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释
import requests
import re
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd=阿里巴巴'
res = requests.get(url, headers=headers).text
# print(res)

p_info = '<p class="c-author">(.*?)</p>'
info = re.findall(p_info, res, re.S)
p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
href = re.findall(p_href, res, re.S)
p_title = '<h3 class="c-title">.*?>(.*?)</a>'
title = re.findall(p_title, res, re.S)
# print(info)
# print(len(info))
# print(href)
# print(len(href))
# print(title)
# print(len(title))

source = []
date = []
for i in range(len(title)):
    title[i] = title[i].strip()
    title[i] = re.sub('<.*?>', '', title[i])
    info[i] = re.sub('<.*?>', '', info[i])
    source.append(info[i].split('&nbsp;&nbsp;')[0])
    date.append(info[i].split('&nbsp;&nbsp;')[1])
    date[i] = date[i].strip()
    source[i] = source[i].strip()
    print(str(i+1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
    print(href[i])
