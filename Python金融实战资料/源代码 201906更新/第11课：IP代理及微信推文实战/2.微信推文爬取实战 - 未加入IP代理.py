'''Python商业爬虫案例实战第7节：IP代理及微信推文爬取实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''2：微信推文爬取实战 - 未加入IP代理'''
import requests
import re
import time
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def weixin(company):
    url = 'https://weixin.sogou.com/weixin?type=2&query=' + company
    res = requests.get(url, headers=headers, timeout=10).text
    try:
        res = res.encode('ISO-8859-1').decode('utf-8')  # 处理可能存在的乱码问题：方法3
    except:
        try:
            res = res.encode('ISO-8859-1').decode('gbk')  # 处理可能存在的乱码问题：方法2
        except:
            res = res  # 方法1
    # print(res)

    p_href = 'data-share="(.*?)">.*?</a>'
    p_title = 'data-share=".*?">(.*?)</a>'
    p_date = 'timeConvert\(\'(.*?)\'\)'
    href = re.findall(p_href, res)
    title = re.findall(p_title, res)
    date = re.findall(p_date, res)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        title[i] = re.sub('&.*?;', '', title[i])
        href[i] = re.sub('amp;', '', href[i])
        timestamp = int(date[i])
        timeArray = time.localtime(timestamp)
        date[i] = time.strftime("%Y-%m-%d", timeArray)
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

weixin('华能信托')

# companys = ['华能信托','阿里巴巴','万科集团','百度','腾讯']
# for i in companys:
#     try:
#         weixin(i)
#         print(i + '该公司微信推文爬取成功')
#     except:
#         print(i + '该公司微信推文爬取失败')

