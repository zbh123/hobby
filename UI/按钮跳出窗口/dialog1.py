# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

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


class Dialog1(QtGui.QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.form = Dialog
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 50, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.dialog1_pushButton = QtGui.QPushButton(Dialog)
        self.dialog1_pushButton.setGeometry(QtCore.QRect(160, 130, 75, 23))
        self.dialog1_pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # 信号连接到指定槽
        self.dialog1_pushButton.clicked.connect(self.on_dialog1_pushButton_clicked)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "dialog1", None))
        self.dialog1_pushButton.setText(_translate("Dialog", "返回主窗体", None))

    def on_dialog1_pushButton_clicked(self):
        self.form.close()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Dialog1()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
