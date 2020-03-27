import urllib.request
import re
import os
import ssl
from collections import deque

def writeFileBytes(htmlBytes, toPath):
    with open(toPath, 'wb') as fp:
        fp.write(htmlBytes)

def writeFileStr(htmlBytes, toPath):
    with open(toPath, 'w') as fp:
        fp.write(str(htmlBytes))

def getHtmlBytes(url):
    headers = {
        "User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"
    }
    try :
        req = urllib.request.Request(url, headers=headers)
        # 使用ssl创建未验证的版本
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(req, context=context)
        return response.read()
    except:
        print(url + '不是网址')
        return 0


def qqCrawler(url, toPath):
    htmlBytes = getHtmlBytes(url)
    if htmlBytes == 0:
        return [0]
    # writeFileStr(htmlBytes, toPath)
    htmlStr = str(htmlBytes)
    # print(htmlStr)
    pat = r"[1-9]\d{3,9}"
    re_qq = re.compile(pat, re.S)
    qqsList = re_qq.findall(htmlStr)
    qqsList = list(set(qqsList))
    with open(toPath + 'qq号.txt', 'a') as fp:
        for qqStr in qqsList:
            fp.write(qqStr+'\n')
    # print(qqsList)
    # print(len(qqsList))
    pat_web = r'<a href="([^, ]*?)">'
    re_web = re.compile(pat_web, re.S)
    webList = re_web.findall(htmlStr)

    return webList


url = "http://qq.qqdna.com/city/shanghai/shanghai.php"
toPath = r"D:\\ruanjian\matplot_test\爬虫\qqFile.html"
# urlList = qqCrawler(url, toPath)



def center(url, toPath):
    queue = deque()

    queue.append(url)

    while len(queue) != 0:
        targetUrl = queue.popleft()
        urlList = qqCrawler(targetUrl, toPath)
        if len(urlList) > 1:
            for item in urlList:
                tempUrl = item[0]
                queue.append(tempUrl)
center(url, toPath)



