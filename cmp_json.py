import os
def cmp(standard_data,temp_data,dict_key = None):
    if isinstance(standard_data, dict) and isinstance(temp_data, dict):
        for standard_key in standard_data:
            if standard_key not in temp_data:
                print("standard存在这个key%s,temp中没有"%standard_key)
        for tmp_key in temp_data:
            if tmp_key not in standard_data:
                #del tmp_dict[tmp_key] #删除tmp有，standard没有的值
                print("temp存在这个key%s,standard中没有"%tmp_key)
                continue
            cmp(standard_data[tmp_key], temp_data[tmp_key],tmp_key)
            
    elif isinstance(standard_data, list) and isinstance(temp_data, list):
        if len(temp_data) != len(standard_data):
            print("list len: '{}' != '{}'".format(len(temp_data), len(standard_data)))
        for value_temp, value_standard in zip(sorted(temp_data), sorted(standard_data)):
            cmp(value_standard, value_temp,dict_key)
    else:
        if str(temp_data) != str(standard_data):
            print('This has a difference in value ,key is %s, value is %s'%(dict_key,temp_data))
            
if __name__ == '__main__':
    standard_file = 'D:\json\file.standard'
    tmp_file = 'D:\json\file.tmp'
    if os.path.exists(standard_file):
        with open(standard_file,'r') as fp1:
            standard = json.load(fp1,encoding = 'utf-8')
        with open(tmp_file,'r') as fp2:
            temp = json.load(fp2,encoding = 'utf-8')
        cmp(standard,temp)
    else:
        print('没有standard文件')
        os._exit(-1)
        
