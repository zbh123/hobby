'''Python商业爬虫案例实战第11节：商业爬虫实战进阶3 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''11.3节：上交所公开信息爬取实战'''
from selenium import webdriver
import re
import time

'''上交所'''
def shangjs(company):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    url = 'http://www.sse.com.cn/home/search/?webswd=' + company
    browser.get(url)
    time.sleep(3)#必须要加
    data = browser.page_source
    # print(data)

    p_title = '<dd><a title="(.*?)" href=".*?" target="_blank"><span>.*?</span>'
    p_href = '<dd><a title=".*?" href="(.*?)" target="_blank"><span>.*?</span>'
    p_date = '<dd><a title=".*?" href=".*?" target="_blank"><span>(.*?)</span>'
    title = re.findall(p_title, data)
    href = re.findall(p_href, data)
    date = re.findall(p_date, data)

    for i in range(len(title)):
        href[i] = 'http://www.sse.com.cn/' + href[i]
        print(str(i+1) + '.' + title[i] + ' - '+ date[i])
        print(href[i])

companys = ['华夏幸福','中国石化','中国平安','国元证券']
for i in companys:
    try:
        shangjs(i)
        print(i + '该公司上交所官网爬取成功')
    except:
        print(i + '该公司上交所官网爬取失败')
