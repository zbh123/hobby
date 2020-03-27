import urllib.request

response = urllib.request.urlopen('http://www.baidu.com')
#读取文件的全部内容，赋值给字符串
# data = response.read()
# # print(data)
# #写入文件
# with open('D:\\ruanjian\matplot_test\爬虫\\baidu.html','w') as fp:
#     fp.write(data)

#读取一行
# data = response.readline()
#读取全部内容，赋值给一个列表
# data = response.readlines()
#以上爬取的data都是二进制文件需要.decode('utf-8')，将其转成字符串，以便处理

#response属性
#返回当前环境的有关信息
print(response.info())

#返回状态码

print(response.getcode())

if response.getcode() == 200 or response.getcode() == 304:
    print('success')

#返回当前正在爬取的URL地址
print(response.geturl())


url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%E6%80%8E%E4%B9%88%E7%94%9F%E6%88%90%E8%87%AA%E5%8A%A8%E5%AE%89%E8%A3%85%E5%8D%B8%E8%BD%BD%E8%BD%AF%E4%BB%B6%E7%9A%84iss%E8%84%9A%E6%9C%AC&oq=%25E8%2587%25AA%25E5%258A%25A8%25E7%2594%259F%25E6%2588%2590%25E5%25AE%2589%25E8%25A3%2585%25E5%258D%25B8%25E8%25BD%25BD%25E8%25BD%25AF%25E4%25BB%25B6%25E7%259A%2584iss%25E8%2584%259A%25E6%259C%25AC&rsv_pq=fb62f77000034b7b&rsv_t=3a23BB8KW8uX2%2BuTcM8%2F9JfMANKggs5aAgPKy5P38U%2FKbpFkgNjItHy8PME&rqlang=cn&rsv_enter=0&inputT=6757&rsv_sug3=88&rsv_sug2=0&rsv_sug4=8007'

#解码
newUrl = urllib.request.unquote(url)
print(newUrl)

#编码
newUrl = urllib.request.quote(newUrl)




