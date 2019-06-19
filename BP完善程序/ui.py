#!/usr/bin/env python
# encoding: utf-8
"""
:author: xiaoxiaobai

:contact: 865816863@qq.com

:file: guiPy.py

:time: 2017/10/3 19:42

:@Software: PyCharm Community Edition

:desc: 该文件完成了主要窗体设计，和数据获取，呈现等操作。调用时，运行主类MainWindow即可

"""
import tkinter as tk
from tkinter import ttk
from dataBaseOpr import *
import tkinter.messagebox


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # 变量定义
        self.opr = OracleOpr()
        self.list = self.init_data()
        self.item_selection = ''
        self.data = []

        # 定义区域，把全局分为上中下三部分
        self.frame_top = tk.Frame(width=600, height=90)
        self.frame_center = tk.Frame(width=600, height=180)
        self.frame_bottom = tk.Frame(width=600, height=90)

        # 定义上部分区域
        self.lb_tip = tk.Label(self.frame_top, text="评议小组名称")
        self.string = tk.StringVar()
        self.string.set('')
        self.ent_find_name = tk.Entry(self.frame_top, textvariable=self.string)
        self.btn_query = tk.Button(self.frame_top, text="查询", command=self.query)
        self.lb_tip.grid(row=0, column=0, padx=15, pady=30)
        self.ent_find_name.grid(row=0, column=1, padx=45, pady=30)
        self.btn_query.grid(row=0, column=2, padx=45, pady=30)

        # 定义下部分区域
        self.btn_delete = tk.Button(self.frame_bottom, text="删除", command=self.delete)
        self.btn_update = tk.Button(self.frame_bottom, text="修改", command=self.update)
        self.btn_add = tk.Button(self.frame_bottom, text="添加", command=self.add)
        self.btn_delete.grid(row=0, column=0, padx=20, pady=30)
        self.btn_update.grid(row=0, column=1, padx=120, pady=30)
        self.btn_add.grid(row=0, column=2, padx=30, pady=30)

        # 定义中心列表区域
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=8, columns=("a", "b", "c", "d"))
        self.vbar = ttk.Scrollbar(self.frame_center, orient=tk.VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column("a", width=80, anchor="center")
        self.tree.column("b", width=120, anchor="center")
        self.tree.column("c", width=120, anchor="center")
        self.tree.column("d", width=120, anchor="center")
        self.tree.heading("a", text="小组编号")
        self.tree.heading("b", text="小组名称")
        self.tree.heading("c", text="负责人")
        self.tree.heading("d", text="联系方式")
        # 调用方法获取表格内容插入及树基本属性设置
        self.tree["selectmode"] = "browse"
        self.get_tree()
        self.tree.grid(row=0, column=0, sticky=tk.NSEW, ipadx=10)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)

        # 定义整体区域
        self.frame_top.grid(row=0, column=0, padx=60)
        self.frame_center.grid(row=1, column=0, padx=60, ipady=1)
        self.frame_bottom.grid(row=2, column=0, padx=60)
        self.frame_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        # 窗体设置
        self.center_window(600, 360)
        self.title('评议小组管理')
        self.resizable(False, False)
        self.mainloop()

    # 窗体居中
    def center_window(self, width, height):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        # 宽高及宽高的初始点坐标
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(size)

    # 数据初始化获取
    def init_data(self):
        result, _ = self.opr.query()
        if self.opr.queryStatus:
            return 0
        else:
            return result

    # 表格内容插入
    def get_tree(self):
        if self.list == 0:
            tkinter.messagebox.showinfo("错误提示", "数据获取失败")
        else:
            # 删除原节点
            for _ in map(self.tree.delete, self.tree.get_children("")):
                pass
            # 更新插入新节点
            for i in range(len(self.list)):
                group = self.list[i]
                self.tree.insert("", "end", values=(group[0],
                                                    group[1],
                                                    group[2],
                                                    group[3]), text=group[0])
            # TODO 此处需解决因主程序自动刷新引起的列表项选中后重置的情况，我采用的折中方法是：把选中时的数据保存下来，作为记录

            # 绑定列表项单击事件
            self.tree.bind("<ButtonRelease-1>", self.tree_item_click)
            self.tree.after(500, self.get_tree)

    # 单击查询按钮触发的事件方法
    def query(self):
        query_info = self.ent_find_name.get()
        self.string.set('')
        # print(query_info)
        if query_info is None or query_info == '':
            tkinter.messagebox.showinfo("警告", "查询条件不能为空！")
            self.get_tree()
        else:
            result, _ = self.opr.query(queryby="where name like '%" + query_info + "%'")
            self.get_tree()
            if self.opr.queryStatus:
                tkinter.messagebox.showinfo("警告", "查询出错，请检查数据库服务是否正常")
            elif not result:
                tkinter.messagebox.showinfo("查询结果", "该查询条件没有匹配项！")
            else:
                self.list = result
                # TODO 此处需要解决弹框后代码列表刷新无法执行的问题

    # 单击删除按钮触发的事件方法
    def delete(self):
        if self.item_selection is None or self.item_selection == '':
            tkinter.messagebox.showinfo("删除警告", "未选中待删除值")
        else:
            # TODO： 删除提示
            self.opr.delete(deleteby="no = '"+self.item_selection+"'")
            if self.opr.deleteStatus:
                tkinter.messagebox.showinfo("删除警告", "删除异常，可能是数据库服务意外关闭了。。。")
            else:
                self.list = self.init_data()
                self.get_tree()

    # 为解决窗体自动刷新的问题，记录下单击项的内容
    def tree_item_click(self, event):
        try:
            selection = self.tree.selection()[0]
            self.data = self.tree.item(selection, "values")
            self.item_selection = self.data[0]
        except IndexError:
            tkinter.messagebox.showinfo("单击警告", "单击结果范围异常，请重新选择！")

    # 单击更新按钮触发的事件方法
    def update(self):
        if self.item_selection is None or self.item_selection == '':
            tkinter.messagebox.showinfo("更新警告", "未选中待更新项")
        else:
            data = [self.item_selection]
            self.data = self.set_info(2)
            if self.data is None or not self.data:
                return
            # 更改参数
            data = data + self.data
            self.opr.update(updatelist=data)
            if self.opr.insertStatus:
                tkinter.messagebox.showinfo("更新小组信息警告", "数据异常库连接异常，可能是服务关闭啦~")
            # 更新界面，刷新数据
            self.list = self.init_data()
            self.get_tree()

    # 单击新增按钮触发的事件方法
    def add(self):
        # 接收弹窗的数据
        self.data = self.set_info(1)
        if self.data is None or not self.data:
            return
        # 更改参数
        self.opr.insert(insertlist=self.data)
        if self.opr.insertStatus:
            tkinter.messagebox.showinfo("新增小组信息警告", "数据异常库连接异常，可能是服务关闭啦~")
        # 更新界面，刷新数据
        self.list = self.init_data()
        self.get_tree()

    # 此方法调用弹窗传递参数，并返回弹窗的结果
    def set_info(self, dia_type):
        """
        :param dia_type:表示打开的是新增窗口还是更新窗口，新增则参数为1，其余参数为更新
        :return: 返回用户填写的数据内容，出现异常则为None
        """
        dialog = MyDialog(data=self.data, dia_type=dia_type)
        # self.withdraw()
        self.wait_window(dialog)  # 这一句很重要！！！
        return dialog.group_info


# 新增窗口或者更新窗口
class MyDialog(tk.Toplevel):
    def __init__(self, data, dia_type):
        super().__init__()

        # 窗口初始化设置，设置大小，置顶等
        self.center_window(600, 360)
        self.wm_attributes("-topmost", 1)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.donothing)   # 此语句用于捕获关闭窗口事件，用一个空方法禁止其窗口关闭。

        # 根据参数类别进行初始化
        if dia_type == 1:
            self.title('新增小组信息')
        else:
            self.title('更新小组信息')

        # 数据变量定义
        self.no = tk.StringVar()
        self.name = tk.StringVar()
        self.pname = tk.StringVar()
        self.pnum = tk.StringVar()
        if not data or dia_type == 1:
            self.no.set('')
            self.name.set('')
            self.pname.set('')
            self.pnum.set('')
        else:
            self.no.set(data[0])
            self.name.set(data[1])
            self.pname.set(data[2])
            self.pnum.set(data[3])

        # 错误提示定义
        self.text_error_no = tk.StringVar()
        self.text_error_name = tk.StringVar()
        self.text_error_pname = tk.StringVar()
        self.text_error_pnum = tk.StringVar()
        self.error_null = '该项内容不能为空!'
        self.error_exsit = '该小组编号已存在!'

        self.group_info = []
        # 弹窗界面布局
        self.setup_ui()

    # 窗体布局设置
    def setup_ui(self):
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.grid(row=0, column=0, padx=160, pady=20)
        tk.Label(row1, text='小组编号：', width=8).pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.no, width=20).pack(side=tk.LEFT)
        tk.Label(row1, textvariable=self.text_error_no, width=20, fg='red').pack(side=tk.LEFT)
        # 第二行
        row2 = tk.Frame(self)
        row2.grid(row=1, column=0, padx=160, pady=20)
        tk.Label(row2, text='小组名称：', width=8).pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.name, width=20).pack(side=tk.LEFT)
        tk.Label(row2, textvariable=self.text_error_name, width=20, fg='red').pack(side=tk.LEFT)
        # 第三行
        row3 = tk.Frame(self)
        row3.grid(row=2, column=0, padx=160, pady=20)
        tk.Label(row3, text='负责人姓名：', width=10).pack(side=tk.LEFT)
        tk.Entry(row3, textvariable=self.pname, width=18).pack(side=tk.LEFT)
        tk.Label(row3, textvariable=self.text_error_pname, width=20, fg='red').pack(side=tk.LEFT)
        # 第四行
        row4 = tk.Frame(self)
        row4.grid(row=3, column=0, padx=160, pady=20)
        tk.Label(row4, text='手机号码：', width=8).pack(side=tk.LEFT)
        tk.Entry(row4, textvariable=self.pnum, width=20).pack(side=tk.LEFT)
        tk.Label(row4, textvariable=self.text_error_pnum, width=20, fg='red').pack(side=tk.LEFT)
        # 第五行
        row5 = tk.Frame(self)
        row5.grid(row=4, column=0, padx=160, pady=20)
        tk.Button(row5, text="取消", command=self.cancel).grid(row=0, column=0, padx=60)
        tk.Button(row5, text="确定", command=self.ok).grid(row=0, column=1, padx=60)

    def center_window(self, width, height):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(size)

    # 点击确认按钮绑定事件方法
    def ok(self):

        self.group_info = [self.no.get(), self.name.get(), self.pname.get(), self.pnum.get()]  # 设置数据
        if self.check_info() == 1:  # 进行数据校验，失败则不关闭窗口
            return
        self.destroy()  # 销毁窗口

    # 点击取消按钮绑定事件方法
    def cancel(self):
        self.group_info = None  # 空！
        self.destroy()

    # 数据校验和用户友好性提示，校验失败返回1，成功返回0
    def check_info(self):
        is_null = 0
        str_tmp = self.group_info
        if str_tmp[0] == '':
            self.text_error_no.set(self.error_null)
            is_null = 1
        if str_tmp[1] == '':
            self.text_error_name.set(self.error_null)
            is_null = 1
        if str_tmp[2] == '':
            self.text_error_pname.set(self.error_null)
            is_null = 1
        if str_tmp[3] == '':
            self.text_error_pnum.set(self.error_null)
            is_null = 1

        if is_null == 1:
            return 1
        res, _ = OracleOpr().query(queryby="where no = '"+str_tmp[0]+"'")
        print(res)
        if res:
            self.text_error_no.set(self.error_exsit)
            return 1
        return 0

    # 空函数
    def donothing(self):
        pass

