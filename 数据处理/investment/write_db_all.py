#!python3
# -*- coding:utf-8 -*-

import MySQLdb
from sshtunnel import SSHTunnelForwarder
import xlrd
import pandas as pd
import os, sys
import time, calendar


def ipo_deal():
    path = r'D:\0RPA\计划财务部\投行业务'
    now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    now_time = '20201203'
    path = os.path.join(path, now_time)
    if not os.path.exists(path):
        sys.exit(0)
    path1 = os.path.join(path, '科创板IPO审核申报企业情况.xls')
    path2 = os.path.join(path, '科创板IPO审核申报企业情况_整理.xls')

    if os.path.exists(path2):
        os.remove(path2)
    else:
        return True

    dataframe = pd.read_excel(path1)
    status_list = ['报送证监会', '已审核通过', '待上会', '已回复(第三次)', '已回复(第二次)', '已回复', '暂缓表决', '已问询', '已受理']
    print(dataframe.shape)

    print(dataframe[dataframe.审核状态.isin(status_list)].shape)
    data = dataframe[dataframe.审核状态.isin(status_list)]
    data.to_excel(path2, index=None)


def get_last_month_start_and_end(date):
    """
    年份 date(2017-09-08格式)
    :param date:
    :return:本月第一天日期和本月最后一天日期
    """
    if date.count('-') != 2:
        raise ValueError('- is error')
    year, month = str(date).split('-')[0], str(date).split('-')[1]
    if month == '1':
        month_last = 12
        year = int(year) - 1
    else:
        month_last = int(month) - 1
        year = int(year)
    end = calendar.monthrange(year, month_last)[1]
    end_date = '%s-%s-%s' % (year, month_last, end)
    return end_date


def mysql_link(de_name):
    """
      连接数据库
      args：db_name（数据库名称）
      returns:db
    """
    try:
        server = SSHTunnelForwarder(
            ("10.29.24.47", 222),  # ssh IP和port
            ssh_password="zts000000",  # ssh 密码
            ssh_username="tianyj",  # ssh账号
            remote_bind_address=("10.29.129.94", 3306),  # 数据库所在的IP和端口
            local_bind_address=('0.0.0.0', 10008)
        )

        server.start()
        # 打印本地端口，已检查是否配置正确
        # print(server.local_bind_port)

        db = MySQLdb.connect(host="127.0.0.1",  # 固定写法
                             port=server.local_bind_port,
                             user="rpa",  # 数据库账号
                             passwd="zts000",  # 数据库密码
                             db=de_name,
                             charset='utf8',
                             connect_timeout=1000)  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
        return db, server
    except:
        print("could not connect to mysql server")


def open_excel(excel_file):
    """
      读取excel函数
      args：excel_file（excel文件，目录在py文件同目录）
      returns：book
    """
    try:
        book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
        # print(sys.getsizeof(book))
        return book
    except:
        print("open excel file failed!")


def generate_sql(table_name, value):
    """
        生成sql语句
        :param table_name:
        :return:
    """
    now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    now_time = '2020-12-03'
    sql = ''
    if table_name == 'wind_dcm':
        sql = "INSERT INTO " + table_name + " (`organization`, total_amount, total_ranking, market_share, `number`," \
                                            "average_amount, remark, amount_lgd, market_share_lgd, number_lgd," \
                                            "amount_pbd, market_share_pbd, number_pbd, amount_npfb," \
                                            "market_share_npfb, number_npfb, amount_ed, market_share_ed, number_ed," \
                                            "amount_cd, market_share_cd, number_cd, amount_stfb, market_share_stfb," \
                                            "number_stfb, amount_mtn, market_share_mtn, number_mtn, amount_ot, " \
                                            "market_share_ot, number_ot, amount_iad, market_share_iad, number_iad," \
                                            "amount_gbib, market_share_gbib, number_gbib, amount_abs, " \
                                            "market_share_abs, number_abs, amount_exd, market_share_exd, number_exd," \
                                            "amount_standard_bill, market_standard_bill, number_standard_bill, " \
                                            "amount_other, market_share_other, number_other, `current_time`) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and `organization` = '" + \
              value[0] + "')"
    elif table_name == 'wind_dcm_without_gb':
        sql = "INSERT INTO " + table_name + " (`organization`, total_amount, total_ranking, market_share, `number`," \
                                            "average_amount, remark, amount_npfb, market_share_npfb, number_npfb," \
                                            " amount_ed, market_share_ed, number_ed," \
                                            "amount_cd, market_share_cd, number_cd, amount_stfb, market_share_stfb," \
                                            "number_stfb, amount_mtn, market_share_mtn, number_mtn, amount_ot, " \
                                            "market_share_ot, number_ot, amount_iad, market_share_iad, number_iad," \
                                            "amount_gbib, market_share_gbib, number_gbib, amount_abs, " \
                                            "market_share_abs, number_abs, amount_exd, market_share_exd, number_exd," \
                                            "amount_standard_bill, market_standard_bill, number_standard_bill," \
                                            "amount_other, market_share_other, number_other, `current_time`) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and `organization` = '" + \
              value[0] + "')"
    elif table_name == 'wind_star':
        sql = "INSERT INTO " + table_name + " (`code`, bond_abbr, accept_date, fullname_issuer, accept_batch, " \
                                            "audit_status, ipo_theme, ipo_theme_detail, list_standards," \
                                            " to_raise_funds, estimated_market_value, sponsor_and_underwriter," \
                                            " account_firm, law_firm, asset_appraisal_agency, registration, csrc, " \
                                            "update_time, `current_time`, data_time) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                            "%s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and `code` = '" + \
              value[0] + "')"
    elif table_name == 'wind_ecm_list':
        '''
        
        '''
        sql = "INSERT INTO " + table_name + " (organization_full, organization_abbr, total_fund, ipo_fund," \
                                            " increase_under_fund, increase_finance_fund, issue_fund, preferred_fund," \
                                            " convertible_fund, total_underw, ipo_underw, increase_under_underw," \
                                            "increase_finance_underw, issue_underw, preferred_underw, " \
                                            "convertible_underw, total_issue, ipo_issue, increase_under_issue, " \
                                            "increase_finance_issue, issue_issue, preferred_issue, convertible_issue, " \
                                            "`current_time`) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                            "%s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and `organization_full` = '" + \
              value[0] + "')"
    elif table_name == 'wind_ecm_issue':
        sql = "INSERT INTO " + table_name + " (organization_full, organization_abbr, total_fund, ipo_fund," \
                                            " increase_under_fund, increase_finance_fund, issue_fund, preferred_fund," \
                                            " convertible_fund, total_underw, ipo_underw, increase_under_underw," \
                                            "increase_finance_underw, issue_underw, preferred_underw, " \
                                            "convertible_underw, total_issue, ipo_issue, increase_under_issue, " \
                                            "increase_finance_issue, issue_issue, preferred_issue, convertible_issue, " \
                                            "`current_time`) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                            "%s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and organization_full = '" + \
              value[0] + "')"
    elif table_name == 'csrc_refinance':
        sql = "INSERT INTO " + table_name + " (index_l, application_type, enterprise, stock_code, sponsor, " \
                                            "accept_date, audit_status, remark, `current_time`, data_time) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and enterprise = '" + \
              value[2] + "')"
    elif table_name == 'csrc_ipo':
        sql = "INSERT INTO " + table_name + " (index_l, enterprise, sponsor, account_firm, law_firm, accept_date, " \
                                            "audit_status, spot_check, remark, `current_time`, data_time) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and enterprise = '" + \
              value[1] + "')"
    elif table_name == 'shenzhen_refinance':
        '''
               index_l, company, issuing_object, finance_type, audit_status, srci, sponsor, law_firm, account_firm, update_date, accept_date
                       '''
        sql = "INSERT INTO " + table_name + " (index_l, company, issuing_object, finance_type, audit_status, srci, " \
                                            "sponsor, law_firm, account_firm, update_date, accept_date," \
                                            " `current_time`, data_time) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and company = '" + \
              value[1] + "')"
    elif table_name == 'shenzhen_ipo':
        '''
                index_l, fullname_issuer, audit_status, place_registrate, srci, sponsor,  law_firm, account_firm, update_date, accept_date
                       '''
        sql = "INSERT INTO " + table_name + " (index_l, fullname_issuer, audit_status, place_registrate, srci, sponsor," \
                                            "  law_firm, account_firm, update_date, accept_date, `current_time`, data_time) " \
                                            "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                            " FROM DUAL WHERE NOT EXISTS(SELECT * FROM " + table_name + " WHERE `current_time` = '" + now_time + "' and fullname_issuer = '" + \
              value[1] + "')"
    return sql


def store_to(db_name, table_name_index, excel_file):
    """
      执行插入操作
      args:db_name（数据库名称）
         table_name(表名称）
         excel_file（excel文件名，把文件与py文件放在同一目录下）

    """
    db, server = mysql_link(db_name)  # 打开数据库连接
    try:
        now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        now_time = '2020-12-03'
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        book = open_excel(excel_file)  # 打开excel文件
        sheets = book.sheet_names()  # 获取所有sheet表名
        sheet_num = 0
        for sheet in sheets:
            if table_name_index[0] == 'csrc_ipo':
                sheet_num += 1
            if sheet_num > 2:
                break
            sh = book.sheet_by_name(sheet)  # 打开每一张表
            row_num = sh.nrows
            # print(row_num)
            # list = []
            num = 0  # 用来计数
            flag = 0  # 失败标志
            count = 0  # 控制失败次数
            i = table_name_index[1]
            while i < row_num:
                # print(i, flag, count)
                if flag == 1:
                    pass
                else:
                    count = 0
                if count == 3:  # 失败3次，跳过该行数据
                    i += 1
                    count = 0
                flag = 0
                row_data = sh.row_values(i)  # 按行获取excel的值
                value = []
                if row_data[2] == '':
                    i += 1
                    continue
                for j in range(len(row_data)):
                    ctype = sh.cell(i, j).ctype  # 获取单元格格式
                    # ctype =3,为日期
                    if ctype == 3:
                        date = xlrd.xldate.xldate_as_datetime(row_data[j], 0)
                        cell = date.strftime('%Y-%m-%d')  # ('%Y/%m/%d %H:%M:%S')
                        # print(cell)
                        value.append(cell)
                    else:
                        value.append(row_data[j])
                value.append(now_time)
                if table_name_index[0] in special_key:
                    value.append(get_last_month_start_and_end(now_time))
                value = tuple(value)
                sql = generate_sql(table_name_index[0], value)
                # print(sql)
                # print(value)
                try:
                    # 执行sql语句
                    cursor.execute(sql, value)
                    db.commit()  # 提交
                    num += 1
                    i += 1
                except Exception as e:
                    print('写入数据库失败,失败信息：', e)
                    flag = 1
                    count += 1
                    db.close()
                    server.close()
                    db, server = mysql_link(db_name)  # 打开数据库连接
                    db.rollback()
                    cursor = db.cursor()
            cursor.close()  # 关闭连接
            print("worksheets: " + sheet + " has been inserted " + str(num) + " datas!")
    except Exception as e:
        db.rollback()
        print('写入数据库失败,失败信息：', e)
    finally:
        db.close()
        server.close()


def verify_excel(table_name_index, excel_file):
    '''
    验证Excel表的头结构关键字是否正确
    :return:
    '''
    terify_name = r'D:\0RPA\计划财务部\主要指标验证表结构.xls'
    book = open_excel(terify_name)  # 打开验证excel文件
    sheet = book.sheet_names()
    for sheet_name in sheet:
        if sheet_name.strip() == table_name_index[0]:
            print(sheet_name)
            sh = book.sheet_by_name(sheet_name)
            col_num_verify = sh.ncols
            row_num_verify = sh.nrows

            book1 = open_excel(excel_file)  # 打开excel文件
            sh1 = book1.sheet_by_index(0)  # 打开Excel的第一张表
            col_num = sh1.ncols
            row_num = table_name_index[1]
            if col_num_verify != col_num or row_num_verify != row_num:
                print('表头结构行列数据不正确，理论行列为：%d, %d,实际行列为：%d，%d' % (row_num_verify, col_num_verify, row_num, col_num))
                # sys.exit(-1)
            for i in range(row_num_verify):
                for j in range(col_num_verify):
                    if sh.cell_value(i, j) != sh1.cell_value(i, j):
                        print('第%d行，第%d列的表头数据不对应，理论数据：%s，实际数据：%s' % (i, j, sh.cell_value(i, j), sh1.cell_value(i, j)))
                        sys.exit(-1)
            break


if __name__ == '__main__':
    ipo_deal()
    special_key = ['wind_star', 'csrc_refinance', 'csrc_ipo', 'shenzhen_refinance', 'shenzhen_ipo']
    path_db = {'债权承销排名(不含可转债)': ['wind_dcm', 3], '债权承销排名(不含三债)': ['wind_dcm_without_gb', 3],
               '科创板IPO审核申报企业情况_整理': ['wind_star', 1], '股权投行承销排名_上市日': ['wind_ecm_list', 2],
               '股权投行承销排名_发行日': ['wind_ecm_issue', 2], '发行监管部再融资申请企业基本信息情况表': ['csrc_refinance', 3],
               '发行监管部首次公开发行股票企业基本信息情况表': ['csrc_ipo', 3], '创业板_再融资': ['shenzhen_refinance', 1],
               '创业板_IPO': ['shenzhen_ipo', 1]}
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\债权承销排名(不含可转债).xls'
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\债权承销排名(不含三债).xls'
    # path = r'D:\0RPA\计划财务部\投行业务\20201030\科创板IPO审核申报企业情况_整理.xls'
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\股权投行承销排名_上市日.xls'
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\股权投行承销排名_发行日.xls'
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\发行监管部再融资申请企业基本信息情况表（截至2020年7月16日）.xlsx'
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\发行监管部首次公开发行股票企业基本信息情况表（截至2020年7月16日）.xls'
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\创业板_再融资.xls'
    # path = r'D:\0RPA\计划财务部\投行业务\20200720\创业板_IPO.xls'
    path = r'D:\0RPA\计划财务部\投行业务'
    now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    now_time = '20201203'
    path = os.path.join(path, now_time)
    if not os.path.exists(path):
        sys.exit(0)
    fileList = os.listdir(path)
    for fileName in fileList:
        fileAbsPath = os.path.join(path, fileName)
        if not os.path.isdir(fileAbsPath):
            print('file name:' + fileName)
            base_dir = fileName.split('.')[0].split("（")[0]
            # print(base_dir)
            for key, value in path_db.items():
                if key in base_dir:
                    store_to('investment_banks', value, fileAbsPath)
                    # verify_excel(value, fileAbsPath)
    # store_to('investment_banks', 'wind_star', path)
