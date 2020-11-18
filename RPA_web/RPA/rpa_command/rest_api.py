import requests
import json

url = 'http://10.49.87.35:8080/command/startflow'
# url = 'http://10.49.87.35:8080/command/machinestatus'   # 获取机器状态
# url = 'http://10.49.87.35:8080/command/flowresult'   # 设置流程结果和机器状态
# url = 'http://10.49.87.35:8080/command/stopflow'

data = {"FlowName": "托管部\FA外包估值\FA系统日终清算第二批", "FlowNum": 10}
# data = {"FlowNum": 2}
# data = {"FlowName": "托管部\TA日清算\TA日初始化", "FlowResult": '成功'}
# data = {"FlowNum": 2}
response = requests.post(url, data=json.dumps(data))
data = response.json()
print(data['result'])
# if data['result'] == '':
#     print('执行成功')
# else:
#     print('执行失败，失败信息：', data['result'])
print(data)

