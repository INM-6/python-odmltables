# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:57:16 2016

@author: zehl
"""

from PyQt4 import QtGui
import sys
from mainwindow import MainWindow

def main():

    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
