'''Python商业爬虫案例实战第8节：舆情监控实战进阶2 by 王宇韬'''
#如果下面的内容被我注释掉了，大家如果想运行的话，可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''8.2节：新浪微博文章爬取实战'''
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def weibo2(company):
    url = 'https://s.weibo.com/weibo?q=' + company + '&Refer=article_weibo'
    res = requests.get(url, headers=headers, timeout=10).text
    # print(res)

    p_name = '<a href=".*?" class="name" target="_blank" nick-name="(.*?)"'
    name = re.findall(p_name, res)
    p_content = '<p class="txt" node-type="feed_list_content" nick-name=".*?>(.*?)</p>'
    content = re.findall(p_content, res, re.S)
    # print(name)
    # print(len(name))
    # print(content)
    # print(len(content))

    for i in range(len(name)):
        content[i] = content[i].strip()
        content[i] = re.sub(r'<.*?>', '', content[i])
        print(str(i + 1) + '.' + content[i] + '——来自:' + name[i])

companys = ['华能信托','阿里巴巴','万科集团','百度','腾讯','京东']
for i in companys:
    try:
        weibo2(i)
        print(i + '该公司新浪微博综合爬取成功')
    except:
        print(i + '该公司新浪微博综合爬取失败')
