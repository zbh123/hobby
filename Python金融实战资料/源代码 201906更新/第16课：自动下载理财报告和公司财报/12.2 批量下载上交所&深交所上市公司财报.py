'''Python商业爬虫案例实战第12章：自动下载下载理财报告和公司财报 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''12.2节：下载深交所上市公司年报'''
from selenium import webdriver
import time
import re
browser = webdriver.Chrome()
url = 'http://www.szse.cn/application/search/index.html?keyword=万科年报'
browser.get(url)
time.sleep(3)# 这里为了严谨，加上3秒的延迟
data = browser.page_source
# print(data)
browser.quit()

p_title = '<a class="text ellipsis pdf" href=.*?><span class="keyword">(.*?)</a>'
p_href = '<a class="text ellipsis pdf" href="(.*?)" target="_blank"'
p_date = '<span class=" pull-right">(.*?)</span>'
title = re.findall(p_title, data)
href = re.findall(p_href, data)
date = re.findall(p_date, data)
print(title)
print(len(title))
print(href)
print(len(href))
print(date)
print(len(date))

for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])


#方法1：用selenium方法创建一个以title[i]为名称的文件夹,当然你也可以仿照上一节的方法，下载到默认文件夹

# for i in range(len(href)):
#     from selenium import webdriver
#     chrome_options = webdriver.ChromeOptions()
#     prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\万科年报\\' + title[i]}  # 这边你可以修改文件储存的位置
#     chrome_options.add_experimental_option('prefs', prefs)
#     browser = webdriver.Chrome(chrome_options=chrome_options)
#     browser.get(href[i])
#     time.sleep(6) #这边把时间放长一点，因为下载PDF需要时间
#     browser.quit()

#方法2：用you_get库自动重命名文件，你得首先把you-get库安装好
for i in range(len(href)):
    import os
    directory = 'D:\\万科年报'
    title[i] = re.sub(' ','',title[i])  # 这一步把原标题里的空格替换掉非常重要，因为原标题里的空格会使最后一行代码运行失败
    name = title[i]
    url = href[i]
    os.system('you-get -o ' + directory + ' -O ' + name + ' ' + url)