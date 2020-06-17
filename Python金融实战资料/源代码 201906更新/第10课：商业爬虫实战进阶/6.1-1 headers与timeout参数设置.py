'''Python商业爬虫案例实战第6节：舆情监控实战进阶1 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''6.1-1：headers与timeout参数设置'''
import requests  # 首先导入requests库和正则表达式re库
import re

'''headers与timeout'''
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
def baidu(company):
    url = 'http://news.baidu.com/ns?word=' + company + '&tn=news&from=news&cl=2&rn=20&ct=0'
    res = requests.get(url, headers=headers, timeout=10).text
    print(len(res))  # 这个len函数作用在字符串上，就是表示文字个数

companys = ['阿里巴巴', '万科集团', '百度']
for i in companys:
    try:
        baidu(i)
        print(i + '爬取成功')
    except:
        print(i + '爬取失败')

