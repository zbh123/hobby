from xlrd import xldate_as_tuple
import xlrd
import datetime


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


excel_file = r'D:\0RPA\计划财务部\信用业务\20200729\市场交易统计_天.xlsx'
book = open_excel(excel_file)  # 打开excel文件
sheets = book.sheet_names()  # 获取所有sheet表名
for sheet in sheets:
    sh = book.sheet_by_name(sheet)  # 打开每一张表
    row_num = sh.nrows
    num = 0  # 用来计数
    flag = 0  # 失败标志
    count = 0  # 控制失败次数
    i = 2
    while i < row_num:

        row_data = sh.row_values(i)  # 按行获取excel的值
        value = []
        if row_data[2] == '':
            i += 1
            continue
        for j in range(len(row_data)):
            # Python读Excel，返回的单元格内容的类型有5种：
            # ctype： 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
            ctype = sh.cell(i, j).ctype

            # ctype =3,为日期
            if ctype == 3:
                date = xlrd.xldate.xldate_as_datetime(row_data[j], 0)
                cell = date.strftime('%Y-%m-%d')  # ('%Y/%m/%d %H:%M:%S')
                print(cell)
                value.append(cell)
            else:
                value.append(row_data[j])
        print(value)
        i += 1
