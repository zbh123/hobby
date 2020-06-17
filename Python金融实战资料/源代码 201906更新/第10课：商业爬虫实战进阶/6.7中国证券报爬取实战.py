'''Python商业爬虫案例实战第6节：舆情监控实战进阶1 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''6.7节：中国证券报爬取实战'''
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def zzss(company):
    url = 'http://search.cs.com.cn/search?searchword=' + company + '&channelid=215308'
    res = requests.get(url, headers=headers, timeout=5000).text

    p_title = '<a style="font-size: 16px;color: #0066ff;line-height: 20px" href=".*?" target="_blank">(.*?)</a>'
    p_href = '<a style="font-size: 16px;color: #0066ff;line-height: 20px" href="(.*?)" target="_blank">'
    p_date = '<td style="color: #666666;font-size: 12px;" >.*?&nbsp;&nbsp;.*?&nbsp;(.*?)</td>'
    title = re.findall(p_title,res)
    href = re.findall(p_href,res)
    date = re.findall(p_date,res,re.S)
    print(title)
    print(href)
    print(date)

    for i in range(len(title)):
        date[i] = date[i].strip()
        date[i] = date[i].split(' ')[0]
        date[i] = re.sub('[.]', '-', date[i])
        print(str(i+1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

companys = ['阿里巴巴','万科集团','百度','腾讯','京东']
for i in companys:
    try:
        zzss(i)
        print(i + '该公司中证搜索爬取成功')
    except:
        print(i + '该公司中证搜索爬取失败')

