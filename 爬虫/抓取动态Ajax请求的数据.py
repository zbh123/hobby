import urllib.request
import ssl
import json
import re

def ajaxCrawler(url):
    headers = {
        "User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"
    }
    req = urllib.request.Request(url, headers=headers)

    #使用ssl创建未验证的版本
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(req,context=context)
    # response = urllib.request.urlopen(req)

    jsonStr = response.read().decode("utf-8")
    # jsonStr = re.sub(r'<html>|<head>|</head>|<body>|<pre style="word-wrap: break-word; white-space: pre-wrap;">','', jsonStr)
    # jsonStr = re.sub(r'</pre>|</body>|</html>|</script>','', jsonStr)
    # print(jsonStr)
    jsonData = json.loads(jsonStr)

    return jsonData


url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=20"
info = ajaxCrawler(url)
print(type(info))


for i in range(11):
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=" +str(i*20)
    info = ajaxCrawler(url)
    print(type(info))






