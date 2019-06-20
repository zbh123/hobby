'''
ui界面转成python的指令是pyuic4 *.ui -o *.py

'''


# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from dialog1 import Dialog1
from dialog2 import Dialog2
import sys

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


class MainWindow(QtGui.QWidget):
    dialog1_signal = QtCore.pyqtSignal()  # 定义一个无参数的信号，串口设定与子站初始化信号
    dialog2_signal = QtCore.pyqtSignal()  # 定义一个无参数的信号，串口设定与子站初始化信号
    exit_signal = QtCore.pyqtSignal()  # 定义一个无参数的信号，串口设定与子站初始化信号

    def __init__(self):
        super(MainWindow, self).__init__()

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.form = Form
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 90, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 90, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 160, 75, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(170, 40, 54, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 信号连接到指定槽
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "进入dialog1", None))
        self.pushButton_2.setText(_translate("Form", "进入dialog2", None))
        self.pushButton_3.setText(_translate("Form", "退出", None))
        self.label.setText(_translate("Form", "主窗体", None))

    def on_pushButton_clicked(self):
        self.form.hide()
        Form1 = QtGui.QDialog()
        ui = Dialog1()
        ui.setupUi(Form1)
        Form1.show()
        Form1.exec_()
        self.form.show()

    def on_pushButton_3_clicked(self, Form):
        # QtCore.QObject.connect( self.pushButton_3, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT(quit()))
        # 也可以这样
        self.form.close()

    def on_pushButton_2_clicked(self):
        self.form.close()
        Form1 = QtGui.QDialog()
        ui = Dialog2()
        ui.setupUi(Form1)
        Form1.show()
        Form1.exec_()
        self.form.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    window = MainWindow()
    window.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

    pass
