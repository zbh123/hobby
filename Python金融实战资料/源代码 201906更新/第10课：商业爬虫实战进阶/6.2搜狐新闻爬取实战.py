'''Python商业爬虫案例实战第6节：舆情监控实战进阶1 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''6.2节：搜狐新闻爬取实战'''
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def souhu(company):
    url = 'https://news.sogou.com/news?mode=1&sort=0&fixrank=1&query=' + company + '&shid=djt1'
    res = requests.get(url,headers=headers, timeout=10).text
    # print(res)

    p_title = '<a href=".*?" id="uigs.*?" target="_blank">(.*?)</a>'
    title = re.findall(p_title, res)
    p_href = '<a href="(.*?)" id="u.*?" target="_blank">'
    href = re.findall(p_href, res)
    p_date = '<p class="news-from">.*?&nbsp;(.*?)</p>'
    date = re.findall(p_date, res)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        title[i] = re.sub('&.*?;', '', title[i])
        date[i] = re.sub('<.*?>', '', date[i])
        print(str(i+1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

companys = ['华能信托','阿里巴巴','万科集团','百度','腾讯','京东']
for i in companys:
    try:
        souhu(i)
        print(i + '该公司搜狐新闻爬取成功')
    except:
        print(i + '该公司搜狐新闻爬取失败')