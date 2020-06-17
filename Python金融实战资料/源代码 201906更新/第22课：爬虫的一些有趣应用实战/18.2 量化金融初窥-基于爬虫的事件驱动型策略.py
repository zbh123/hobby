'''Python商业爬虫案例实战第18节：爬虫的有趣应用实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''18.2节：量化金融初窥 - 基于爬虫的事件驱动型策略'''
from selenium import webdriver
import re
import time

# browser = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://data.eastmoney.com/report/')
data = browser.page_source
# browser.quit()
# print(data)

p_code = 'class="hqPopCls" data_code="(.*?)" data_name=".*?"'  #
p_company = 'class="hqPopCls" data_code=".*?" data_name="(.*?)"'
p_date = '<span title="(.*?)" class="txt">.*?</span>'
p_title = '<div class="report_tit"><a href=".*?" title=".*?">(.*?)</a>'
p_href = '<div class="report_tit"><a href="(.*?)" title=".*?">.*?</a>'
p_rate = '<div class="report_tit">.*?</div></td><td>(.*?)</td>'
p_change = '<div class="report_tit">.*?</div></td><td>.*?</td><td>(.*?)</td>'
code = re.findall(p_code, data)
company = re.findall(p_company, data)
date = re.findall(p_date, data)
title = re.findall(p_title, data)
href = re.findall(p_href, data)
rate = re.findall(p_rate, data)
change = re.findall(p_change, data)
code = code[0:len(code):2]
company = company[0:len(company):2]
# print(company)
# print(len(company))
# print(code)
# print(len(code))
# print(date)
# print(len(date))
# print(title)
# print(len(title))
# print(href)
# print(len(href))
# print(rate)
# print(len(rate))
# print(change)
# print(len(change))

for i in range(len(company)):
    title[i] = re.sub('&amp;', '', title[i])
    href[i] = 'http://data.eastmoney.com' + href[i]
    print(str(i + 1) + '.' + company[i] + ' - ' + code[i])
    print('研报日期：' + date[i])
    print('研报标题：' + title[i])
    print('研报链接：' + href[i])
    print('公司评级：' + rate[i])
    print('评级变化：' + change[i])
    print('------------------------')



