import os
import logging


def cmp(standard_data, temp_data, dict_key=None):
    if isinstance(standard_data, dict) and isinstance(temp_data, dict):
        for standard_key in standard_data:
            if standard_key not in temp_data:
                print("standard存在这个key%s,temp中没有" % standard_key)
                logging.info("standard存在这个key%s,temp中没有" % standard_key)
        for tmp_key in temp_data:
            if tmp_key not in standard_data:
                # del tmp_dict[tmp_key] #删除tmp有，standard没有的值
                print("temp存在这个key%s,standard中没有" % tmp_key)
                logging.info("temp存在这个key%s,standard中没有" % tmp_key)
                continue
            cmp(standard_data[tmp_key], temp_data[tmp_key], tmp_key)

    elif isinstance(standard_data, list) and isinstance(temp_data, list):
        if len(temp_data) != len(standard_data):
            print("list len: '{}' != '{}'".format(len(temp_data), len(standard_data)))
            logging.info("list len: '{}' != '{}'".format(len(temp_data), len(standard_data)))
        for value_temp, value_standard in zip(sorted(temp_data), sorted(standard_data)):
            cmp(value_standard, value_temp, dict_key)
    else:
        if str(temp_data) != str(standard_data):
            print('This has a difference in value ,key is %s, value is %s' % (dict_key, temp_data))
            logging.info('This has a difference in value ,key is %s, value is %s' % (dict_key, temp_data))


if __name__ == '__main__':
    standard_file = 'D:\json\file.standard'
    tmp_file = 'D:\json\file.tmp'
    logging.basicConfig(level=logging.DEBUG, filename='log.txt',
                        format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S')  # 定义log文件格式，级别是INFO，格式是：时间，执行文件名[行数]，级别，传入信息，可以使用
    # logging.warning等，文件中显示相应的级别
    if os.path.exists(standard_file):
        with open(standard_file, 'r') as fp1:
            standard = json.load(fp1, encoding='utf-8')
        with open(tmp_file, 'r') as fp2:
            temp = json.load(fp2, encoding='utf-8')
        cmp(standard, temp)
    else:
        print('没有standard文件')
        logging.info('没有standard文件')
        os._exit(-1)
