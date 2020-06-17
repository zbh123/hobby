'''Python商业爬虫案例实战第11节：商业爬虫实战进阶3 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''11.6节：华尔街评论爬取实战'''
from selenium import webdriver
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://wallstreetcn.com/news/global')
data = browser.page_source
browser.quit()
# print(data)

p_title = '<a data-v-ab4c239a="" href=".*?" target="_blank" class="title">(.*?)<'
p_href = '<div data-v-ab4c239a="" class="container"><a data-v-ab4c239a="" href="(.*?)" target="_blank" class="title">.*?<'
title = re.findall(p_title, data, re.S)
href = re.findall(p_href, data, re.S)
print(title)
print(len(title))
print(href)
print(len(href))

for i in range(len(title)):
    title[i] = title[i].strip()
    if 'http' in href[i]:
        href[i] = href[i]
    else:
        href[i] = 'https://wallstreetcn.com' + href[i]
    print(str(i + 1) + '.' + title[i])
    print(href[i])

