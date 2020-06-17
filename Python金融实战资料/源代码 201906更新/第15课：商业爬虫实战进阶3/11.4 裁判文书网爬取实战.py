'''Python商业爬虫案例实战第11节：商业爬虫实战进阶3 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''11.4节：裁判文书网爬取实战'''
from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get('http://wenshu.court.gov.cn/')
browser.maximize_window()
browser.find_element_by_xpath('//*[@id="gover_search_key"]').clear() #清空原搜索框
browser.find_element_by_xpath('//*[@id="gover_search_key"]').send_keys('房地产') #在搜索框内模拟输入'房地产'三个字
time.sleep(2)  # 这样等待俩秒再点击搜索按钮，更稳妥一点
browser.find_element_by_xpath('//*[@id="searchBox"]/div[2]/div[3]/button').click() #点击搜索按钮
time.sleep(10) # 如果还是获取不到你想要的内容，你可以把这个时间再稍微延长一些
data = browser.page_source
print(data)
