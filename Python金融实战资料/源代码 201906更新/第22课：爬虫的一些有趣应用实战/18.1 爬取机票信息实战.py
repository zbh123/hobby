'''Python商业爬虫案例实战第18节：爬虫的有趣应用实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''18.1节：爬取机票信息实战'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time

city1 = '北京'
city2 = '上海'
date = '2019-01-29'
# 如果你想增强互动性，可以使用如下代码
# city1 = input("请输入出发城市:")
# city2 = input("请输入到达城市:")
# date = input("请输入出发日期xxxx-xx-xx:")

# 1.访问携程首页
browser = webdriver.Chrome()
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://flights.ctrip.com')

# 2.在首页上输入出发城市、到达城市、出发日期并通过按回车键进行访问
# 2.1 模拟键盘输入出发城市
browser.find_element_by_xpath('//*[@id="DepartCity1TextBox"]').clear()
browser.find_element_by_xpath('//*[@id="DepartCity1TextBox"]').send_keys(city1)

# 2.2 模拟键盘输入到达城市
browser.find_element_by_xpath('//*[@id="ArriveCity1TextBox"]').clear()
browser.find_element_by_xpath('//*[@id="ArriveCity1TextBox"]').send_keys(city2)

# 2.3 模拟键盘输入出发日期
browser.find_element_by_xpath('//*[@id="DepartDate1TextBox"]').clear()
browser.find_element_by_xpath('//*[@id="DepartDate1TextBox"]').send_keys(date)

# 2.4 模拟键盘通过按一下ENTER回车键进行页面刷新访问，这里没有选择模拟鼠标点击搜索按钮，因为有的小屏幕上搜索按钮被广告遮住了，点击不了
browser.find_element_by_xpath('//*[@id="DepartDate1TextBox"]').send_keys(Keys.ENTER)
# browser.find_element_by_xpath('//*[@id="search_btn"]').click()  # 这个是模拟鼠标点击搜索按钮的代码，这里不如上面敲击ENTER键的方法好

# 3.获取机票信息网页的源代码
time.sleep(10)
data = browser.page_source
# browser.quit()
# print(data)

# 4.编写航空公司、航班号、出发时间、到达时间、出发机场、到达机场、机票价格正则表达式
p_company = '<strong><img class="pubFlights-logo" src=.*?>(.*?)</strong>'
p_code = '<strong><img class="pubFlights-logo" src=.*?>.*?</strong><span>(.*?)</span>'
p_time1 = '<div class="inb left">.*?<strong class="time">(.*?)</strong>'
p_time2 = '<div class="inb right">.*?<strong class="time">(.*?)</strong>'
p_start = '<div class="inb left">.*?<div class="airport">(.*?)</div>'
p_arrive = '<div class="inb right">.*?<div class="airport">(.*?)</div>'
p_price = '<div class=".*?child_price.*?">.*?¥</dfn>(.*?)</span>'
company = re.findall(p_company, data, re.S)
code = re.findall(p_code, data, re.S)
time1 = re.findall(p_time1, data, re.S)
time2 = re.findall(p_time2, data, re.S)
start = re.findall(p_start, data, re.S)
arrive = re.findall(p_arrive, data, re.S)
price = re.findall(p_price, data, re.S)
print(company)
print(len(company))
print(code)
print(len(code))
print(time1)
print(len(time1))
print(time2)
print(len(time2))
print(start)
print(len(start))
print(arrive)
print(len(arrive))
print(price)
print(len(price))

# 5.打印输出获取的信息
print('公司' + ' 出发地' + ' 到达地' + ' 出发时间' + ' 到达时间' + ' 价格')
for i in range(0, len(company)):
    print(company[i] + ' ' + start[i] + ' ' + arrive[i] + ' ' + time1[i] + ' ' + time2[i] + ' ' + price[i])

