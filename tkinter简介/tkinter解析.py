
import tkinter


#创建主窗口
win = tkinter.Tk()

#设置标题
win.title('heheh')
#设置大小和位置
win.geometry('400x400+200+20')
#进入消息循环

'''
Label :标签控件可以显示文本
'''

#win 父窗体

#Label 控件
# label = tkinter.Label(win, text="good",
#                       bg = "pink",
#                       fg = "red",
#                       font = ('黑体',15),
#                       width = 100,
#                       height = 10,
#                       wraplength = 10,
#                       justify = "left")
# #显示出来
# label.pack()

#Button控件
# def func():
#     print('hahahah')
#
# button1 = tkinter.Button(win, text='按钮',command=func, width=10, height=10)
# button1.pack()
# button1 = tkinter.Button(win, text='按钮',command=win.quit, width=10, height=10)
# button1.pack()

'''
Entry:输入控件
用于显示简单文本内容
'''
#绑定变量
# e = tkinter.Variable()
# #show 密文显示 show = '*'
# entry = tkinter.Entry(win,textvariable=e)
# entry = tkinter.Entry(win,show='*')
# entry.pack()
# e.set('hahahhhh')

'''
点击按钮输入输出框中内容
'''
# def showInfo():
#     print(entry.get())
# entry = tkinter.Entry(win)
# entry.pack()
# button = tkinter.Button(win, text='按钮', command=showInfo)
# buttom.pack()

'''
文本控件，用于显示多行文本
'''

#height显示行数
#创建滚动条
# scroll = tkinter.Scrollbar()
# text = tkinter.Text(win, width=30, height=4)
#
# #side放在窗体的那一侧，fill填充
# scroll.pack(side = tkinter.RIGHT, fill=tkinter.Y)
# text.pack(side=tkinter.LEFT, fill=tkinter.Y)
# #关联滚动条和text文件
# scroll.config(command=text.yview)
# text.config(yscrollcommand=scroll.set)
#
# str = '''snkjsnvjksdbvskjdfsd
# aslkfndjksnfkdjs
# sdknfkjsdhahdjuk'''
# text.insert(tkinter.INSERT,str)


'''
CheckButton多选框控件
'''

# def update():
#     message = ""
#     if hobby1.get() == True:
#         message += "money\n"
#     if hobby2.get() == True:
#         message += "power\n"
#     if hobby3.get() == True:
#         message += "beauty\n"
#     #清除text中的所有内容
#     text.deleta(0.0, tkinter.END)
#     #显示选中内容
#     text.insert(tkinter.INSERT,message)
#
# #布尔型，要绑定的变量
# hobby1 = tkinter.BooleanVar()
# #多选框
# check1 = tkinter.Checkbutton(win,text="money", variable=hobby1,command=update)
# check1.pack()
#
# hobby2 = tkinter.BooleanVar()
# check2 = tkinter.Checkbutton(win,text="power", variable=hobby2,command=update)
# check2.pack()
#
# hobby3 = tkinter.BooleanVar()
# check3 = tkinter.Checkbutton(win,text="beauty", variable=hobby3,command=update)
# check3.pack()
#
# text = tkinter.Text(win, width=50, height = 5)
# text.pack()

'''
Radiobutton单选框
'''

# def update():
#     print(r.get())
#
# r = tkinter.StringVar()
# radio1 = tkinter.Radiobutton(win, text="one", value="good", variable = r, command=update)
# radio1.pack()
#
# r = tkinter.IntVar()
# radio2 = tkinter.Radiobutton(win, text="one", value=1, variable = r, command=update)
# radio2.pack()


'''
Listbox1列表框控件，可以包含一个或多个文本框，（下拉选项框）
作用：在listbox控件的小窗口显示一个字符串
'''

# lb = tkinter.Listbox(win, selectmode=tkinter.BROWSE)

#
# lb.pack
# for item in ['good', 'nice', 'money','power', 'beauty']:
#     #按顺序添加
#     lb.insert(tkinter.END, item)
#
# #在开始添加
# lb.insert(tkinter.ACTIVE,'money')
# #将列表当成一个元素添加
# lb.insert(tkinter.END,['heheh','hahah'])
# #删除，参数1为开始索引，参数2为结束索引，如果不指定参数2，只删除第一个索引的内容
# lb.delete(1,3)
# lb.delete(1)
#
# #选中2-4
# lb.select_set(2,4)
# #取消选中
# lb.select_clear(2,4)
# #获取列表中的元素个数
# print(lb.size())
# #获取值
# print(lb.get(2,4))
#
# #当前选中的索引项
# print(lb.curselection())
#
# #判断一个选项是否被选中
# print(lb.selection_include(1))


'''
Listbox2列表框控件，可以包含一个或多个文本框，（下拉选项框）
作用：在listbox控件的小窗口显示一个字符串
'''
#不随鼠标变动而变动

# lbv = tkinter.StringVar()
# lb = tkinter.Listbox(win, selectmode=tkinter.SINGLE, listvariable=lbv)
# lb.pack()
# for item in ['111','222','333']:
#     lb.insert(tkinter.END, item)
#
# #打印当前列表中的选项
# print(lbv.get())
#
# lbv.set(('1','2','3'))
# #绑定事件
# def myPrint(event):
#     print(lb.get(lb.curselection()))
# lb.bind("<Double-Button-1>", myPrint)

'''
Listbox3支持shift和ctrl
'''

#EXTENDED  可以使listbox支持shift和ctrl
# lb = tkinter.Listbox(win, selectmode=tkinter.EXTENDED, listvariable=lbv)
# lb.pack()
# for item in ['111','222','333']:
#     lb.insert(tkinter.END, item)
#
# sc = tkinter.Scrollbar(win)
# sc.pack(side=tkinter.RIGHT,fill=tkinter.Y)
# lb.configure(yscrollcommand=sc.set)
# lb.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
# sc['command']=lb.yview

'''
Listbox3支持自动多选（无需按住shift和ctrl）
'''

# EXTENDED  可以使listbox支持shift和ctrl
# lb = tkinter.Listbox(win, selectmode=tkinter.MULTIPLE, listvariable=lbv)
# lb.pack()
# for item in ['111', '222', '333']:
#     lb.insert(tkinter.END, item)
#
# sc = tkinter.Scrollbar(win)
# sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# lb.configure(yscrollcommand=sc.set)
# lb.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
# sc['command'] = lb.yview

'''
Scale供用户通过拖拽指示器改变变量的值，可以水平HORIZONTAL也可以竖直VERTICAL
'''

# scale = tkinter.Scale(win, from_ = 0, to = 100, orient = tkinter.HORIZONTAL, tickinterval = 10, length=200)
# scale.pack()
#
# #设置值
# scale.set(20)
# #取值
# def showNum:
#     print(scale.get())
# tkinter.Button(win,text = "按钮", command=showNum).pack()

'''
Spinbox数值范围控制
'''

#绑定变量
# v = tkinter.SpringVar()
#
# #increment 步长
# #values项显示值的元组
# sp = tkinter.Spinbox(win, from_=0, to = 100, increment=5, textvariable = v)
# sp.pack()
#
# #设置值
# v.set(20)
# #取值
# print(v.get(10))

'''
Menu 顶层菜单,没有get选项时，可以添加变量
'''

#创建菜单条
# menubar = tkinter.Menu(win)
# win.config(menu=menubar)
# menu1 = Menu(menubar, tearoff=False)
#
# #向菜单选项中添加内容
# def func():
#     print('hhh')
#
# for item in ['C','C++','Python','Java','PHP', 'quit']:
#     if item == 'quit':
#         menu1.add_separator()
#         menu1.add_command(label=item, command=win.quit)
#     else:
#         menu1.add_command(label=item, command=func)
#
# #向菜单条上添加菜单选项
# menubar.add_cascade(lable='语言', menu=menu1)
#
# menu2 = = Menu(menubar, tearoff=False)
# menu1.add_command(label='red')
# menu1.add_command(label='blue')
# menubar.add_cascade(lable='颜色', menu=menu2)


'''
Menu鼠标右键菜单
'''
menubar = tkinter.Menu(win)
menu = tkinter.Menu(menubar, tearoff = False)
for item in ['C','C++','Python','Java','PHP', 'quit']:
    if item == 'quit':
        menu1.add_separator()
        menu1.add_command(label=item, command=win.quit)
    else:
        menu1.add_command(label=item)

menubar.add_cascade(label = '语言', menu=menu)

def showMenu(event):
    menubar.post(event.x_root, event.y_root)
win.bind("<Button-3>",showMenu)

'''
Combobox下拉控件
'''

from tkinter import ttk
#绑定变量
cv = tkinter.StringVar()
com = ttk.Combobox(win, textvariable=cv)
com.pack()
#设置下拉数据
com['value'] = ('济南','济宁','潍坊')
#设置默认值
com.current(0)

#绑定事件
def func(event):
    print(com.get())
com.bind('<<ComboboxSelected>>',func)

'''
Frame控件，框架控件
在屏幕上显示一个矩形区域，多作为容器控件
'''
frm = tkinter.Frame(win)
frm.pack()

#left
frm_l = tkinter.Frame(frm)
tkinter.Lable(frm_l,text='左上',bg='pink').pack(side=tkinter.TOP)
tkinter.Lable(frm_l,text='左下',bg='blue').pack(side=tkinter.TOP)
frm_l.pack(side=tkinter.LEFT)

#Right
frm_r = tkinter.Frame(frm)
tkinter.Lable(frm_r,text='左上',bg='red').pack(side=tkinter.TOP)
tkinter.Lable(frm_r,text='左下',bg='yellow').pack(side=tkinter.TOP)
frm_r.pack(side=tkinter.RIGHT)


'''
表格数据
'''

from tkinter import ttk

tree = ttk.Treeview(win)
#定义列
tree['columns'] = ('姓名','年龄','身高','体重')
#设置列,不显示列
tree.column('姓名', width=100)
tree.column('年龄', width=100)
tree.column('身高', width=100)
tree.column('体重', width=100)

#设置表头，显示列
tree.heading('姓名',text='姓名-name')
tree.heading('年龄',text='年龄-age')
tree.heading('身高',text='身高-height')
tree.heading('体重',text='体重-weight')

#添加数据顺序是0,1，
tree.insert("", 0, text='line1',values=('lulu','23','175','56'))
tree.insert("", 1, text='line2',values=('luyu','24','171','66'))


'''
树状数据，类似于目录
'''
from tkinter import ttk

tree = ttk.Treeview(win)
tree.pack()

#添加一级树枝
treeF1 = tree.insert("", 0, '中国', text= 'China', values=('F1'))
treeF2 = tree.insert("", 1, '美国', text= 'USA', values=('F2'))
treeF3 = tree.insert("", 2, '英国', text= 'UK', values=('F3'))

#添加二级树枝
treeF1_1 = tree.insert(treeF1,0,'上海',text = '上海')
treeF1_2 = tree.insert(treeF1,1,'北京',text = '北京')
treeF1_3 = tree.insert(treeF1,2,'济南',text = '济南')

'''
绝对布局
'''

label1 = tkinter.Label(win,text='good',bg='blue')
label2 = tkinter.Label(win,text='nice',bg='red')
label3 = tkinter.Label(win,text='cool',bg='black')

#绝对布局,窗体改变对控件没影响

label1.place(x=10, y=10)
label2.place(x=50, y=50)
label3.place(x=100, y=100)

'''
相对布局
'''
label1 = tkinter.Label(win,text='good',bg='blue')
label2 = tkinter.Label(win,text='nice',bg='red')
label3 = tkinter.Label(win,text='cool',bg='black')

#相对布局

label1.pack(fill=tkinter.Y, side = tkinter.LEFT)
label2.pack(fill=tkinter.X, side = tkinter.TOP)
label3.pack(fill=tkinter.Y, side = tkinter.RIGHT)

'''
表格布局
'''
label1 = tkinter.Label(win,text='good',bg='blue')
label2 = tkinter.Label(win,text='nice',bg='red')
label3 = tkinter.Label(win,text='cool',bg='black')
label4 = tkinter.Label(win,text='hand',bg='yellow')

#表格布局
label1.grid(row=0,column=0)
label1.grid(row=0,column=1)
label1.grid(row=1,column=0)
label1.grid(row=1,column=1)

'''
鼠标点击事件,<Button-1>左键，<Button-2>中键，<Button-3>右键,<Double-Button-1>左键双击，<Double-Button-3>右键双击
'''

def func(event):
    print(event.x, event.y)
button1 = tkinter.Button(win,text='左击')
button1.bind('<Double-Button-1>',func)
button1.pack()

'''
鼠标移动事件
'''

label = tkinter.Label(win, text='hhh')
label.pack()
def func(event):
    print(event.x,event.y)
label.bind('<B1-Motion>',func)

'''
鼠标释放事件
'''

label = tkinter.Label(win,text='hhh')
label.pack()
def func(event):
    print(event.x,event.y)
label.bind('<ButtonReleased-1>',func)

'''
进入事件<Enter>,离开<Leave>
'''
label = tkinter.Label(win,text='hhh')
label.pack()
def func(event):
    print(event.x,event.y)
label.bind('<Enter>',func)

'''
响应所有按键事件
'''

label = tkinter.Label(win,text='hhh')
#设置焦点
label.focus_set()
label.pack()
def func(event):
    print('event.char = ',event.char)
    print('event.keycode = ',event.keycode)
label.bind('<Key>',func)


'''
相应特殊按键事件
'''
label = tkinter.Label(win,text='hhh')
#设置焦点
label.focus_set()
label.pack()
def func(event):
    print('event.char = ',event.char)
    print('event.keycode = ',event.keycode)
label.bind('<Shift_L>',func)


win.mainloop()















