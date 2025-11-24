import sys
import os

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
from src.gui import MainWindow, app_qss
from PyQt5 import QtWidgets



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(app_qss())

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()