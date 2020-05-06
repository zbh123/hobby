import requests
import json

url = 'http://10.25.108.41:8080/command/startflow'

data = {"FlowName": "测试\录屏测试"}

response = requests.post(url, data=json.dumps(data))
data = response.json()
print(data['result'])
if data['result'] == '':
    print('执行成功')
else:
    print('执行失败，失败信息：', data['result'])
print(data)