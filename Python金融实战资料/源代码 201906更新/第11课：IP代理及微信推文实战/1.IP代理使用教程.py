'''IP代理及微信推文爬取实战 by 王宇韬'''
#如果下面的内容被我注释掉了，大家可以选中，然后ctrl+/（Spyder中的快捷键是ctrl+1）取消注释

'''1：IP代理使用教程'''
import requests

proxy = requests.get('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=b030195e2075469299bca6b661c913ff&orderno=YZ2019166267j7iNVq&returnType=1&count=1').text
proxy = proxy.strip() #这一步非常重要，因为要把你看不见的换行符等空格给清除掉
proxies = {"http":"http://"+proxy, "https":"https://"+proxy}
url = 'https://httpbin.org/get'
res = requests.get(url, proxies=proxies).text
print(res)