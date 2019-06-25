'''
实时动态显示print值，只能在QThread下，正常部件不能有效执行显示控制台的功能
QThread下不能再使用多进程，否则会跳出多个窗口，无法正常运行，但可以另外引进函数或者类，执行多进程，配合pyqtSignal功能可以满足当前条件
'''

from PyQt4 import *
import os

class Worker(QThread):
    file_changed_signal = pyqtSignal(str)
    def __init__(self):
        super(Worker, self).__init__()
        self.working = True

    def __del__(self):
        self.working = False

    def run(self):
        self.main()

    def main(self):
        pass
