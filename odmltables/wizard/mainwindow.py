# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:57:46 2016

@author: zehl
"""

from PyQt4 import QtGui, QtCore
#import wizards
from converterwiz import ConversionWizard
from compsectionwiz import CompSectionWiz
from generatetemplatewiz import GenerateTemplateWizard
from filterwiz import FilterWizard
from mergewiz import MergeWizard
#from table2odmlwiz import Table2OdmlWiz

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):

        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)

        vbox = QtGui.QVBoxLayout()

        title_font = QtGui.QFont()
        # title_font.setFamily("Verdana")
        title_font.setBold(True)
        title_font.setPointSize(14)
        label = QtGui.QLabel("Welcome to the grapical odml-tables interface!")
        label.setFont(title_font)
        vbox.addWidget(label)
        vbox.addSpacing(5)

        subtitle = QtGui.QLabel('Select one of the actions below')
        vbox.addWidget(subtitle)
        vbox.addSpacing(10)

        grid = QtGui.QGridLayout()
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,1)
        vbox.addLayout(grid)

        self.convertbutton = QtGui.QToolButton()
        self.convertbutton.setText(self.tr('Convert between odml\nand table format'))
        self.convertbutton.setIcon(QtGui.QIcon("graphics/convertodml.svg"))
        self.convertbutton.setIconSize(QtCore.QSize(120,60))
        self.convertbutton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.convertbutton.setFixedWidth(200)
        self.convertbutton.clicked.connect(self.startWizard)
        grid.addWidget(self.convertbutton,0,0)

        self.comparebutton = QtGui.QToolButton()
        self.comparebutton.setText(self.tr('Compare entries within\nan odml'))
        self.comparebutton.setIcon(QtGui.QIcon("graphics/comparetable.svg"))
        self.comparebutton.setIconSize(QtCore.QSize(120,60))
        self.comparebutton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.comparebutton.setFixedWidth(200)
        self.comparebutton.clicked.connect(self.startWizard)
        grid.addWidget(self.comparebutton,0,1)

        self.generatebutton = QtGui.QToolButton()
        self.generatebutton.setText(self.tr('Generate empty template\n table'))
        self.generatebutton.setIcon(QtGui.QIcon("graphics/createtemplate.svg"))
        self.generatebutton.setIconSize(QtCore.QSize(120,60))
        self.generatebutton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.generatebutton.setFixedWidth(200)
        self.generatebutton.clicked.connect(self.startWizard)
        grid.addWidget(self.generatebutton,1,0)

        self.filterbutton = QtGui.QToolButton()
        self.filterbutton.setText(self.tr('Filter content of odml\n'))
        self.filterbutton.setIcon(QtGui.QIcon("graphics/filterodml.svg"))
        self.filterbutton.setIconSize(QtCore.QSize(120,60))
        self.filterbutton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.filterbutton.setFixedWidth(200)
        self.filterbutton.clicked.connect(self.startWizard)
        grid.addWidget(self.filterbutton,1,1)

        self.mergebutton = QtGui.QToolButton()
        self.mergebutton.setText(self.tr('Merge contents of odmls\n'))
        self.mergebutton.setIcon(QtGui.QIcon("graphics/mergeodml.svg"))
        self.mergebutton.setIconSize(QtCore.QSize(120,60))
        self.mergebutton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mergebutton.setFixedWidth(200)
        self.mergebutton.clicked.connect(self.startWizard)
        grid.addWidget(self.mergebutton,2,0)


        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('odML-tables')
        centralWidget.setLayout(vbox)
        self.show()

    def startWizard(self):
        sender = self.sender()
        if sender==self.convertbutton:
            wizard = ConversionWizard()
        elif sender==self.comparebutton:
            wizard = CompSectionWiz()
        elif sender==self.generatebutton:
            wizard = GenerateTemplateWizard()
        elif sender==self.filterbutton:
            wizard = FilterWizard()
        elif sender==self.mergebutton:
            wizard = MergeWizard()
        else:
            raise EnvironmentError('Unknown sender')
        wizard.exec_()
