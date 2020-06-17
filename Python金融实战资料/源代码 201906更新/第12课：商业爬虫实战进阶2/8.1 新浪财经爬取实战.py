'''Python商业爬虫案例实战第8节：舆情监控实战进阶2 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''8.1节：新浪财经爬取实战'''
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def xinlang(company,code):
    url = 'https://search.sina.com.cn/?q=' + code + '&range=all&c=news&sort=time'
    print('爬取的公司为' + company)

    res = requests.get(url, headers=headers, timeout=10).text
    # print(res)

    p_title = '<h2><a href=".*?" target="_blank">(.*?)</a>'
    p_href = '<h2><a href="(.*?)" target="_blank">'
    p_date = '<span class="fgray_time">(.*?)</span>'
    title = re.findall(p_title, res)
    href = re.findall(p_href, res)
    date = re.findall(p_date, res)
    # print(title)
    # print(href)
    # print(date)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[1]
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])

companys = {'阿里巴巴':'%B0%A2%C0%EF%B0%CD%B0%CD','万科集团':'%CD%F2%BF%C6%BC%AF%CD%C5','华能信托':'%BB%AA%C4%DC%D0%C5%CD%D0'}
for i in companys:
    xinlang(i,companys[i])


#方法2 这里就是破解了它的编码方式，不需要自己再去网站上找它对应的英文编码。它其实是进行了一个gbk的编码，大家了解即可，爬取新浪财经的时候直接拿去用就行了
from urllib.parse import quote
companys1 = ['阿里巴巴', '万科集团', '华能信托']
companys2 = {}
for i in companys1:
    code = quote(i.encode('gbk'))
    companys2[i] = code
print(companys2)
for i in companys2:
    xinlang(i,companys2[i])


'''这是最开始的方法：直接写一个编码列表的方法，非常好理解且好写，但这样没法知道公司信息'''
# def xinlang2(code):
#     url = 'https://search.sina.com.cn/?q=' + code + '&range=all&c=news&sort=time'
#     res = requests.get(url, headers=headers, timeout=10).text
#     # print(res)
#
#     p_title = '<h2><a href=".*?" target="_blank">(.*?)</a>'
#     p_href = '<h2><a href="(.*?)" target="_blank">'
#     p_date = '<span class="fgray_time">(.*?)</span>'
#     title = re.findall(p_title, res)
#     href = re.findall(p_href, res)
#     date = re.findall(p_date, res)
#     # print(title)
#     # print(href)
#     # print(date)
#
#     for i in range(len(title)):
#         title[i] = re.sub('<.*?>', '', title[i])
#         date[i] = date[i].split(' ')[1]
#         print(str(i + 1) + '.' + title[i] + '-' + date[i])
#         print(href[i])
#
# companys = ['%B0%A2%C0%EF%B0%CD%B0%CD','%CD%F2%BF%C6%BC%AF%CD%C5','%BB%AA%C4%DC%D0%C5%CD%D0']
# for i in companys:
#     xinlang2(i)