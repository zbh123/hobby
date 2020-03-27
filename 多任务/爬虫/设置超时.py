
import urllib.request

#如果网页长时间未响应，

for i in range(1, 100):
    try:
        response = urllib.request.urlopen('http://www.baidu.com',timeout=0.5)
        print(len(response.read()))
    except:
        print('请求超时，继续下一个爬取')







