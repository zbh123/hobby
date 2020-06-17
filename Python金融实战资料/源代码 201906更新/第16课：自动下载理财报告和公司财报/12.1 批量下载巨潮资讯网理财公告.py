'''Python商业爬虫案例实战第12章：自动下载下载理财报告和公司财报 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''12.1节：批量下载巨潮资讯网理财公告'''
from selenium import webdriver
import re
import time
browser = webdriver.Chrome()
url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=理财'
browser.get(url)
time.sleep(1)
data = browser.page_source
p_count = 'id="page-info-title"><span>合计约(.*?)条</span>'
count = re.findall(p_count, data)[0] #获取公告个数，注意这里要加一个[0],因为findall返回的是一个列表
pages = int(int(count)/10)

#1.自动翻页
datas = []
datas.append(data) #这边是把第一页源代码先放到datas这个列表里
for i in range(3): #这边为了演示改成了range(3)，想爬全部的话改成range(pages)
    browser.find_element_by_xpath('//*[@id="pagination_title"]/ul/li[12]').click()
    time.sleep(2)
    data = browser.page_source
    datas.append(data)
    time.sleep(1)
alldata = "".join(datas)
browser.quit()

p_title = '<td class="sub-title"><a href=".*?" target="_blank">(.*?)</td>'
p_href = '<td class="sub-title"><a href="(.*?)" target="_blank">.*?</td>'
p_date = '<div class="sub-time-time">(.*?)</div>'
title = re.findall(p_title, alldata)
href = re.findall(p_href, alldata)
date = re.findall(p_date, alldata)

for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])
    href[i] = 'http://www.cninfo.com.cn' + href[i]
    href[i] = re.sub('amp;', '', href[i])
    date[i] = date[i].split(' ')[0]
    print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
    print(href[i])

#2.自动筛选
for i in range(len(title)):
    if '2018' in date[i] or '2019' in date[i]: #筛选2018和2019年的
        title[i] = title[i]
        href[i] = href[i]
        date[i] = date[i]
    else:
        title[i] = ''
        href[i] = ''
        date[i] = ''
while '' in title:
    title.remove('')
while '' in href:
    href.remove('')
while '' in date:
    date.remove('')

#3.自动批量爬取PDF - 选择默认储存位置
for i in range(len(href)):
    browser = webdriver.Chrome()
    browser.get(href[i])
    try:
        browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div/a[4]').click()
        time.sleep(3)
        browser.quit()
        print(str(i+1) + '.' + title[i] + '是PDF文件')
    except:
        print(title[i] + '不是PDF文件')

#3.自动批量爬取PDF - 自己设定储存位置
# for i in range(len(href)):
#     chrome_options = webdriver.ChromeOptions()
#     prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\公告'} #这边你可以修改文件储存的位置
#     chrome_options.add_experimental_option('prefs', prefs)
#     browser = webdriver.Chrome(chrome_options=chrome_options)
#     browser.get(href[i])
#     try:
#         browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div/a[4]').click()
#         time.sleep(3) # 这个一定要加，因为下载需要一点时间
#         print(str(i+1) + '.' + title[i] + '下载完毕')
#         browser.quit()
#     except:
#         print(title[i] + '不是PDF')
