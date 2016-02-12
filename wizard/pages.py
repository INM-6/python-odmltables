# -*- coding: utf-8 -*-
"""
pages
=====

Classes to create dialog pages for the wizard interface of python-odmltables.

Classes
-------

WelcomePage        - Class generating the first dialog page, where the user has
                     to decide which odmltable operation he/she wants to
                     perform

LoadodMLPage       - Class generating a dialog page, where the user has to
                     specify the odML file he/she wants to transform into a
                     table and define the corresponding table format

LoadTablePage      - Class generating a dialog page, where the user has to
                     specify the table file he/she wants to transform into an
                     odML file and state if the item names of the table header
                     were modified

HeaderOrderPage    - Class generating a dialog page, where the user has to
                     choose which table header items should be used, can change
                     in which order the table header items are displayed, and
                     state if the item names should be modified

HeaderDefNamesPage - Class generating a dialog page, where the user can modify
                     the names for all chosen header items for the wanted table

HeaderModNamesPage - Class generating a dialog page, where the user has to
                     match the default names of the odML header items to all
                     modified header item names of the loaded table

RedundancyPage     - Class generating a dialog page, where the user can state
                     if and which redundant information should be displayed in
                     the wanted table

MarkColumnPage     - Class generating a dialog page, where the user can decide
                     if and which column of the wanted table should be
                     emphasized compared to the remaining columns

BackPatternPage    - Class generating a dialog page, where the user can decide
                     if and which background pattern type should be used for
                     the wanted table

StylePage          - Class generating a dialog page, where the user can see the
                     style (background color, font style) of the chosen pattern
                     and can decide to change the style for the pattern fields,
                     individually

StyleModPage       - Class generating a dialog page, where the user can change
                     the background colors, the font colors, and the font style
                     for a selected pattern field of the wanted table

SavePage           - Class generating a dialog page, where the user defines the
                     location, and filename of the file that he wants to save


@author: zehl
"""

import os
import re
import copy
import xlwt
# from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
#                          QRadioButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout,
#                          QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
#                          QMessageBox,QWidget,QPushButton, QFileDialog, QComboBox,QListWidget,
#                          QListWidgetItem, QTableView,QFont,QPalette,QFrame,QSizePolicy,
#                          QToolButton,QColor,QItemEditorCreatorBase,QSpacerItem)
from PyQt4.QtGui import *
from PyQt4.QtCore import (pyqtSlot, QRegExp, Qt,pyqtProperty,SIGNAL)

from  odmltables import odml_table, odml_xls_table, odml_csv_table, xls_style



class QIWizardPage(QWizardPage):
    def __init__(self,settings,parent=None):
        super(QIWizardPage,self).__init__(parent)
        self.settings = settings

class LoadFilePage(QIWizardPage):
    def __init__(self,parent=None):
        super(LoadFilePage,self).__init__(parent)

        # Set up layout
        vbox = QVBoxLayout()

        # Adding input part
        topLabel = QLabel(self.tr("Choose a file to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        # Add first horizontal box
        self.buttonbrowse = QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.inputfilename = ''
        self.inputfile = QLabel(self.inputfilename)
        self.inputfile.setWordWrap(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.buttonbrowse)
        hbox1.addWidget(self.inputfile)

        hbox1.addStretch()
        vbox.addLayout(hbox1)

        self.cbcustominput = QCheckBox('I changed the column names in the input table.')
        self.cbcustominput.setEnabled(False)
        self.settings.register('CBcustominput',self.cbcustominput)
        vbox.addWidget(self.cbcustominput)
        vbox.addStretch()

        # Adding output part
        bottomLabel = QLabel(self.tr("Select an output format"))
        bottomLabel.setWordWrap(True)
        vbox.addWidget(bottomLabel)
        vbox.addWidget(bottomLabel)

        # Add second horizontal box
        self.rbuttonxls = QRadioButton(self.tr("xls"))
        self.rbuttoncsv = QRadioButton(self.tr("csv"))
        self.rbuttonodml = QRadioButton(self.tr("odml"))

        self.settings.register('RBoutputxls',self.rbuttonxls)
        self.settings.register('RBoutputcsv',self.rbuttoncsv)
        self.settings.register('RBoutputodml', self.rbuttonodml)
        # self.registerField('RBxls',self.rbuttonxls)
        # self.registerField('RBcsv',self.rbuttoncsv)
        # self.registerField('RBodml',self.rbuttonodml)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.rbuttonxls)
        hbox2.addSpacing(50)
        hbox2.addWidget(self.rbuttoncsv)
        hbox2.addSpacing(50)
        hbox2.addWidget(self.rbuttonodml)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        vbox.addStretch()

        self.setLayout(vbox)


    def handlebuttonbrowse(self):
        self.inputfilename = str(QFileDialog().getOpenFileName())

        self.settings.register('inputfilename', self)
        # self.registerField('Linputfile',self.inputpath)
        # filename = QFileDialog.getOpenFileName()
        short_filename = _shorten_path(self.inputfilename)
        self.inputfile.setText(short_filename)

        if str(self.inputfilename[-4:]) in ['.xls','.csv']:
            self.cbcustominput.setEnabled(True)
        else:
            self.cbcustominput.setEnabled(False)

        if str(self.inputfilename[-4:]) in ['.xls','.csv']:
            self.rbuttonodml.setChecked(True)
        elif str(self.inputfilename[-5:]) in ['.odml']:
            self.rbuttonxls.setChecked(True)

    def validatePage(self):
        if not any((self.settings.get_object('RBoutputxls').isChecked(),
                    self.settings.get_object('RBoutputcsv').isChecked(),
                    self.settings.get_object('RBoutputodml').isChecked())):
            QMessageBox.warning(self,'Select a format','You need to select a table format to continue.')
            return 0

        if not self.settings.get_object('inputfilename'):
            QMessageBox.warning(self,'Select an input file','You need to select an inupt file to continue.')
            return 0

        if self.settings.get_object('inputfilename').split('.')[-1] not in ['xls', 'csv', 'odml']:
            QMessageBox.warning(self,'Wrong input format','The input file has to be an ".xls", ".csv" or ".odml" file.')
            return 0

        return 1



    def nextId(self):
        if ((self.inputfilename[-5:] != '.odml') and
                (self.settings.get_object('CBcustominput').isChecked())):
            return self.wizard().PageCustomInputHeader

        elif not self.settings.get_object('RBoutputodml').isChecked():
            return self.wizard().PageHeaderOrder
        else:
            return self.wizard().PageSaveFile
        # if self.inputfilename[-5:] != '.odml':
        #     if self.settings.get_object('CBcustominput').isChecked():
        #         return self.wizard().PageCustomInputHeader
        #     else:
        #         return self.wizard().PageHeaderOrder
        # else:
        #     if (self.settings.get_object('RBoutputxls').isChecked() or
        #         self.settings.get_object('RBoutputcsv').isChecked()):
        #
        #         return self.wizard().PageHeaderOrder
        #
        #     else:
        #         return self.wizard().PageSaveFile




class CustomInputHeaderPage(QIWizardPage):
    def __init__(self,parent=None):
        super(CustomInputHeaderPage, self).__init__(parent)
        self.pagename =  self.objectName().split('.')[-1]

        # Set up layout
        vbox = QVBoxLayout()

        # Adding input part
        topLabel = QLabel(self.tr("Provide the column types used in the input table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        self.grid = QGridLayout()
        vbox.addLayout(self.grid)

        self.setLayout(vbox)

    def initializePage(self):
        # get header names from input file
        load_from = str(self.settings.get_object('inputfilename'))
        if load_from.endswith('.xls'):
            inputxlsheaders = odml_table.OdmlTable.get_xls_header(load_from)
        elif load_from.endswith('.csv'):
            inputxlsheaders = odml_table.OdmlTable.get_csv_header(load_from)
        else:
            raise TypeError('Header can be only read for xls or csv files.')


        odtables = odml_table.OdmlTable()
        header_names = odtables._header_titles.values()

        # self.n_headers = QLineEdit(str(len(customheaders)))
        # self.registerField('LEn_headers',self.n_headers)

        self.headerlabels = []
        self.customheaders = []

        for h, header in enumerate(inputxlsheaders):
            #set up individual row for header association
            h_label = QLabel(header)
            dd_list = QComboBox()
            dd_list.addItems(header_names)
            # Preselect fitting header name if possible
            if header in header_names:
                ind = header_names.index(header)
                dd_list.setCurrentIndex(ind)
            self.grid.addWidget(h_label,h,0)
            self.grid.addWidget(dd_list,h,1)
            # self.registerField('Lheader_%i'%(h),h_label)
            # self.registerField('CBheadernames_%i'%(h),dd_list)
            self.headerlabels.append(h_label)
            self.customheaders.append(dd_list)

        self.settings.register('headerlabels',self.headerlabels)
        self.settings.register('customheaders', self.customheaders)

        self.update()

    def validatePage(self):
        header_names = []

        # check for duplicate headers
        for h in self.customheaders:
            header_name = h.currentText()
            if header_name in header_names:
                QMessageBox.warning(self, self.tr("Non-unique headers"), self.tr("Header assignment has"
                                                  " to be unique. '%s' has been"
                                                  " assigned multiple times"%header_name))
                return 0
            header_names.append(header_name)

        # check for mandatory headers
        mandatory_headers = ['Path to Section', 'Property Name', 'Value', 'odML Data Type']
        for mand_head in mandatory_headers:
            if mand_head not in header_names:
                QMessageBox.warning(self, self.tr("Incomplete headers"), self.tr("You need to have the mandatory"
                                                                                 " headers %s in you table to be"
                                                                                 " able to reconstruct an odml"
                                                                                 ""%mandatory_headers))
                return 0
        return 1

class HeaderOrderPage(QIWizardPage):
    def __init__(self,parent=None):
        super(HeaderOrderPage, self).__init__(parent)
        self.pagename =  self.objectName().split('.')[-1]


        # Set up layout
        vbox = QVBoxLayout()

        # Adding input part
        topLabel = QLabel(self.tr("Select the columns for the output table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)


        odtables = odml_table.OdmlTable()
        header_names = odtables._header_titles.values()

        # generating selection lists
        self.header_list = QListWidget()
        self.header_list.setSelectionMode(3)
        self.selection_list = QListWidget()
        self.selection_list.setSelectionMode(3)

        self.settings.register('LWselectedcolumns',self.selection_list)
        self.settings.register('LWnonselectedcolumns',self.header_list)
        # self.registerField('test',self.header_list)
        # self.registerField('LWcolumnselection',self.selection_list,'currentItemData') #TODO: Check how fields work properly
        toright = QToolButton()
        toright.setArrowType(Qt.RightArrow)
        toright.clicked.connect(self.toright)
        toleft = QToolButton()
        toleft.setArrowType(Qt.LeftArrow)
        toleft.clicked.connect(self.toleft)

        hbox = QHBoxLayout()
        hbox.addWidget(self.header_list)
        vboxbuttons = QVBoxLayout()
        vboxbuttons.addStretch()
        vboxbuttons.addWidget(toright)
        vboxbuttons.addSpacing(30)
        vboxbuttons.addWidget(toleft)
        vboxbuttons.addStretch()
        hbox.addLayout(vboxbuttons)


        vbox.addLayout(hbox)


        self.itemsleft = []
        self.itemsright= []
        default_selection_list = ['Path to Section',
                                  'Property Name',
                                  'Value',
                                  'odML Data Type']
        self.mandatory_headers = copy.deepcopy(default_selection_list)
        for i,h in enumerate(header_names):
            if h not in default_selection_list:
                item = QListWidgetItem()
                item.setText(h)
                self.header_list.addItem(item)
                self.itemsleft.append(item)
                # if h in default_selection_list:
                #     self.header_list.setItemHidden(item,True)
            else:
                item = QListWidgetItem()
                item.setText(h)
                self.itemsright.append(item)
                self.selection_list.addItem(item)
                # if h not in default_selection_list:
                #     self.selection_list.setItemHidden(item,True)

        hbox.addWidget(self.selection_list)

        # adding up and down buttons
        up = QToolButton()
        up.setArrowType(Qt.UpArrow)
        up.clicked.connect(self.up)
        down = QToolButton()
        down.setArrowType(Qt.DownArrow)
        down.clicked.connect(self.down)

        vboxbuttons2 = QVBoxLayout()
        vboxbuttons2.addStretch()
        vboxbuttons2.addWidget(up)
        vboxbuttons2.addSpacing(30)
        vboxbuttons2.addWidget(down)
        vboxbuttons2.addStretch()
        hbox.addLayout(vboxbuttons2)

        vbox.addSpacing(20)

        self.cbcustomheader = QCheckBox('I want to change the names of my columns.')
        self.settings.register('CBcustomheader',self.cbcustomheader)
        # self.registerField('CBcustomheader',self.cbcustomheader)
        vbox.addWidget(self.cbcustomheader)

        self.setLayout(vbox)

    def toright(self):
        # sort rows in descending order in order to compensate shifting due to takeItem
        rows = sorted([index.row() for index in self.header_list.selectedIndexes()],
                      reverse=True)
        for row in rows:
            self.selection_list.addItem(self.header_list.takeItem(row))

    def toleft(self):
        # sort rows in descending order in order to compensate shifting due to takeItem
        rows = sorted([index.row() for index in self.selection_list.selectedIndexes()],
                      reverse=True)
        for row in rows:
            self.header_list.addItem(self.selection_list.takeItem(row))

    def up(self):
        currentRow = self.selection_list.currentRow()
        currentItem = self.selection_list.takeItem(currentRow)
        self.selection_list.insertItem(currentRow - 1, currentItem)
        self.selection_list.setCurrentRow(currentRow-1)

    def down(self):
        currentRow = self.selection_list.currentRow()
        currentItem = self.selection_list.takeItem(currentRow)
        self.selection_list.insertItem(currentRow + 1, currentItem)
        self.selection_list.setCurrentRow(currentRow+1)

    def nextId(self):
        if self.settings.get_object('CBcustomheader').isChecked():
            return self.wizard().PageCustomColumNames
        else:
            return self.wizard().currentId()+1

    def validatePage(self):

        # check number of selected headers
        if self.settings.get_object('LWselectedcolumns').count() < 1:
            QMessageBox.warning(self, self.tr("No header selected"),
                                self.tr("You need to select at least one header"
                                        " to generate a table representation of an odml."))
            return 0

        selectedheaderstrings = []
        for itemid in range(self.settings.get_object('LWselectedcolumns').count()):
            selectedheaderstrings.append(self.settings.get_object('LWselectedcolumns').item(itemid).text())

        missing_headers = []
        for mand_header in self.mandatory_headers:
            if mand_header not in selectedheaderstrings:
                missing_headers.append(mand_header)

        if missing_headers != []:
            QMessageBox.warning(self, self.tr("Incomplete odml"),
                            self.tr("You need to include the headers %s "
                                    " in your table if you want to be able to"
                                    " generate an odml from the table."%(missing_headers)))

        return 1




class CustomColumnNamesPage(QIWizardPage):
    def __init__(self,parent=None):
        super(CustomColumnNamesPage, self).__init__(parent)
        self.pagename =  self.objectName().split('.')[-1]

        # Set up layout
        vbox = QVBoxLayout()

        # Adding input part
        topLabel = QLabel(self.tr("Customize header names of output table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        self.grid = QGridLayout()
        vbox.addLayout(self.grid)

        self.setLayout(vbox)



    def initializePage(self):

        # get selected columns from HeaderOrderPage
        selectedheaderstrings = []
        for itemid in range(self.settings.get_object('LWselectedcolumns').count()):
            selectedheaderstrings.append(self.settings.get_object('LWselectedcolumns').item(itemid).text())

        # show marking option only for xls output
        enable_marking = False
        if self.settings.get_object('RBoutputxls').isChecked():
            enable_marking = True

        self.customheaderlabels = []
        self.columnmarkings = False
        headerlabel = QLabel('Odml Header')
        headerlabel.setStyleSheet('font: bold 14px')
        self.grid.addWidget(headerlabel,0,0)
        customlabel = QLabel('Customized Label')
        customlabel.setStyleSheet('font: bold 14px')
        self.grid.addWidget(customlabel,0,1)
        if enable_marking:
            markinglabel = QLabel('Highlight Column')
            markinglabel.setStyleSheet('font: bold 14px')
            self.grid.addWidget(markinglabel,0,2)

        for h,selheaderstr in enumerate(selectedheaderstrings):
            label = QLabel(selheaderstr)
            customheader = QLineEdit()
            customheader.setText(selheaderstr)
            self.customheaderlabels.append(customheader)
            self.grid.addWidget(label,h+1,0)
            self.grid.addWidget(customheader,h+1,1)
            if enable_marking:
                cbmarking = QCheckBox()
                self.grid.addWidget(cbmarking,h+1,2)
                if self.columnmarkings == False:
                    self.columnmarkings = []
                self.columnmarkings.append(cbmarking)
                self.grid.setAlignment(cbmarking,Qt.AlignCenter)

        self.settings.register('customheaderlabels', self.customheaderlabels)
        self.settings.register('columnmarkings',self.columnmarkings)

    def validatePage(self):
        #get manually entered labels
        customlabels = [le.text() for le in self.settings.get_object('customheaderlabels')]

        if any([label == '' for label in customlabels]):
            QMessageBox.warning(self, self.tr("Empty header name"),
                self.tr("You need to provide a unique, non empty "
                        "name for each of your selected headers"))
            return 0

        for l,label in enumerate(customlabels):
            if label in customlabels[:l] + customlabels[l+1:]:
                QMessageBox.warning(self, self.tr("Ambiguous header name"),
                self.tr("You used '%s' as label for multiple headers. "
                        " You need to provide a unique "
                        " name for each of your selected headers"%(label)))
                return 0

        return 1

    def nextId(self):
        if self.settings.get_object('RBoutputxls').isChecked():
            return self.wizard().currentId() + 1
        else:
            return self.wizard().PageSaveFile




# class ColumnMarkingPage(QIWizardPage):
#     def __init__(self,parent=None):
#         super(ColumnMarkingPage, self).__init__(parent)
#         self.pagename =  self.objectName().split('.')[-1]
#
#         # Set up layout
#         vbox = QVBoxLayout()
#
#         # Adding input part
#         topLabel = QLabel(self.tr("Select colums to be marked in the xls table"))
#         topLabel.setWordWrap(True)
#         vbox.addWidget(topLabel)
#         vbox.addSpacing(20)
#
#         self.grid = QGridLayout()
#         vbox.addLayout(self.grid)
#
#         self.setLayout(vbox)
#
#     def initializePage(self):
#         # get selected columns from HeaderOrderPage
#         selectedheaderstrings = []
#         for itemid in range(self.settings.get_object('LWselectedcolumns').count()):
#             selectedheaderstrings.append(self.settings.get_object('LWselectedcolumns').item(itemid).text())
#
#         # get customized headerlabels if specified
#         if self.settings.is_registered('customheaderlabels'):
#             customheaderstrings = [le.text() for le in self.settings.get_object('customheaderlabels')]
#             if len(selectedheaderstrings) != len(customheaderstrings):
#                 raise ValueError('Different numbers of customized headers and customized header labels.')


class ColorPatternPage(QIWizardPage):
    def __init__(self,parent=None):
        super(ColorPatternPage, self).__init__(parent)
        self.pagename =  self.objectName().split('.')[-1]

        # Set up layout
        vbox = QVBoxLayout()

        # adding pattern selection part
        topLabel = QLabel(self.tr("Select the color pattern to be used in the xls table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        self.rbalternating = QRadioButton('alternating')
        self.rbchessfield = QRadioButton('chessfield')
        self.rbnopattern = QRadioButton('no pattern')

        self.settings.register('RBalternating',self.rbalternating)
        self.settings.register('RBchessfield',self.rbchessfield)
        self.settings.register('RBnopattern',self.rbnopattern)

        self.rbalternating.setChecked(True)
        self.rbnopattern.toggled.connect(self.updatelayout)

        vbox.addWidget(self.rbalternating)
        vbox.addWidget(self.rbchessfield)
        vbox.addWidget(self.rbnopattern)

        vbox.addSpacing(40)

        # adding style switch part
        self.bottomLabel = QLabel(self.tr("When shall the style switch? Beginning of a new"))
        self.bottomLabel.setWordWrap(True)
        # self.bottomLabel.setEnabled(False)
        vbox.addWidget(self.bottomLabel)
        vbox.addSpacing(20)

        self.rbsection = QRadioButton('Section')
        self.rbproperty = QRadioButton('Property')
        self.rbvalue = QRadioButton('Value')

        self.rbsection.setChecked(True)

        # self.rbsection.setEnabled(False)
        # self.rbproperty.setEnabled(False)
        # self.rbvalue.setEnabled(False)

        self.settings.register('RBsection',self.rbsection)
        self.settings.register('RBproperty',self.rbproperty)
        self.settings.register('RBvalue',self.rbvalue)

        vbox.addWidget(self.rbsection)
        vbox.addWidget(self.rbproperty)
        vbox.addWidget(self.rbvalue)

        self.setLayout(vbox)


    def updatelayout(self):
        if self.rbnopattern.isChecked():
            self.bottomLabel.setEnabled(False)
            self.rbsection.setEnabled(False)
            self.rbproperty.setEnabled(False)
            self.rbvalue.setEnabled(False)
        else:
            self.bottomLabel.setEnabled(True)
            self.rbsection.setEnabled(True)
            self.rbproperty.setEnabled(True)
            self.rbvalue.setEnabled(True)



class ChangeStylePage(QIWizardPage):
    def __init__(self,parent=None):
        super(ChangeStylePage, self).__init__(parent)

        # Set up layout
        vbox = QVBoxLayout()

        # adding pattern selection part
        topLabel = QLabel(self.tr("Click on a field to choose the style for this field"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)



        texts = ['Header','Standard\nRow 1', 'Standard\nRow 2','Marked \nRow 1','Marked \nRow 2','Default Value']
        default_styles = ['color: rgb(255,255,255); background-color: rgb(51,51,51); font:bold',
                          'color: rgb(255,255,255); background-color: rgb(0,128,0)',
                          'color: rgb(255,255,255); background-color: rgb(0,0,128)',
                          'color: rgb(0,0,0); background-color: rgb(153,204,0)',
                          'color: rgb(0,0,0); background-color: rgb(51,102,255)',
                          'color: rgb(0,0,0); background-color: rgb(255,0,0)']
        common_default = "; padding-left: 5px; padding-right: 5px; padding-top: 5px; padding-bottom: 5px; border-color: rgb(255,0,0)" #background-color: rgb(0, 255, 255);
        # ''padding: 6px'
        positions = [(0,0,1,2),(1,0),(2,0),(1,1),(2,1),(3,0,1,2)]

        self.tablebuttons = [None]*len(texts)

        gridtable = QGridLayout()
        for i in range(len(self.tablebuttons)):
            self.tablebuttons[i] = QPushButton()
            self.tablebuttons[i].setText(texts[i])
            self.tablebuttons[i].setStyleSheet(default_styles[i])
            self.tablebuttons[i].setStyleSheet(self.tablebuttons[i].styleSheet() + common_default)
            self.tablebuttons[i].setAutoFillBackground(True)
            self.tablebuttons[i].clicked.connect(self.updatesettings)
            gridtable.addWidget(self.tablebuttons[i],*positions[i])
            # self.tablebuttons[i].setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
            self.settings.register(texts[i],self.tablebuttons[i])

        self.cbhighlightdefaults = QCheckBox('Highlight default values')
        self.cbhighlightdefaults.setChecked(True)
        self.cbhighlightdefaults.toggled.connect(self.updatedefaultbutton)
        self.settings.register('CBhighlightdefaults',self.cbhighlightdefaults)

        # add spacer for invisible 'default value' button
        self.spacer = QSpacerItem(10,0)

        gridtable.setSpacing(0)

        vstretcher = QVBoxLayout()
        vstretcher.addStretch(1)
        vstretcher.addLayout(gridtable)
        vstretcher.addSpacerItem(self.spacer)
        vstretcher.addSpacing(10)
        vstretcher.addWidget(self.cbhighlightdefaults)
        vstretcher.addStretch(1)

        hbox.addLayout(vstretcher)

        # adding separator
        verticalLine = QFrame()
        verticalLine.setFrameStyle(QFrame.VLine)
        verticalLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        hbox.addWidget(verticalLine)


        self.cbbgcolor = ColorListWidget()
        self.cbbgcolor.currentIndexChanged.connect(self.updatetable)
        self.settings.register('CBbgcolor',self.cbbgcolor)

        self.cbfontcolor = ColorListWidget()
        self.cbfontcolor.currentIndexChanged.connect(self.updatetable)
        self.settings.register('CBfontcolor',self.cbfontcolor)

        self.cbboldfont = QCheckBox('bold')
        self.cbboldfont.setStyleSheet('font:bold')
        self.cbboldfont.toggled.connect(self.updatetable)
        self.cbitalicfont = QCheckBox('italic')
        self.cbitalicfont.setStyleSheet('font:italic')
        self.cbitalicfont.toggled.connect(self.updatetable)

        gridsettings = QGridLayout()
        self.settingstitle = QLabel()
        self.settingstitle.setText('-')
        self.settingstitle.setStyleSheet('font:bold 16px')
        gridsettings.addWidget(self.settingstitle,0,0,1,1)
        gridsettings.addWidget(QLabel('Backgroundcolor'),1,0)
        gridsettings.addWidget(self.cbbgcolor,1,1)
        gridsettings.addWidget(QLabel('Fontcolor'),2,0)
        gridsettings.addWidget(self.cbfontcolor,2,1)
        gridsettings.addWidget(QLabel('Fontstyle'),3,0)
        gridsettings.addWidget(self.cbboldfont,3,1)
        gridsettings.addWidget(self.cbitalicfont,4,1)
        gridsettings.setSpacing(0)
        gridsettings.setAlignment(Qt.AlignCenter)

        hbox.addLayout(gridsettings)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.currentbutton = self.tablebuttons[0]


    def updatesettings(self):
        sender = self.sender()
        self.currentbutton = sender
        # show selected button
        sender.setStyleSheet(sender.styleSheet() + '; border: 2px solid red')
        # unselect other buttons
        for button in self.tablebuttons:
            if button != sender:
                button.setStyleSheet(self.removestyle(button.styleSheet(),'border'))

        # update header of selection part (right part)
        self.settingstitle.setText(sender.text().replace('\n',' '))
        # update backgroundcolor
        color = get_rgb(get_property(sender.styleSheet(),'background-color'))
        index = self.cbbgcolor.xlwt_rgbcolors.index(color)#self.cbbgcolor.findText(color, Qt.MatchFixedString)
        if index >= 0:
            self.cbbgcolor.setCurrentIndex(index)
        else:
            pass
        # update fontcolor
        color = get_rgb(get_property(sender.styleSheet(),'color'))
        index = self.cbfontcolor.xlwt_rgbcolors.index(color)#self.cbfontcolor.findText(color, Qt.MatchFixedString)
        if index >= 0:
            self.cbfontcolor.setCurrentIndex(index)
        else:
            pass
        #update font style
        font_style = get_property(sender.styleSheet(),'font')
        if font_style == None: font_style = ''
        self.cbboldfont.setChecked('bold' in font_style)
        self.cbitalicfont.setChecked('italic' in font_style)


    def updatetable(self):
        sender = self.sender()
        # updates from comboboxes
        if sender in [self.cbbgcolor,self.cbfontcolor]:
            if sender == self.cbbgcolor:
                to_update = 'background-color'
                new_style_value = 'rgb%s;'%(str(self.cbbgcolor.get_current_rgb()))
            elif sender == self.cbfontcolor:
                to_update = 'color'
                new_style_value = 'rgb%s;'%(str(self.cbfontcolor.get_current_rgb()))
            self.currentbutton.setStyleSheet(self.removestyle(self.currentbutton.styleSheet(),to_update) + '; %s:%s'%(to_update,new_style_value))

        # updates from checkboxes
        elif sender in [self.cbboldfont,self.cbitalicfont]:
            new_style = self.currentbutton.styleSheet()
            if sender == self.cbboldfont:
                new_value = 'bold'
            elif sender == self.cbitalicfont:
                new_value = 'italic'
            new_style.replace(new_value,'')
            if sender.isChecked():
                if 'font:' in new_style:
                    new_style.replace('font:','font: %s'%new_value)
                else:
                    new_style += '; font: %s'%new_value

            self.currentbutton.setStyleSheet(new_style)

    def removestyle(self,style,property):
        styles = [str(s) for s in style.split(';')]
        s = 0
        while s < len(styles):
            if styles[s].strip(' ').startswith(property+':'):
                styles.pop(s)
                styles = [s.strip(' ').rstrip(' ') for s in styles if s.strip(' ')!='']
            else:
                s += 1
        return '; '.join(styles)


    def updatedefaultbutton(self):
        self.tablebuttons[5].setVisible(self.cbhighlightdefaults.isChecked())
        if self.cbhighlightdefaults.isChecked():
            height = 0
        else:
            height = self.tablebuttons[5].height()
        self.spacer.changeSize(self.tablebuttons[5].width(),height,QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout().invalidate()



class ColorListWidget(QComboBox):

    _xlwt_rgbcolors=[
    (0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0),
    (255,0,255), (0,255,255), (0,0,0), (255,255,255), (255,0,0), (0,255,0),
    (0,0,255), (255,255,0), (255,0,255), (0,255,255), (128,0,0), (0,128,0),
    (0,0,128), (128,128,0), (128,0,128), (0,128,128), (192,192,192),
    (128,128,128), (153,153,255), (153,51,102), (255,255,204),
    (204,255,255), (102,0,102), (255,128,128), (0,102,204), (204,204,255),
    (0,0,128), (255,0,255), (255,255,0), (0,255,255), (128,0,128),
    (128,0,0), (0,128,128), (0,0,255), (0,204,255), (204,255,255),
    (204,255,204), (255,255,153), (153,204,255), (255,153,204),
    (204,153,255), (255,204,153), (51,102,255), (51,204,204), (153,204,0),
    (255,204,0), (255,153,0), (255,102,0), (102,102,153), (150,150,150),
    (0,51,102), (51,153,102), (0,51,0), (51,51,0), (153,51,0), (153,51,102),
    (51,51,153), (51,51,51)
    ]

    def __init__(self):
        super(ColorListWidget, self).__init__()
        cmap = xlwt.Style.colour_map
        self.xlwt_colornames = []
        self.xlwt_color_index = []
        self.xlwt_rgbcolors = []
        # self._xlwt_colorlabels = []
        for i in range(64):
            cnames = [name for name, index in cmap.items() if index == i]
            # self._xlwt_colorlabels.append(cnames[0] if len(cnames)>0 else '')
            if cnames != []:
                self.xlwt_colornames.append(', '.join(cnames))
                self.xlwt_color_index.append(i)
                self.xlwt_rgbcolors.append(self._xlwt_rgbcolors[i])

        for i,xlwtcolor in enumerate(self.xlwt_colornames):
            self.insertItem(i, xlwtcolor)
            self.setItemData(i, QColor(*self.xlwt_rgbcolors[i]), Qt.DecorationRole)

    def get_current_rgb(self):
        return self.xlwt_rgbcolors[self.currentIndex()]








class SaveFilePage(QIWizardPage):
    def __init__(self,parent=None):
        super(SaveFilePage, self).__init__(parent)

        # Set up layout
        vbox = QVBoxLayout()

        # adding pattern selection part
        topLabel = QLabel(self.tr("Where do you want to save your file?"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(40)

        # Add first horizontal box
        self.buttonbrowse = QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.outputfilename = ''
        self.outputfile = QLabel(self.outputfilename)
        self.outputfile.setWordWrap(True)
        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonbrowse)
        hbox.addWidget(self.outputfile)

        hbox.addStretch()

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.outputfilename = ''

    def handlebuttonbrowse(self):
        self.outputfilename = str(QFileDialog.getSaveFileName(self, self.tr("Save File"),
                            os.path.dirname(self.settings.get_object('inputfilename')),""))

        self.settings.register('outputfilename', self)
        short_filename = _shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

    def validatePage(self):
        if self.settings.get_object('RBoutputxls').isChecked():
            expected_extension = '.xls'
        elif self.settings.get_object('RBoutputcsv').isChecked():
            expected_extension = '.csv'
        elif self.settings.get_object('RBoutputodml').isChecked():
            expected_extension = '.odml'
        else:
            raise ValueError('Can not save file without selection of output format.')

        if self.outputfilename == '':
            QMessageBox.warning(self,'No output file','You need to select an output file.')
            return 0
        elif ((os.path.splitext(self.outputfilename)[1]!=expected_extension) and
                  (os.path.splitext(self.outputfilename)[1]!='')):
            QMessageBox.warning(self,'Wrong file format','The output file format is supposed to be "%s",'
                                                         ' but you selected "%s"'
                                                         ''%(expected_extension,
                                                             os.path.splitext(self.outputfilename)[1]))
            return 0
        # extending filename if no extension is present
        if os.path.splitext(self.outputfilename)[1]=='':
            self.outputfilename += expected_extension

        convert(self.settings)

        print 'Complete!'
        return 1


def convert(settings):

    # generate odmltables object
    table = None
    if os.path.splitext(settings.get_object('outputfilename'))[1] == '.xls':
        table = odml_xls_table.OdmlXlsTable()
    elif os.path.splitext(settings.get_object('outputfilename'))[1] == '.csv':
        table = odml_csv_table.OdmlCsvTable()
    elif os.path.splitext(settings.get_object('outputfilename'))[1] == '.odml':
        table = odml_table.OdmlTable()
    else:
        raise ValueError('Unknown output file extension "%s"'
                         ''%os.path.splitext(settings.get_object('outputfilename'))[1])

    # setting xls_table or csv_table headers if necessary
    if ((os.path.splitext(settings.get_object('inputfilename'))[1] in ['.xls','.csv']) and
            (settings.get_object('CBcustominput').isChecked())):
        inputheaderlabels = [str(l.text()) for l in settings.get_object('headerlabels')]
        inputcustomheaders = [str(cb.currentText()) for cb in settings.get_object('customheaders')]
        title_translator = {v:k for k,v in table._header_titles.iteritems()}
        inputcolumnnames = [title_translator[label] for label in inputcustomheaders]
        table.change_header_titles(**dict(zip(inputcolumnnames,inputheaderlabels)))

    # loading input file
    if os.path.splitext(settings.get_object('inputfilename'))[1] == '.xls':
        table.load_from_xls_table(settings.get_object('inputfilename'))
    elif os.path.splitext(settings.get_object('inputfilename'))[1] == '.csv':
        table.load_from_csv_table(settings.get_object('inputfilename'))
    elif os.path.splitext(settings.get_object('inputfilename'))[1] == '.odml':
        table.load_from_file(settings.get_object('inputfilename'))
    else:
        raise ValueError('Unknown input file extension "%s"'
                         ''%os.path.splitext(settings.get_object('inputfilename'))[1])


    # setting custom header selection and custom header titles if necessary
    if (os.path.splitext(settings.get_object('inputfilename'))[1] in ['.xls','.csv']):
        # setting custom header columns
        output_headers = [title_translator[str(settings.get_object('LWselectedcolumns').item(index).text())]
                          for index in range(settings.get_object('LWselectedcolumns').count())]
        table.change_header(**dict(zip(output_headers,range(1,len(output_headers)+1))))

        # setting custom header labels
        if settings.get_object('CBcustomheader').isChecked():
            customoutputlabels = [le.text() for le in settings.get_object('customheaderlabels')]
            table.change_header_titles(**dict(zip(output_headers,customoutputlabels)))

        # adding extra layout specifications to xls output files
        if os.path.splitext(settings.get_object('outputfilename'))[1] == '.xls':
            # marking columns
            marked_columns = [cb.isChecked() for cb in settings.get_object('columnmarkings')]
            if any(marked_columns):
                table.mark_columns(*[h for i,h in enumerate(output_headers) if marked_columns[i]])

            # setting color pattern and changing point
            if settings.get_object('RBalternating').isChecked():
                table.pattern = 'alternating'
            elif settings.get_object('RBchessfield').isChecked():
                table.pattern = 'chessfield'

            if settings.get_object('RBnopattern').isChecked():
                table.changing_point = None
            elif settings.get_object('RBsection').isChecked():
                table.changing_point = "sections"
            elif settings.get_object('RBproperty').isChecked():
                table.changing_point = "properties"
            elif settings.get_object('RBvalue').isChecked():
                table.changing_point = "values"

            style_names = ['header_style','first_style','second_style','first_marked_style','second_marked_style','highlight_style']
            style_labels = ['Header','Standard\nRow 1', 'Standard\nRow 2','Marked \nRow 1','Marked \nRow 2','Default Value']
            style_buttons = [settings.get_object(style_label) for style_label in style_labels]

            for i,style_name in enumerate(style_names):
                style_button = style_buttons[i]

                # get background color
                rgb_tuple = get_rgb(get_property(style_button.styleSheet(),'background-color'))
                index = settings.get_object('CBbgcolor').xlwt_rgbcolors.index(rgb_tuple)
                bgcolor = settings.get_object('CBbgcolor').xlwt_colornames[index].split(',')[0]

                # get font color
                rgb_tuple = get_rgb(get_property(style_button.styleSheet(),'color'))
                index = settings.get_object('CBfontcolor').xlwt_rgbcolors.index(rgb_tuple)
                fontcolor = settings.get_object('CBfontcolor').xlwt_colornames[index].split(',')[0]

                # get font properties
                font_properties = ''
                font_string = get_property(style_button.styleSheet(),'font')
                if 'bold' in font_string:
                    font_properties += 'bold 1'
                if 'italic' in font_string:
                    font_properties += 'italic 1'

                # construct style
                style = xls_style.XlsStyle(backcolor=bgcolor,
                                             fontcolor=fontcolor,
                                             fontstyle=font_properties)
                setattr(table,style_name,style)


            # setting highlight defaults
            table.highlight_defaults = settings.get_object('CBhighlightdefaults').isChecked()

    # saving file
    if os.path.splitext(settings.get_object('outputfilename'))[1] in ['.xls','.csv']:
        table.write2file(settings.get_object('outputfilename'))
    elif os.path.splitext(settings.get_object('outputfilename'))[1] == '.odml':
        table.write2odml(settings.get_object('outputfilename'))











#######################################################
# Supplementory functions
def _shorten_path(path):
    sep = os.path.sep
    if path.count(sep)>2:
        id = path.rfind(sep)
        id = path.rfind(sep,0,id)
    else:
        id = 0
    if path == '':
        return path
    else:
        return "...%s" % (path[id:])


def get_property(style,property):
    styles = [str(s) for s in style.split(';')]
    for s in styles:
        if s.strip(' ').startswith(property+':'):
            return s.replace(property+':','')

    return ''


def get_rgb(style_string):
    rgbregex = re.compile(" *rgb\( {0,2}(?P<r>\d{1,3}), {0,2}(?P<g>\d{1,3}), {0,2}(?P<b>\d{1,3})\) *")
    match = rgbregex.match(style_string)
    if match:
        groups = match.groupdict()
        return tuple([int(groups['r']),int(groups['g']),int(groups['b'])])
    else:
        raise ValueError('No rgb identification possible from "%s"'%style_string)