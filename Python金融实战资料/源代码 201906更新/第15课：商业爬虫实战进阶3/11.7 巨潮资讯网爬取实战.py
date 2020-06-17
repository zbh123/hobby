'''Python商业爬虫案例实战第11节：商业爬虫实战进阶3 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''11.7节：巨潮资讯网爬取实战'''
from selenium import webdriver
import re

def juchao(keyword):
    browser = webdriver.Chrome()
    url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=' + keyword
    browser.get(url)
    data = browser.page_source
    # print(data)
    browser.quit()

    p_title = '<td class="sub-title"><a href=".*?" target="_blank">(.*?)</td>'
    p_href = '<td class="sub-title"><a href="(.*?)" target="_blank">.*?</td>'
    p_date = '<div class="sub-time-time">(.*?)</div>'
    title = re.findall(p_title, data)
    href = re.findall(p_href, data)
    date = re.findall(p_date, data)

    for i in range(len(title)):
        title[i] = re.sub(r'<.*?>', '', title[i])
        href[i] = 'http://www.cninfo.com.cn' + href[i]
        href[i] = re.sub('amp;', '', href[i])
        date[i] = date[i].split(' ')[0]
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])


keywords = ['理财', '现金管理', '纾困']
for i in keywords:
    juchao(i)

