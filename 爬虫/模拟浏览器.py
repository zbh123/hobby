import urllib.request

'''
url = "http://www.baidu.com"

headers = {
    "User-Agent":"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
#设置一个请求体
req = urllib.request.Request(url, headers=headers)
#发起请求
response = urllib.request.urlopen(req)
data = response.read()
'''

agentList = [
    "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)" ,
    "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
]

agentStr = random.choice(agentList)
req = urllib.request.Request(url)
req.add_header("User-Agent", agentStr)
response = urllib.request.urlopen(req)
print(response.read())

