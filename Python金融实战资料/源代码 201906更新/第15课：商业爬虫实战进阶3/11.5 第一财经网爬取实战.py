'''Python商业爬虫案例实战第11节：商业爬虫实战进阶3 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''11.5节：第一财经网爬取实战'''
from selenium import webdriver
import re


def dycj(company):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('https://www.yicai.com/search?keys=' + company)
    data = browser.page_source
    browser.quit()
    # print(data)
    p_title = '<div>.*?<h2>(.*?)</h2>.*?<p>'
    p_href = ' <a href="(.*?)" class="f-db" target="_blank">'
    p_date = '<div class="author">.*?<span>.*?</span>.*?<span>(.*?)</span>'
    title = re.findall(p_title, data)
    href = re.findall(p_href, data)
    date = re.findall(p_date, data)
    # print(title)
    # print(len(title))
    # print(date)
    # print(len(date))
    # print(href)
    # print(len(href))

    for i in range(len(title)):
        href[i] = 'https://www.yicai.com' + href[i]
        date[i] = date[i].split(' ')[0]
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

companys = ['华能信托','阿里巴巴','腾讯','京东']
for i in companys:
    try:
        dycj(i)
        print(i + '该公司第一财经网爬取成功')
    except:
        print(i + '该公司第一财经网爬取失败')