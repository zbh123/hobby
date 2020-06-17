'''Python商业爬虫案例实战第11节：商业爬虫实战进阶3 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''11.2节：东方财富网信息爬取实战'''
from selenium import webdriver
import re

def dongfang(company):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    url = 'http://so.eastmoney.com/news/s?keyword=' + company
    browser.get(url)
    data = browser.page_source
    browser.quit()
    # print(data)

    p_title = '<div class="news-item"><h3><a href=".*?">(.*?)</a>'
    p_href = '<div class="news-item"><h3><a href="(.*?)">.*?</a>'
    p_date = '<p class="news-desc">(.*?)</p>'
    title = re.findall(p_title,data)
    href = re.findall(p_href,data)
    date = re.findall(p_date,data,re.S)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[0]
        print(str(i+1) + '.' + title[i] + ' - '+ date[i])
        print(href[i])

companys = ['华能信托','阿里巴巴','腾讯','京东']
for i in companys:
    try:
        dongfang(i)
        print(i + '该公司东方财富网爬取成功')
    except:
        print(i + '该公司东方财富网爬取失败')
