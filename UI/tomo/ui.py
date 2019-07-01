from PyQt4 import QtCore, QtGui
from Input import Ui_Form
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



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        if text.strip('\n').strip():
            self.textWritten.emit("print Info: {}".format(str(text).strip('\n')))

class TestDialog(QtGui.QTableWidget):
    def __init__(self):
        super(TestDialog, self).__init__()

        self.resize(900, 900)
        self.firstUI = Ui_Form()
        self.secondUI = Ui_Dialog()

        tabWidget = QtGui.QTabWidget(self)
        w1 = QtGui.QWidget()
        self.firstUI.setupUi(w1)
        w2 = QtGui.QDialog()
        self.secondUI.setupUi(w2)

        tabWidget.addTab(w1, "Input")
        tabWidget.addTab(w2, "preProcess")
        tabWidget.resize(900, 800)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        #cursor = self.firstUI.out.textCursor()
        #cursor.movePosition(QtGui.QTextCursor.End)
        self.firstUI.out.append(text)
        #self.firstUI.out.setTextCursor(cursor)
        #self.firstUI.out.ensureCursorVisible()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = TestDialog()
    dialog.show()
    sys.exit(app.exec_())






