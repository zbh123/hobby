'''4.1-3 多家公司批量爬取多页新闻 by 王宇韬'''
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


# 爬取多个公司的多页, 可以给函数传入两个参数，供参考
def baidu(company, page):
    num = (page - 1) * 10
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company + '&pn=' + str(num)  # rtt=4则是按时间顺序爬取，rtt=1为按焦点排序
    res = requests.get(url, headers=headers).text
    # 其他相关爬虫代码

    p_info = '<p class="c-author">(.*?)</p>'
    info = re.findall(p_info, res, re.S)
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)

    source = []  # 先创建两个空列表来储存等会分割后的来源和日期
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()

        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')  # i是数字，所以要用str函数转换一下，且i是从0开始的序号，所以要写str(i+1)
        print(href[i])


companys = ['华能信托', '阿里巴巴', '万科集团', '百度集团', '腾讯', '京东']
for company in companys:
    for i in range(10):  # i是从0开始的序号，所以下面要写i+1，这里一共爬取了10页
        baidu(company, i+1)
        print(company + '第' + str(i+1) + '页爬取成功')
