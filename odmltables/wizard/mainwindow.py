# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:57:46 2016

@author: zehl
"""

import os
from PyQt4 import QtGui, QtCore
#import wizards
from converterwiz import ConversionWizard
from compsectionwiz import CompSectionWiz
from generatetemplatewiz import GenerateTemplateWizard
from filterwiz import FilterWizard
from mergewiz import MergeWizard

from wizutils import get_graphic_path

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

        self.convertbutton = self.generate_icon('Convert between odml\nand '
                                                'table format',
                                                "convertodml.svg")
        self.comparebutton = self.generate_icon('Compare entries within\nan ' \
                                               'odml',
                                           "comparetable.svg")
        self.generatebutton = self.generate_icon('Generate empty '
                                                 'template\ntable',
                                                 "createtemplate.svg")
        self.filterbutton = self.generate_icon('Filter content of odml\n',
                                               "filterodml.svg")
        self.mergebutton = self.generate_icon('Merge contents of odmls\n',
                                              "mergeodml.svg")

        grid.addWidget(self.convertbutton,0,0)
        grid.addWidget(self.comparebutton,0,1)
        grid.addWidget(self.generatebutton,1,0)
        grid.addWidget(self.filterbutton,1,1)
        grid.addWidget(self.mergebutton,2,0)


        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('odML-tables')
        centralWidget.setLayout(vbox)
        self.show()

    def generate_icon(self,text,graphic_name):
        graphic_path = get_graphic_path()
        button = QtGui.QToolButton()
        button.setText(self.tr(text))
        button.setIcon(QtGui.QIcon(os.path.join(graphic_path,graphic_name)))
        button.setIconSize(QtCore.QSize(120,60))
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        button.setFixedWidth(200)
        button.clicked.connect(self.startWizard)

        return button


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
