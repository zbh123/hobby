
import urllib.request
import re
import os


def imageCrawler(url, toPath):
    headers = {
        "User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"
    }
    req = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(req)
    HtmlStr = response.read().decode('utf-8')
    # with open(r"D:\\ruanjian\matplot_test\爬虫\一号店图片\yhd.html",'wb') as fp:
    #     fp.write(HtmlStr)

    pat = r'<img src="//(\S+)"/>'
    re_image = re.compile(pat, re.S)
    imagesList = re_image.findall(HtmlStr)
    print(imagesList)
    print(len(imagesList))
    num = 1
    for imageUrl in imagesList:
        path = os.path.join(toPath, str(num)+".jpg")
        num+=1
        #把图片下载到本地
        urllib.request.urlretrieve("http://"+imageUrl, filename=path)


    # return imagesList

url = "http://search.yhd.com/c0-0/k%25E5%25A5%25B3%25E8%25A3%2585/"

toPath = r"D:\\ruanjian\matplot_test\爬虫\一号店图片"

imageCrawler(url, toPath)







