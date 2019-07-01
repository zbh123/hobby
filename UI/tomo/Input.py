from PyQt4 import QtCore, QtGui
from excute_c import Worker
import os
import re

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(837, 626)
        self.lamdaEdit = QtGui.QLineEdit(Form)
        self.lamdaEdit.setGeometry(QtCore.QRect(710, 100, 51, 20))
        self.lamdaEdit.setText(_fromUtf8(""))
        self.lamdaEdit.setObjectName(_fromUtf8("lamdaEdit"))

        self.shotpathEdit = QtGui.QLineEdit(Form)
        self.shotpathEdit.setGeometry(QtCore.QRect(130, 200, 221, 20))
        self.shotpathEdit.setObjectName(_fromUtf8("shotpathEdit"))

        self.elevation = QtGui.QLabel(Form)
        self.elevation.setGeometry(QtCore.QRect(430, 250, 61, 20))
        self.elevation.setObjectName(_fromUtf8("elevation"))

        self.v0 = QtGui.QLabel(Form)
        self.v0.setGeometry(QtCore.QRect(200, 100, 21, 20))
        self.v0.setObjectName(_fromUtf8("v0"))

        self.buttonBox = QtGui.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(440, 310, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.dvEdit = QtGui.QLineEdit(Form)
        self.dvEdit.setGeometry(QtCore.QRect(350, 100, 51, 20))
        self.dvEdit.setText(_fromUtf8(""))
        self.dvEdit.setObjectName(_fromUtf8("dvEdit"))

        self.recpathEdit = QtGui.QLineEdit(Form)
        self.recpathEdit.setGeometry(QtCore.QRect(500, 200, 221, 20))
        self.recpathEdit.setObjectName(_fromUtf8("recpathEdit"))

        self.Nz = QtGui.QLabel(Form)
        self.Nz.setGeometry(QtCore.QRect(440, 60, 21, 20))
        self.Nz.setObjectName(_fromUtf8("Nz"))

        self.fb_file = QtGui.QLabel(Form)
        self.fb_file.setGeometry(QtCore.QRect(60, 250, 61, 20))
        self.fb_file.setObjectName(_fromUtf8("fb_file"))

        self.reset = QtGui.QPushButton(Form)
        self.reset.setGeometry(QtCore.QRect(680, 320, 75, 23))
        self.reset.setObjectName(_fromUtf8("reset"))

        self.Nshot = QtGui.QLabel(Form)
        self.Nshot.setGeometry(QtCore.QRect(60, 60, 41, 20))
        self.Nshot.setObjectName(_fromUtf8("Nshot"))

        self.Output = QtGui.QLabel(Form)
        self.Output.setGeometry(QtCore.QRect(400, 360, 41, 41))
        self.Output.setObjectName(_fromUtf8("Output"))

        self.dzEdit = QtGui.QLineEdit(Form)
        self.dzEdit.setGeometry(QtCore.QRect(110, 100, 51, 20))
        self.dzEdit.setObjectName(_fromUtf8("dzEdit"))

        self.niter = QtGui.QLabel(Form)
        self.niter.setGeometry(QtCore.QRect(420, 140, 41, 20))
        self.niter.setObjectName(_fromUtf8("niter"))

        self.dxEdit = QtGui.QLineEdit(Form)
        self.dxEdit.setGeometry(QtCore.QRect(590, 60, 51, 20))
        self.dxEdit.setText(_fromUtf8(""))
        self.dxEdit.setObjectName(_fromUtf8("dxEdit"))

        self.lamda = QtGui.QLabel(Form)
        self.lamda.setGeometry(QtCore.QRect(660, 100, 41, 20))
        self.lamda.setObjectName(_fromUtf8("lamda"))

        self.dv = QtGui.QLabel(Form)
        self.dv.setGeometry(QtCore.QRect(320, 100, 21, 20))
        self.dv.setObjectName(_fromUtf8("dv"))

        self.Nx = QtGui.QLabel(Form)
        self.Nx.setGeometry(QtCore.QRect(200, 60, 21, 20))
        self.Nx.setObjectName(_fromUtf8("Nx"))

        self.NshotEdit = QtGui.QLineEdit(Form)
        self.NshotEdit.setGeometry(QtCore.QRect(110, 60, 51, 20))
        self.NshotEdit.setObjectName(_fromUtf8("NshotEdit"))

        self.NxEdit = QtGui.QLineEdit(Form)
        self.NxEdit.setGeometry(QtCore.QRect(230, 60, 51, 20))
        self.NxEdit.setText(_fromUtf8(""))
        self.NxEdit.setObjectName(_fromUtf8("NxEdit"))

        self.recpath = QtGui.QLabel(Form)
        self.recpath.setGeometry(QtCore.QRect(430, 200, 61, 20))
        self.recpath.setObjectName(_fromUtf8("recpath"))

        self.damp = QtGui.QLabel(Form)
        self.damp.setGeometry(QtCore.QRect(550, 100, 31, 20))
        self.damp.setObjectName(_fromUtf8("damp"))

        self.itmax = QtGui.QLabel(Form)
        self.itmax.setGeometry(QtCore.QRect(300, 140, 41, 20))
        self.itmax.setObjectName(_fromUtf8("itmax"))

        self.delta = QtGui.QLabel(Form)
        self.delta.setGeometry(QtCore.QRect(420, 100, 41, 20))
        self.delta.setObjectName(_fromUtf8("delta"))

        self.itmaxEdit = QtGui.QLineEdit(Form)
        self.itmaxEdit.setGeometry(QtCore.QRect(350, 140, 51, 20))
        self.itmaxEdit.setText(_fromUtf8(""))
        self.itmaxEdit.setObjectName(_fromUtf8("itmaxEdit"))

        self.dampEdit = QtGui.QLineEdit(Form)
        self.dampEdit.setGeometry(QtCore.QRect(590, 100, 51, 20))
        self.dampEdit.setText(_fromUtf8(""))
        self.dampEdit.setObjectName(_fromUtf8("dampEdit"))

        self.dx = QtGui.QLabel(Form)
        self.dx.setGeometry(QtCore.QRect(560, 60, 21, 20))
        self.dx.setObjectName(_fromUtf8("dx"))

        self.NzEdit = QtGui.QLineEdit(Form)
        self.NzEdit.setGeometry(QtCore.QRect(470, 60, 51, 20))
        self.NzEdit.setText(_fromUtf8(""))
        self.NzEdit.setObjectName(_fromUtf8("NzEdit"))

        self.fb_fileEdit = QtGui.QLineEdit(Form)
        self.fb_fileEdit.setGeometry(QtCore.QRect(130, 250, 221, 20))
        self.fb_fileEdit.setObjectName(_fromUtf8("fb_fileEdit"))

        self.line_2 = QtGui.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(60, 380, 701, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))

        self.szEdit = QtGui.QLineEdit(Form)
        self.szEdit.setGeometry(QtCore.QRect(110, 140, 51, 20))
        self.szEdit.setObjectName(_fromUtf8("szEdit"))

        self.line = QtGui.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(60, 20, 701, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        self.out = QtGui.QTextEdit(Form)
        self.out.setGeometry(QtCore.QRect(60, 410, 701, 181))
        self.out.setObjectName(_fromUtf8("textEdit"))

        self.omega = QtGui.QLabel(Form)
        self.omega.setGeometry(QtCore.QRect(180, 140, 41, 20))
        self.omega.setObjectName(_fromUtf8("omega"))

        self.Ny = QtGui.QLabel(Form)
        self.Ny.setGeometry(QtCore.QRect(320, 60, 21, 20))
        self.Ny.setObjectName(_fromUtf8("Ny"))

        self.run = QtGui.QPushButton(Form)
        self.run.setGeometry(QtCore.QRect(590, 320, 75, 23))
        self.run.setObjectName(_fromUtf8("run"))

        self.sz = QtGui.QLabel(Form)
        self.sz.setGeometry(QtCore.QRect(80, 140, 21, 20))
        self.sz.setObjectName(_fromUtf8("sz"))

        self.dyEdit = QtGui.QLineEdit(Form)
        self.dyEdit.setGeometry(QtCore.QRect(710, 60, 51, 20))
        self.dyEdit.setText(_fromUtf8(""))
        self.dyEdit.setObjectName(_fromUtf8("dyEdit"))

        self.Input = QtGui.QLabel(Form)
        self.Input.setGeometry(QtCore.QRect(380, 0, 91, 41))
        self.Input.setObjectName(_fromUtf8("Input"))

        self.shotpath = QtGui.QLabel(Form)
        self.shotpath.setGeometry(QtCore.QRect(60, 200, 61, 20))
        self.shotpath.setObjectName(_fromUtf8("shotpath"))

        self.niterEdit = QtGui.QLineEdit(Form)
        self.niterEdit.setGeometry(QtCore.QRect(470, 140, 51, 20))
        self.niterEdit.setText(_fromUtf8(""))
        self.niterEdit.setObjectName(_fromUtf8("niterEdit"))

        self.NyEdit = QtGui.QLineEdit(Form)
        self.NyEdit.setGeometry(QtCore.QRect(350, 60, 51, 20))
        self.NyEdit.setText(_fromUtf8(""))
        self.NyEdit.setObjectName(_fromUtf8("NyEdit"))

        self.v0Edit = QtGui.QLineEdit(Form)
        self.v0Edit.setGeometry(QtCore.QRect(230, 100, 51, 20))
        self.v0Edit.setText(_fromUtf8(""))
        self.v0Edit.setObjectName(_fromUtf8("v0Edit"))

        self.dy = QtGui.QLabel(Form)
        self.dy.setGeometry(QtCore.QRect(680, 60, 21, 20))
        self.dy.setObjectName(_fromUtf8("dy"))

        self.dz = QtGui.QLabel(Form)
        self.dz.setGeometry(QtCore.QRect(80, 100, 21, 20))
        self.dz.setObjectName(_fromUtf8("dz"))

        self.elevationEdit = QtGui.QLineEdit(Form)
        self.elevationEdit.setGeometry(QtCore.QRect(500, 250, 221, 20))
        self.elevationEdit.setObjectName(_fromUtf8("elevationEdit"))

        self.deltaEdit = QtGui.QLineEdit(Form)
        self.deltaEdit.setGeometry(QtCore.QRect(470, 100, 51, 20))
        self.deltaEdit.setText(_fromUtf8(""))
        self.deltaEdit.setObjectName(_fromUtf8("deltaEdit"))

        self.omegaEdit = QtGui.QLineEdit(Form)
        self.omegaEdit.setGeometry(QtCore.QRect(230, 140, 51, 20))
        self.omegaEdit.setText(_fromUtf8(""))
        self.omegaEdit.setObjectName(_fromUtf8("omegaEdit"))

        self.shot_path = QtGui.QPushButton(Form)
        self.shot_path.setGeometry(QtCore.QRect(350, 200, 31, 23))
        self.shot_path.setObjectName(_fromUtf8("shot_path"))

        self.rec_path = QtGui.QPushButton(Form)
        self.rec_path.setGeometry(QtCore.QRect(720, 200, 31, 23))
        self.rec_path.setObjectName(_fromUtf8("rec_path"))

        self.fb_path = QtGui.QPushButton(Form)
        self.fb_path.setGeometry(QtCore.QRect(350, 250, 31, 23))
        self.fb_path.setObjectName(_fromUtf8("fb_path"))

        self.ele_path = QtGui.QPushButton(Form)
        self.ele_path.setGeometry(QtCore.QRect(720, 250, 31, 23))
        self.ele_path.setObjectName(_fromUtf8("ele_path"))

        self.retranslateUi(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)

        self.thread = Worker()
        self.thread.file_changed_signal.connect(self.update_file_list)

        self.reset.clicked.connect(self.clear)
        self.run.clicked.connect(self.thread_start)
        self.shot_path.clicked.connect(lambda :self.get_file(self.shotpathEdit))
        self.rec_path.clicked.connect(lambda :self.get_file(self.recpathEdit))
        self.fb_path.clicked.connect(lambda :self.get_file(self.fb_fileEdit))
        self.ele_path.clicked.connect(lambda :self.get_file(self.elevationEdit))

    def update_file_list(self, file_inf):
        self.out.append(file_inf)

    def thread_start(self):
        self.get_text()
        self.run.setEnabled(False)
        self.thread.start()

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.elevation.setText(_translate("Form", "elevation:", None))
        self.v0.setText(_translate("Form", "v0:", None))
        self.Nz.setText(_translate("Form", "Nz:", None))
        self.fb_file.setText(_translate("Form", "fb_file:", None))
        self.reset.setText(_translate("Form", "Reset", None))
        self.Nshot.setText(_translate("Form", "Nshot:", None))
        self.Output.setText(_translate("Form", "Output", None))
        self.niter.setText(_translate("Form", "niter:", None))
        self.lamda.setText(_translate("Form", "lamda:", None))
        self.dv.setText(_translate("Form", "dv:", None))
        self.Nx.setText(_translate("Form", "Nx:", None))
        self.recpath.setText(_translate("Form", "recpath:", None))
        self.damp.setText(_translate("Form", "damp:", None))
        self.itmax.setText(_translate("Form", "itmax:", None))
        self.delta.setText(_translate("Form", "delta:", None))
        self.dx.setText(_translate("Form", "dx:", None))
        self.omega.setText(_translate("Form", "omega:", None))
        self.Ny.setText(_translate("Form", "Ny:", None))
        self.run.setText(_translate("Form", "Run", None))
        self.sz.setText(_translate("Form", "sz:", None))
        self.Input.setText(_translate("Form", "Input Parameter", None))
        self.shotpath.setText(_translate("Form", "shotpath:", None))
        self.dy.setText(_translate("Form", "dy:", None))
        self.dz.setText(_translate("Form", "dz:", None))
        self.shot_path.setText(_translate("Form", "...", None))
        self.rec_path.setText(_translate("Form", "...", None))
        self.fb_path.setText(_translate("Form", "...", None))
        self.ele_path.setText(_translate("Form", "...", None))

    def clear(self):
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
        self.shotpathEdit.clear()
        self.recpathEdit.clear()
        self.fb_fileEdit.clear()
        self.elevationEdit.clear()
        self.out.clear()

    def get_file(self, name):
        path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.', 'dat files (*.dat);;All files (*.*)')
        name.setText(path)

    def is_number(self, num):
        pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        result = pattern.match(num)
        if result:
            return True
        else:
            return False

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
            shotname = self.shotpathEdit.text()
            self.write_par(fp, shotname)
            recname = self.recpathEdit.text()
            self.write_par(fp, recname)
            fb_path = self.fb_fileEdit.text()
            self.write_par(fp, fb_path)
            ele = self.elevationEdit.text()
            self.write_par(fp, ele)

    def write_par(self, f, num):
        if self.is_number(num) or os.path.exists(num):
            f.write(num + '\n')
        else:
            self.out.append("%s need be number or path" % num)

    #def start(self):
        #self.get_text()
        # from * import *
        # *

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
