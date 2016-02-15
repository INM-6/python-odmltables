# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:57:46 2016

@author: zehl
"""

import sys
from PyQt4 import QtGui, QtCore
#import wizards
from odmlconverterwiz import Odml2TableWiz
from compsectionwiz import CompSectionWiz
#from table2odmlwiz import Table2OdmlWiz

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):

        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)

        label = QtGui.QLabel("Welcome to the odmltable-GUI!")

        self.radio1 = QtGui.QRadioButton("odmltable <-> odml")
        self.radio2 = QtGui.QRadioButton("compare sections")
        self.radio3 = QtGui.QRadioButton("sth else")

        okButton = QtGui.QPushButton("OK")
        cancelButton = QtGui.QPushButton("Cancel")

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)
        hbox.addWidget(okButton)

        vbox = QtGui.QVBoxLayout()

        vbox.addWidget(label)
        vbox.addStretch(1)
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addWidget(self.radio3)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        centralWidget.setLayout(vbox)

        self.statusBar()

        okButton.clicked.connect(self.startWizard)
        cancelButton.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main Window')
        self.show()

    def startWizard(self):
        if self.radio1.isChecked():
            wizard = Odml2TableWiz()
            wizard.exec_()
        elif self.radio2.isChecked():
            wizard = CompSectionWiz()
            wizard.exec_()
        elif self.radio3.isChecked():
            pass # new options
        else:
            self.statusBar().showMessage("Choose one of the Options above")

