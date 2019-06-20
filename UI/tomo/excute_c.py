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