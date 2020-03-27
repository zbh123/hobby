import urllib.request
import re
def jokeCrawler(url):
    headers = {
        "User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"
    }

    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)

    HTML = response.read().decode("utf-8")

    pat = r'<div class="author clearfix">(.*?)<span class="stats-vote"><i class="number">'
    re_joke = re.compile(pat, re.S)
    divList = re_joke.findall(HTML)
    print(divList, len(divList))
    dic = {}
    for div in divList:
        #用户名
        re_u = re.compile(r"<h2>(.*?)</h2>", re.S)
        username = re_u.findall(div)
        username = username[0]
        #段子
        re_d = re.compile(r'<div class="content">\n<span>(.*?)</span>',re.S)
        duanzi = re_d.findall(div)
        duanzi = duanzi[0]


        # print(username, duanzi)
        dic[username] = duanzi
    return dic
    # with open(r"D:\\ruanjian\matplot_test\爬虫\\糗事百科.html",'w') as f:
    #     f.write(HTML)





url = "https://www.qiushibaike.com/text/page/1/"
info = jokeCrawler(url)
for k,v in info.items():
    print(k, v)


