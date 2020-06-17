'''Python商业爬虫案例实战第6节：舆情监控实战进阶1 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''6.2节：中国经营报爬取实战'''
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def zgjy(company):
    url = 'http://zhannei.baidu.com/cse/search?s=1769878842797832208&entry=1&q=' + company
    res = requests.get(url, headers=headers, timeout=10).text
    res = res.encode('ISO-8859-1').decode('utf-8')
    # print(res)
    p_title = '<a rpos="" cpos="title" href=".*?"  target="_blank">(.*?)</a>'
    p_href = '<a rpos="" cpos="title" href="(.*?)"  target="_blank">.*?</a>'
    p_date = '<span class="c-showurl" >(.*?)</span>'

    title = re.findall(p_title, res)
    href = re.findall(p_href, res)
    date = re.findall(p_date, res)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[1]
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

companys = ['华能信托','阿里巴巴','万科集团','百度','腾讯','京东']
for i in companys:
    try:
        zgjy(i)
        print(i + '该公司中国经营报爬取成功')
    except:
        print(i + '该公司中国经营报爬取失败')