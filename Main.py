#-*-coding:utf-8-*-
__author__ = 'lixin'
from PyQt4 import QtGui,QtCore
import sys
import QtGui as UI


def main():
    app = QtGui.QApplication(sys.argv)
    ex = UI.window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()