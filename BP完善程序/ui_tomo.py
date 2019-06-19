import os
import re
import tkinter as tk
# from tkinter import ttk
from tkinter import filedialog


class MainGui():
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('3D VTI Tomo')
        self.win.geometry('800*800+200+20')

    def openfile(self):
        filename = filedialog.askopenfilenames(title='打开dat文件', filetypes=[('dat file', '*.dat'), ('All Files', '*')])
        return filename

    def setMenu(self):
        #菜单栏
        menubar = tk.Menu(self.win)
        #文件栏
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label='打开', command=self.openfile())
        filemenu.add_command(label='Save', command=self.openfile())
        # 分割线
        filemenu.add_separator()
        filemenu.add_command(label='Exist', command=self.win.quit)
        menubar.config(menu=menubar)

    def openfile1(self, entry_file):
        path = filedialog.askdirectory()
        entry_file.insert('insert', path)

    def set_top_content(self, canvas_top):

        canvas_top.creat_line((0,15),(720,15), width=5, fill='gray')
        canvas_top.creat_text((360,15), text="Input")
        # place设置相对宽relwidth高relheight和相对位置relx， rely
        tk.Label(canvas_top, text="Nshot:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.1, rely=0.1)
        nshot = tk.StringVar()
        self.nshotEntry = tk.Entry(canvas_top, textvariable=nshot)
        self.nshotEntry.place(relwidth=0.1, relheight=0.1, relx=0.2, rely=0.1)
        nshot.set(100)

        tk.Label(canvas_top, text="Nx:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.31, rely=0.1)
        nx = tk.StringVar()
        self.nxEntry = tk.Entry(canvas_top, textvariable=nx)
        self.nxEntry.place(relwidth=0.1, relheight=0.1, relx=0.41, rely=0.1)
        nx.set(150)

        tk.Label(canvas_top, text="Ny:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.52, rely=0.1)
        ny = tk.StringVar()
        self.nyEntry = tk.Entry(canvas_top, textvariable=ny)
        self.nyEntry.place(relwidth=0.1, relheight=0.1, relx=0.62, rely=0.1)
        ny.set(460)

        tk.Label(canvas_top, text="Nz:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.73, rely=0.1)
        nz = tk.StringVar()
        self.nzEntry = tk.Entry(canvas_top, textvariable=nz)
        self.nzEntry.place(relwidth=0.1, relheight=0.1, relx=0.83, rely=0.1)
        nz.set(100)
        #
        tk.Label(canvas_top, text="dx:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.1, rely=0.25)
        dx = tk.StringVar()
        self.dxEntry = tk.Entry(canvas_top, textvariable=dx)
        self.dxEntry.place(relwidth=0.1, relheight=0.1, relx=0.2, rely=0.25)
        dx.set(10)

        tk.Label(canvas_top, text="dy:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.31, rely=0.25)
        dy = tk.StringVar()
        self.dyEntry = tk.Entry(canvas_top, textvariable=dy)
        self.dyEntry.place(relwidth=0.1, relheight=0.1, relx=0.41, rely=0.25)
        dy.set(10)

        tk.Label(canvas_top, text="dz:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.52, rely=0.25)
        dz = tk.StringVar()
        self.dzEntry = tk.Entry(canvas_top, textvariable=dz)
        self.dzEntry.place(relwidth=0.1, relheight=0.1, relx=0.62, rely=0.25)
        dz.set(10)

        tk.Label(canvas_top, text="v0:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.73, rely=0.25)
        v0 = tk.StringVar()
        self.v0Entry = tk.Entry(canvas_top, textvariable=v0)
        self.v0Entry.place(relwidth=0.1, relheight=0.1, relx=0.83, rely=0.25)
        v0.set(1500)
        #
        tk.Label(canvas_top, text="dv:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.1, rely=0.4)
        dv = tk.StringVar()
        self.dvEntry = tk.Entry(canvas_top, textvariable=dv)
        self.dvEntry.place(relwidth=0.1, relheight=0.1, relx=0.2, rely=0.4)
        dv.set(10)

        tk.Label(canvas_top, text="delta:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.31, rely=0.4)
        delta = tk.StringVar()
        self.deltaEntry = tk.Entry(canvas_top, textvariable=delta)
        self.deltaEntry.place(relwidth=0.1, relheight=0.1, relx=0.41, rely=0.4)
        delta.set(0.5)

        tk.Label(canvas_top, text="damp:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.52, rely=0.4)
        damp = tk.StringVar()
        self.dampEntry = tk.Entry(canvas_top, textvariable=damp)
        self.dampEntry.place(relwidth=0.1, relheight=0.1, relx=0.62, rely=0.4)
        damp.set(0.5)

        tk.Label(canvas_top, text="lamda:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.73, rely=0.4)
        lamda = tk.StringVar()
        self.lamdaEntry = tk.Entry(canvas_top, textvariable=lamda)
        self.lamdaEntry.place(relwidth=0.1, relheight=0.1, relx=0.83, rely=0.4)
        lamda.set(0.5)
        #
        tk.Label(canvas_top, text="sz:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.1, rely=0.55)
        sz = tk.StringVar()
        self.szEntry = tk.Entry(canvas_top, textvariable=sz)
        self.szEntry.place(relwidth=0.1, relheight=0.1, relx=0.2, rely=0.55)
        sz.set(10)

        tk.Label(canvas_top, text="omega:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.31, rely=0.55)
        omega = tk.StringVar()
        self.omegaEntry = tk.Entry(canvas_top, textvariable=omega)
        self.omegaEntry.place(relwidth=0.1, relheight=0.1, relx=0.41, rely=0.55)
        omega.set(0.5)

        tk.Label(canvas_top, text="itmax:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.52, rely=0.55)
        itmax = tk.StringVar()
        self.itmaxEntry = tk.Entry(canvas_top, textvariable=itmax)
        self.itmaxEntry.place(relwidth=0.1, relheight=0.1, relx=0.62, rely=0.55)
        itmax.set(800)

        tk.Label(canvas_top, text="niter:", fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.73, rely=0.55)
        niter = tk.StringVar()
        self.niterEntry = tk.Entry(canvas_top, textvariable=niter)
        self.niterEntry.place(relwidth=0.1, relheight=0.1, relx=0.83, rely=0.55)
        niter.set(3)

        #循环设置多个默认值
        # index_y = 0
        # count = 0
        # for index, para in enumerate(['Nshot', 'Nx', 'Ny', 'Nz', 'dx', 'dy', 'dz', 'v0', 'dv', 'delta', 'damp', 'sz', 'omega', 'itmax', 'niter']):
        #     if index + 1 > 4 + 4*count:
        #         count += 1
        #         index_y +=1
        #     index = index - 4*count
        #     tk.Label(canvas_top, text="%s:"%para, fg='blue').place(relwidth=0.1, relheight=0.1, relx=0.1 + (index*0.21), rely=0.1 + (index_y*0.15))
        #     vari = tk.StringVar()
        #     self.szEntry = tk.Entry(canvas_top, textvariable=vari).place(relwidth=0.1, relheight=0.1, relx=0.2 + (index*0.21), rely=0.1 + (index_y*0.15))
        #     vari.set(0.1)

        scriptPath = os.path.split(os.path.abspath(__file__))[0]
        shotpath = tk.StringVar()
        self.shotEntry = tk.Entry(canvas_top, textvariable=shotpath)
        self.shotEntry.place(relwidth=0.3, relheight=0.1, relx=0.1, rely=0.7)
        shotpath.set(scriptPath)

        button_shot = tk.Button(canvas_top, text='Choose Path', command=lambda :self.openfile1(self.shotEntry))
        button_shot.place(relwidth=0.1, relheight=0.1, relx=0.4, rely=0.7)

    def define_print(self):
        #output information and 滚动条
        frame_bottom = tk.Frame(self.win)
        frame_bottom.place(relwidth=0.9, relheight=0.2, relx=0.05, rely=0.8)
        scrob = tk.Scrollbar(frame_bottom)
        scrob.pack(side=RIGHT, fill=Y)
        self.print_line = tk.Text(frame_bottom, ysrollcommand=scrob.set)
        self.print_line.place(relwidth=0.976, relheight=1)
        scrob.config(command=self.print_line)

    def is_number(self, num):
        pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        result = pattern.match(num)
        if result:
            return True
        else:
            return False

    def write_par(self, f, num):
        if self.is_number(num) or os.path.exists(num):
            f.write(num + '\n')
        else:
            self.print_line.insert(END, "%s need be number or path\n"%num)

    def getpara(self):
        with open('Tomo.par', 'w') as fp:
            nshot = self.nshotEntry.get()
            self.write_par(fp, nshot)
            nx = self.nxEntry.get()
            self.write_par(fp, nx)
            ny = self.nyEntry.get()
            self.write_par(fp, ny)
            ny = self.nyEntry.get()
            self.write_par(fp, ny)
            nz = self.nzEntry.get()
            self.write_par(fp, nz)
            dx = self.dxEntry.get()
            self.write_par(fp, dx)
            dy = self.dyEntry.get()
            self.write_par(fp, dy)
            dz = self.dzEntry.get()
            self.write_par(fp, dz)
            v0 = self.v0Entry.get()
            self.write_par(fp, v0)
            dv = self.dvEntry.get()
            self.write_par(fp, dv)
            delta = self.deltaEntry.get()
            self.write_par(fp, delta)
            damp = self.dampEntry.get()
            self.write_par(fp, damp)
            lamda = self.lamdaEntry.get()
            self.write_par(fp, lamda)
            sz = self.szEntry.get()
            self.write_par(fp, sz)
            omega = self.omegaEntry.get()
            self.write_par(fp, omega)
            itmax = self.itmaxEntry.get()
            self.write_par(fp, itmax)
            niter = self.niterEntry.get()
            self.write_par(fp, niter)

    def run(self):
        self.getpara()

    def clear(self):
        self.nshotEntry.delete(0, END)
        self.nxEntry.delete(0, END)
        self.nyEntry.delete(0, END)
        self.nzEntry.delete(0, END)
        self.dxEntry.delete(0, END)
        self.dyEntry.delete(0, END)
        self.dzEntry.delete(0, END)
        self.v0Entry.delete(0, END)
        self.dvEntry.delete(0, END)
        self.deltaEntry.delete(0, END)
        self.dampEntry.delete(0, END)
        self.lamdaEntry.delete(0, END)
        self.szEntry.delete(0, END)
        self.omegaEntry.delete(0, END)
        self.itmaxEntry.delete(0, END)
        self.niterEntry.delete(0, END)

    def mainUi(self):

        self.setMenu()

        canvas_top = tk.Canvas(self.win, bg='red')
        canvas_top.place(relwidth=0.9, relheight=0.5, relx=0.05, rely=0.01)
        self.define_print()

        self.set_top_content(canvas_top)

        button_start = tk.Button(canvas_top, text="Run", command=self.run)
        button_start.place(relwidth=0.1, relheight=0.1, relx=0.88, rely=0.88)

        button_start = tk.Button(canvas_top, text="Clear", command=self.clear)
        button_start.place(relwidth=0.1, relheight=0.1, relx=0.77, rely=0.88)

        self.win.mainloop()























