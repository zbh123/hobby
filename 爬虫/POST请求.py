'''
特点：把参数打包，单独传输
优点：数据量大，安全
缺点：速度慢
'''


import urllib.request
import urllib.parse

url = "http://www.baidu.com"
data = {
    'username':'sunck',
    'passwd':'666'
}
#对要发送的数据进行打包

postData = urllib.parse.urlencode(data).encode('utf-8')

#请求体
req = urllib.request.Request(url, data=postData)
req.add_header("User-Agent","User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0")
#请求
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))


















