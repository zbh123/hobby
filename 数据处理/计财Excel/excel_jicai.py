#!python3
# -*- coding:utf-8 -*-

import re
from datetime import datetime, date

import xlrd, xlwt
import time
import os, sys

from xlutils.copy import copy

"""
股票质押明细表操作，
1，选取自有资金。
2，批注及备注中包含本月
3，提取字段
"""


def open_excel(excel_file):
    """
      读取excel函数
      args：excel_file（excel文件，目录在py文件同目录）
      returns：book
    """
    try:
        book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
        return book
    except:
        print("open excel file failed!")


def filter_sheet(excel_file, target_folder, now_month):
    """
    过滤excel文件的sheet
    :param excel_file:
    :return:
    """
    book = open_excel(excel_file)  # 打开excel文件
    sheets = book.sheet_names()  # 获取所有sheet表名
    # 如果sheet包含待赎回交易(汇总)，返回sheet的索引
    for sheet in sheets:
        if sheet != '待购回交易（汇总）':
            continue
        # 处理当前sheet的excel
        handle_excel(book, sheet, target_folder, now_month)
        break


def handle_excel(book, sheet, target_folder, now_month):
    """
    处理表
    :param book:
    :param sheet:
    :return:
    """
    # 创建新表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('待赎回交易(处理后)')
    # 读取原表行
    sh = book.sheet_by_name(sheet)
    row_num = sh.nrows
    # 把头部写入新的excel
    row_data = sh.row_values(0)
    for i, content in enumerate(row_data):
        worksheet.write(0, i, content)
    # 处理每一行
    r = 1
    for row in range(1, row_num):
        row_data = sh.row_values(row)
        # 出资方
        investor = row_data[1]
        if investor != '自有资金':
            continue
        dateFormat = xlwt.XFStyle()
        # 把这一行写入新的excel
        for i, content in enumerate(row_data):
            # 时间格式特殊处理下
            if i == 0 or i == 26:
                date_value = xlrd.xldate_as_tuple(content, 0)
                date_value = date(*date_value[:3]).strftime('%Y/%m/%d')
                date_value = time_format(date_value)
                dateFormat.num_format_str = 'yyyy/m/d'
                worksheet.write(r, i, date_value, dateFormat)
            else:
                worksheet.write(r, i, content)
        # 行数+1
        r = r + 1
    workbook.save(target_folder + '/自有资金-待赎回交易.xlsx')


def handle_comment(target_file, now_month):
    """
    处理批注
    :return:
    """
    # 读取修改后的文件
    book = open_excel(target_file)
    sh = book.sheet_by_index(0)
    row_num = sh.nrows
    colx_num = sh.ncols
    # 设置修改文件
    workbook = copy(book)
    worksheet = workbook.get_sheet(0)
    # worksheet.write(0, colx_num, '批注')
    for row in range(1, row_num):
        row_data = sh.row_values(row)
        comment = row_data[23]
        # 先把批注写到最后一列
        # worksheet.write(row, colx_num, comment)
        # 处理批注（分成数组，如果数组有月份和数字，把月份和数字向后写）
        com = comment.split('；')
        index_row = 0  # 用一个变量控制每一行行的最大列
        for c in com:
            print(c)
            if not (now_month + '/' in c):
                continue
            # 提取数组里面的日期和金额
            date_reg_exp = re.compile('\d{4}[-/]\d{1,2}[-/]\d{1,2}')
            matches_list = date_reg_exp.findall(c)
            print(matches_list)
            # 金额（把万或者元前面的数字提取）
            for matches in matches_list:
                c_no_date = c.replace(matches, '')
                print(c_no_date)
                c_num_unit = re.findall(r'\d+(?:\.\d+)?万', c_no_date)
                print(c_num_unit)
                c_num2_unit = re.findall(r'\d+(?:\.\d+)?元', c_no_date)
                print(c_num2_unit)
            # 写入excel
            index_date = 0  # 标志本月日期的增行数
            index_money_w = 0  # 控制万的增行数
            index_money_y = 0  # 控制元的增行数
            for index, date in enumerate(matches_list):
                if now_month + '/' in date:
                    worksheet.write(row, colx_num + index_date + index_row, date)
                    index_date = index_date + 1
            for index2, c_num in enumerate(c_num_unit):
                c_num = re.findall(r'\d+(?:\.\d+)?', c_num)
                worksheet.write(row, colx_num + index_date + index2 + index_row, int(c_num[0]) * 10000)
                index_money_w = index2 + 1
            for index3, c_num2 in enumerate(c_num2_unit):
                c_num2 = re.findall(r'\d+(?:\.\d+)?', c_num2)
                worksheet.write(row, colx_num + index_date + index_money_w + index3 + index_row, c_num2[0])
                index_money_y = index3 + 1
            index_row = index_date + index_money_w + index_money_y + index_row
    workbook.save(target_file)


def handle_remarks(target_file, now_month):
    """
    处理备注
    :return:
    """
    # 读取修改后的文件
    book = open_excel(target_file)
    sh = book.sheet_by_index(0)
    row_num = sh.nrows
    colx_num = sh.ncols
    # 设置修改文件
    workbook = copy(book)
    worksheet = workbook.get_sheet(0)
    # worksheet.write(0, colx_num, '备注')
    for row in range(1, row_num):
        row_data = sh.row_values(row)
        remarks = row_data[27]
        # 先把备注写到最后一列
        # worksheet.write(row, colx_num, remarks)
        # 处理备注（分成数组，如果数组有月份和数字，把月份和数字向后写）
        com = remarks.split('；')
        index_row = 0
        for c in com:
            # print(c)
            if not (now_month + '/' in c):
                continue
            if not ('变更' in c):
                continue
            # 提取数组里面的日期
            date_reg_exp = re.compile('\d{4}[-/]\d{1,2}[-/]\d{1,2}')
            matches_list = date_reg_exp.findall(c)
            # 把延期日期去掉
            for matches in matches_list:
                c = c.replace('延期' + matches, '')
                c = c.replace('延期到' + matches, '')
            print('----' + c)
            # 拿到变更前后的日期和金额，默认分成两个，可能存在多个变更的情况
            array = c.split('变更')
            for index, str in enumerate(array):
                if index == len(array) - 1:
                    break
                date_reg_exp = re.compile(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}')
                matches_date_list = date_reg_exp.findall(str)
                print(matches_date_list)
                per_reg_exp = re.compile(r"\d+\.\d*%|\d*%")
                matches_per_list = per_reg_exp.findall(array[index + 1])
                print(matches_per_list)
                # 如果包含分之，并且数据的前面无日期或者数据日期为当月日期，取出
                date_fenshu = ''
                fenshu = ''
                if array[index + 1].find("分之") != -1:
                    index_temp = array[index + 1].find("分之")
                    c_bef = array[index + 1][0:index_temp - 1]
                    d_reg_exp = re.compile(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}')
                    m_date_list = d_reg_exp.findall(c_bef)
                    if len(m_date_list) == 0:
                        fenshu = array[index + 1][int(index_temp) - 1: int(index_temp) + 3]
                    elif now_month + '/' in m_date_list[len(m_date_list) - 1]:
                        date_fenshu = m_date_list[len(m_date_list) - 1]
                        fenshu = array[index + 1][int(index_temp) - 1: int(index_temp) + 3]
                    print(date_fenshu)
                    print(fenshu)
                date = matches_date_list[len(matches_date_list) - 1]
                per = matches_per_list[0]
                if now_month + '/' in date:
                    worksheet.write(row, colx_num + index_row, date)
                    worksheet.write(row, colx_num + 1 + index_row, per)
                    # 如果只有百分数
                    if fenshu != '' and date_fenshu == '':
                        worksheet.write(row, colx_num + 2 + index_row, fenshu)
                        index_row = index_row + 1 + 2
                    # 如果有百分数，有日期
                    elif fenshu != '' and date_fenshu != '':
                        worksheet.write(row, colx_num + 2 + index_row, date_fenshu)
                        worksheet.write(row, colx_num + 3 + index_row, fenshu)
                        index_row = index_row + 1 + 3
                    else:
                        index_row = index_row + 1 + 1
                if now_month + '/' in date_fenshu:
                    if fenshu != '' and date_fenshu != '':
                        worksheet.write(row, colx_num + index_row, date_fenshu)
                        worksheet.write(row, colx_num + 1 + index_row, fenshu)
                        index_row = index_row + 2
    workbook.save(target_file)


def time_format(date_value):
    """
    时间格式化 去掉月份，日期前面的0
    :param date_value:
    :return:
    """
    dates = date_value.split('/')
    if len(dates) == 3:
        month = dates[1].lstrip('0')
        day = dates[2].lstrip('0')
        return dates[0] + '/' + month + '/' + day
    elif len(dates) == 2:
        month = dates[1].lstrip('0')
        return dates[0] + '/' + month
    else:
        return date_value


if __name__ == '__main__':
    source_file = r'D:\0RPA\计划财务部\财务rpa\魏丽Excel\科目余额表.xls'
    # source_file = r'C:\Users\LiGuangxi\Desktop\RPA需求\计财\股票质押明细表(仅供参考，请核对).xlsx'
    target_file = r'D:\0RPA\计划财务部\财务rpa\魏丽Excel'
    now_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    # 如果没有源文件，则报错退出
    if not os.path.exists(source_file):
        print("查询不到源文件")
        sys.exit(1)
    # 如果没有目标文件夹，则创建
    target_folder = target_file + '/' + now_time
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    # 当前月
    now_month = time.strftime("%Y/%m", time.localtime(time.time()))
    # ---------------------start：下面可以修改为您处理的任何月份---------------------------------------------------------------------------------------------
    # now_month = '2020/12'
    # ---------------------end：上面可以修改为您处理的任何月份-----------------------------------------------------------------------------------------------
    # 过滤
    filter_sheet(source_file, target_folder, now_month)
    # 加工
    handle_comment(target_folder + '/自有资金-待赎回交易.xlsx', now_month)
    handle_remarks(target_folder + '/自有资金-待赎回交易.xlsx', now_month)
