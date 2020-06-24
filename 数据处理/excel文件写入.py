import xlwt
import pandas as pd
from collections import OrderedDict
import os
from functools import reduce

script = os.path.dirname(__file__)
print(script)
head_list = ['', '']

data_dict = OrderedDict()

data = pd.DataFrame(data_dict, index=head_list)
# mean_data是序列
mean_data = data.mean(axis=1)
list_mean = [round(i, 2) for i in mean_data]
mean_value = reduce(lambda x, y: x + y, list_mean) / len(list_mean)
list_mean.append(mean_value)
data_dict["Mean"] = list_mean

outfile = os.path.join(script, "result.xlsx")
writer = xlwt.Workbook()
ws = writer.add_sheet('sheet1')
for index, head in enumerate(head_list):
    ws.write(0, index + 1, head)

count = 1
for key, values in data_dict.items():
    ws.write(count, 0, key)
    for index, value in enumerate(values):
        ws.write(count, index + 1, value)
    count += 1
writer.save(outfile)
