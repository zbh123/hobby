# #coding:utf-8
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtWebKit import *
from PyQt4 import QtCore, QtGui
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class MyConsole(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent

        self.initUI()

    # 初始化UI
    def initUI(self):
        self.gridlayout = QtGui.QGridLayout()

        # 设置出20 x 20 的格局
        for i in range(20):
            self.gridlayout.setColumnStretch(i, 1)
            self.gridlayout.setRowStretch(i, 1)

        lb1 = QLabel(u'账户：')
        lb2 = QLabel(u'密码：')
        self.userEntry = QLineEdit()
        self.passEntry = QLineEdit()
        self.passEntry.setEchoMode(QLineEdit.Password)
        self.loginBtn = QtGui.QPushButton(u"登录")
        self.loginBtn.setFixedSize(40, 20)
        self.connect(self.loginBtn, QtCore.SIGNAL('clicked()'), self.onLoginButton)

        self.gridlayout.addWidget(lb1, 0, 0)
        self.gridlayout.addWidget(lb2, 1, 0)
        self.gridlayout.addWidget(self.userEntry, 0, 1, 1, 3)
        self.gridlayout.addWidget(self.passEntry, 1, 1, 1, 3)
        self.gridlayout.addWidget(self.loginBtn, 0, 4, 1, 2)

        self.setLayout(self.gridlayout)

        # 响应登录按钮

    def onLoginButton(self):
        username = self.userEntry.text()
        password = self.passEntry.text()
        QtGui.QMessageBox.about(self, username + u'登录成功', u"密码是：" + password)
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf-8"))
        print
        username + u'登录成功！\n' + u"密码是：" + password


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        tabs = QtGui.QTabWidget(self)

        # tab1
        tab1 = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout()
        console = MyConsole(self)
        vbox.addWidget(console)
        tab1.setLayout(vbox)

        # tab2
        self.tab2 = QTextEdit()

        tabs.addTab(tab1, u"控制台")
        tabs.addTab(self.tab2, u"日志输出")

        tabs.resize(500, 350)
        self.resize(500, 350)

        # 禁止最大化
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.show()

        # 重定向输出
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        cursor = self.tab2.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.tab2.setTextCursor(cursor)
        self.tab2.ensureCursorVisible()


def main():
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
