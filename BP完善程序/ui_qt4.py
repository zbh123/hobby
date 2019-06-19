import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import re
import os

class ParaFrame(QtGui.QWidget):
    def __init__(self):
        super(ParaFrame, self).__init__()

        self.initUI()

    def initUI(self):
        Nshot = QtGui.QLabel('Nshot')
        self.NshotEdit = QtGui.QLineEdit()
        Nx = QtGui.QLabel('Nx')
        self.NxEdit = QtGui.QLineEdit()
        Ny = QtGui.QLabel('Ny')
        self.NyEdit = QtGui.QLineEdit()
        Nz = QtGui.QLabel('Nz')
        self.NzEdit = QtGui.QLineEdit()
        dx = QtGui.QLabel('dx')
        self.dxEdit = QtGui.QLineEdit()
        dy = QtGui.QLabel('dy')
        self.dyEdit = QtGui.QLineEdit()
        dz = QtGui.QLabel('dz')
        self.dzEdit = QtGui.QLineEdit()
        v0 = QtGui.QLabel('v0')
        self.v0Edit = QtGui.QLineEdit()
        dv = QtGui.QLabel('dv')
        self.dvEdit = QtGui.QLineEdit()
        delta = QtGui.QLabel('delta')
        self.deltaEdit = QtGui.QLineEdit()
        damp = QtGui.QLabel('damp')
        self.dampEdit = QtGui.QLineEdit()
        lamda = QtGui.QLabel('lamda')
        self.lamdaEdit = QtGui.QLineEdit()
        sz = QtGui.QLabel('sz')
        self.szEdit = QtGui.QLineEdit()
        omega = QtGui.QLabel('omega')
        self.omegaEdit = QtGui.QLineEdit()
        itmax = QtGui.QLabel('itmax')
        self.itmaxEdit = QtGui.QLineEdit()
        niter = QtGui.QLabel('niter')
        self.niterEdit = QtGui.QLineEdit()

        grid = QtGui.QGridLayout()

        grid.addWidget(Nshot, 0, 0)
        grid.addWidget(self.NshotEdit, 0, 1)

        grid.addWidget(Nx, 0, 2)
        grid.addWidget(self.NxEdit, 0, 3)

        grid.addWidget(Ny, 0, 4)
        grid.addWidget(self.NyEdit, 0, 5)

        grid.addWidget(Nz, 0, 6)
        grid.addWidget(self.NzEdit, 0, 7)

        grid.addWidget(dx, 1, 0)
        grid.addWidget(self.dxEdit, 1, 1)

        grid.addWidget(dy, 1, 2)
        grid.addWidget(self.dyEdit, 1, 3)

        grid.addWidget(dz, 1, 4)
        grid.addWidget(self.dzEdit, 1, 5)

        grid.addWidget(v0, 1, 6)
        grid.addWidget(self.v0Edit, 1, 7)

        grid.addWidget(dv, 2, 0)
        grid.addWidget(self.dvEdit, 2, 1)

        grid.addWidget(delta, 2, 2)
        grid.addWidget(self.deltaEdit, 2, 3)

        grid.addWidget(damp, 2, 4)
        grid.addWidget(self.dampEdit, 2, 5)

        grid.addWidget(lamda, 2, 6)
        grid.addWidget(self.lamdaEdit, 2, 7)

        grid.addWidget(sz, 3, 0)
        grid.addWidget(self.szEdit, 3, 1)

        grid.addWidget(omega, 3, 2)
        grid.addWidget(self.omegaEdit, 3, 3)

        grid.addWidget(itmax, 3, 4)
        grid.addWidget(self.itmaxEdit, 3, 5)

        grid.addWidget(niter, 3, 6)
        grid.addWidget(self.niterEdit, 3, 7)

        shotPath = QtGui.addWidget('shot path')
        grid.addWidget(shotPath, 4, 0)
        self.shotname = QtGui.QLineEdit()
        shot_path = QtGui.QPushButton()
        shot_path.setText('Browse')
        grid.addWidget(self.shotname, 4, 1, 1, 2)
        grid.addWidget(shot_path, 4, 3)
        self.connect(shot_path, QtCore.SIGNAL("clicked()"), lambda : self.button_click(self.shotname))

        recPath = QtGui.addWidget('rec path')
        grid.addWidget(recPath, 4, 0)
        self.recname = QtGui.QLineEdit()
        rec_path = QtGui.QPushButton()
        rec_path.setText('Browse')
        grid.addWidget(self.recname, 4, 1, 1, 2)
        grid.addWidget(rec_path, 4, 3)
        self.connect(rec_path, QtCore.SIGNAL("clicked()"), lambda : self.button_click(self.recname))

        self.out = QtGui.QTextEdit()
        grid.addWidget(self.out, 6, 0, 3, 8)

        self.clear = QtGui.QPushButton()
        self.clear.setText('Clear')
        grid.addWidget(self.clear, 5, 6)
        self.connect(self.clear, QtCore.SIGNAL('clicked()'), self.clear_input)

        self.run = QtGui.QPushButton()
        self.run.setText('Run')
        grid.addWidget(self.run, 5, 7)
        self.connect(self.run, QtCore.SIGNAL('clicked()'), self.start)

        self.setLayout(grid)
        self.setWindowTitle('Input Parameter')
        self.resize(800, 500)


    def button_click(self, name):
        path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.', 'dat file(*.dat);;All files(*.*)')
        name.setText(path)

    def clear_input(self):
        self.NshotEdit.clear()
        self.NxEdit.clear()
        self.NyEdit.clear()
        self.NzEdit.clear()
        self.dxEdit.clear()
        self.dyEdit.clear()
        self.dzEdit.clear()
        self.v0Edit.clear()
        self.dvEdit.clear()
        self.deltaEdit.clear()
        self.dampEdit.clear()
        self.lamdaEdit.clear()
        self.szEdit.clear()
        self.omegaEdit.clear()
        self.itmaxEdit.clear()
        self.niterEdit.clear()
        self.shotname.clear()
        self.recname.clear()


    def start(self):
        self.get_text()
        from tomo import *
        self.out.append('Start')

    def get_text(self):
        with open('tomo.par', 'w') as fp:
            Nshot = self.NshotEdit.text()
            self.write_par(fp, Nshot)
            Nx = self.NxEdit.text()
            self.write_par(fp, Nx)
            Ny = self.NyEdit.text()
            self.write_par(fp, Ny)
            Nz = self.NzEdit.text()
            self.write_par(fp, Nz)
            dx = self.dxEdit.text()
            self.write_par(fp, dx)
            dy = self.dyEdit.text()
            self.write_par(fp, dy)
            dz = self.dzEdit.text()
            self.write_par(fp, dz)
            v0 = self.v0Edit.text()
            self.write_par(fp, v0)
            dv = self.dvEdit.text()
            self.write_par(fp, dv)
            delta = self.deltaEdit.text()
            self.write_par(fp, delta)
            damp = self.dampEdit.text()
            self.write_par(fp, damp)
            lamda = self.lamdaEdit.text()
            self.write_par(fp, lamda)
            sz = self.szEdit.text()
            self.write_par(fp, sz)
            omega = self.omegaEdit.text()
            self.write_par(fp, omega)
            itmax = self.itmaxEdit.text()
            self.write_par(fp, itmax)
            niter = self.niterEdit.text()
            self.write_par(fp, niter)
            shotname = self.shotname.text()
            self.write_par(fp, shotname)
            recname = self.recname.text()
            self.write_par(fp, recname)

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
            self.out.append("%s need be number or path"%num)









