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
import pickle
import copy
import xlwt
from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
                         QRadioButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout,
                         QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
                         QMessageBox,QWidget,QPushButton, QFileDialog, QComboBox,QListWidget,
                         QListWidgetItem, QTableView,QFont,QPalette,QFrame,QSizePolicy,
                         QToolButton,QColor,QItemEditorCreatorBase)
from PyQt4.QtCore import (pyqtSlot, QRegExp, Qt,pyqtProperty,SIGNAL)

from  odmltables import odml_table, odml_xls_table, odml_csv_table



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
        if self.inputfilename[-5:] != '.odml':
            if self.settings.get_object('CBcustominput').isChecked():
                return self.wizard().PageCustomInputHeader
            else:
                return self.wizard().PageHeaderOrder
        else:
            if (self.settings.get_object('RBoutputxls').isChecked() or
                self.settings.get_object('RBoutputcsv').isChecked()):

                return self.wizard().PageHeaderOrder

            else:
                return self.wizard().PageSaveFile




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
        for h in self.customheaders:

            header_name = h.currentText()

            if header_name in header_names:
                QMessageBox.warning(self, self.tr("Non-unique headers"), self.tr("Header assignment has"
                                                  " to be unique. '%s' has been"
                                                  " assigned multiple times"%header_name))
                return 0

            header_names.append(header_name)

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
                                    " generate an odml from the table."))

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

        self.tablebuttons = [None]*5

        texts = ['Header','Standard\nRow 1', 'Standard\nRow 2','Marked \nRow 1','Marked \nRow 2']
        default_styles = ['color: white; background-color: gray; font:bold',
                          'color: white; background-color: green',
                          'color: white; background-color: blue',
                          'color: white; background-color: red',
                          'color: white; background-color: orange']
        common_default = "; padding-left: 5px; padding-right: 5px; padding-top: 5px; padding-bottom: 5px; border-color: red" #background-color: rgb(0, 255, 255);
        # ''padding: 6px'
        positions = [(0,0,1,2),(1,0),(2,0),(1,1),(2,1)]

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

        self.settings.register('GLtablegrid',gridtable)

        gridtable.setSpacing(0)

        vstretcher = QVBoxLayout()
        vstretcher.addStretch(1)
        vstretcher.addLayout(gridtable)
        vstretcher.addStretch(1)

        hbox.addLayout(vstretcher)

        # adding separator
        verticalLine = QFrame()
        verticalLine.setFrameStyle(QFrame.VLine)
        verticalLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        hbox.addWidget(verticalLine)


        self.cbbgcolor = ColorListWidget()
        self.cbbgcolor.currentIndexChanged.connect(self.updatetable)

        self.cbfontcolor = ColorListWidget()
        self.cbfontcolor.currentIndexChanged.connect(self.updatetable)

        self.cbboldfont = QCheckBox('bold')
        self.cbboldfont.setStyleSheet('font:bold')
        self.cbboldfont.toggled.connect(self.updatetable)
        self.cbitalicfont = QCheckBox('italic')
        self.cbitalicfont.setStyleSheet('font:italic')
        self.cbitalicfont.toggled.connect(self.updatetable)

        gridsettings = QGridLayout()
        self.settingstitle = QLabel()
        self.settingstitle.setText(self.tablebuttons[0].text())
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
        color = self.get_property(sender.styleSheet(),'background-color').strip().rstrip()
        index = self.cbbgcolor.findText(color, Qt.MatchFixedString)
        if index >= 0:
            self.cbbgcolor.setCurrentIndex(index)
        # update fontcolor
        color = self.get_property(sender.styleSheet(),'color').strip().rstrip()
        index = self.cbfontcolor.findText(color, Qt.MatchFixedString)
        if index >= 0:
            self.cbfontcolor.setCurrentIndex(index)
        #update font style
        font_style = self.get_property(sender.styleSheet(),'font')
        if font_style == None: font_style = ''
        self.cbboldfont.setChecked('bold' in font_style)
        self.cbitalicfont.setChecked('italic' in font_style)


    def updatetable(self):
        # get current settings from settings dialog
        style = ';'
        style += 'background-color:rgb%s;'%(str(self.cbbgcolor.get_current_rgb()))
        style += 'color:rgb%s;'%(str(self.cbfontcolor.get_current_rgb()))
        if self.cbboldfont.isChecked():
            style += 'font:bold'
            if self.cbitalicfont.isChecked():
                style.rstrip(';')
                style += ' italic;'
        elif self.cbitalicfont.isChecked(): style += 'font:italic;'

        old_style = self.removestyle(self.currentbutton.styleSheet(),'font')

        self.currentbutton.setStyleSheet(old_style + style)

    def removestyle(self,style,property):
        styles = [str(s) for s in style.split(';')]
        s = 0
        while s < len(styles):
            if styles[s].strip(' ').startswith(property+':'):
                styles.pop(s)
            else:
                s += 1
        return '; '.join(styles)

    def get_property(self,style,property):
        styles = [str(s) for s in style.split(';')]
        for s in styles:
            if s.strip(' ').startswith(property+':'):
                return s.replace(property+':','')



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
        for i in range(64):
            cnames = [name for name, index in cmap.items() if index == i]
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
        elif ((os.path.splitext(self.outputfilename)[1]!=expected_extension) and
                  (os.path.splitext(self.outputfilename)[1]!='')):
            QMessageBox.warning(self,'Wrong file format','The output file format is supposed to be "%s",'
                                                         ' but you selected "%s"'
                                                         ''%(expected_extension,
                                                             os.path.splitext(self.outputfilename)[1]))
        # extending filename if no extension is present
        if os.path.splitext(self.outputfilename)[1]=='':
            self.outputfilename += expected_extension

        convert(self.settings)


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
        headerlabels = [l.text() for l in settings.get_object('headerlabels')]
        customheaders = [cb.getCurrentItem().text() for cb in settings.get_object('customheaders')]

        table.change_header_titles(**zip(customheaders,headerlabels))

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

    settings.get_object('')

    odml_table





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











#
#
# class IntroPage(QWizardPage):
#     def __init__(self, parent=None):
#         super(IntroPage, self).__init__(parent)
#
#         self.setTitle(self.tr("Introduction"))
#         self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
#         topLabel = QLabel(self.tr("This Wizard will help you register your copy of "
#                                   "<i>Super Product One</i> or start "
#                                   "evaluating the product."))
#         topLabel.setWordWrap(True)
#
#         regRBtn = QRadioButton(self.tr("&Register your copy"))
#         self.evalRBtn = QRadioButton(self.tr("&Evaluate the product for 30 days"))
#         regRBtn.setChecked(True)
#
#         layout = QVBoxLayout()
#         layout.addWidget(topLabel)
#         layout.addWidget(regRBtn)
#         layout.addWidget(self.evalRBtn)
#         self.setLayout(layout)
#
#         self.registerField('regRBtn',regRBtn)
#
#
#     # def nextId(self):
#     #     # if self.evalRBtn.isChecked():
#     #     #     print 'Current ID %s'%(self.currentId())
#     #     return self.currentId() + 1
#     #     # else:
#     #     #     return 2
#
#
#
# class EvaluatePage(QWizardPage):
#     def __init__(self, parent=None):
#         super(EvaluatePage, self).__init__(parent)
#
#         self.setTitle(self.tr("Evaluate <i>Super Product One</i>"))
#         self.setSubTitle(self.tr("Please fill both fields. \nMake sure to provide "
#                                  "a valid email address (e.g. john.smith@example.com)"))
#         nameLabel = QLabel("Name: ")
#         nameEdit = QLineEdit()
#         nameLabel.setBuddy(nameEdit)
#
#         emailLabel = QLabel(self.tr("&Email address: "))
#         emailEdit = QLineEdit()
#         emailEdit.setValidator(QRegExpValidator(
#                 QRegExp(".*@.*"), self))
#         emailLabel.setBuddy(emailEdit)
#
#         self.registerField("evaluate.name*", nameEdit)
#         self.registerField("evaluate.email*", emailEdit)
#
#         grid = QGridLayout()
#         grid.addWidget(nameLabel, 0, 0)
#         grid.addWidget(nameEdit, 0, 1)
#         grid.addWidget(emailLabel, 1, 0)
#         grid.addWidget(emailEdit, 1, 1)
#         self.setLayout(grid)
#
#     # def nextId(self):
#     #     return odml2tableWizard.PageConclusion
#
#     def validatePage(self):
#         print 'validation'
#         pass
#
# class RegisterPage(QWizardPage):
#     def __init__(self, parent=None):
#         super(RegisterPage, self).__init__(parent)
#
#         self.setTitle(self.tr("Register Your Copy of <i>Super Product One</i>"))
#         self.setSubTitle(self.tr("If you have an upgrade key, please fill in "
#                                  "the appropriate field."))
#         nameLabel = QLabel(self.tr("N&ame"))
#         nameEdit = QLineEdit()
#         nameLabel.setBuddy(nameEdit)
#
#         upgradeKeyLabel = QLabel(self.tr("&Upgrade key"))
#         self.upgradeKeyEdit = QLineEdit()
#         upgradeKeyLabel.setBuddy(self.upgradeKeyEdit)
#
#         self.registerField("register.name*", nameEdit)
#         self.registerField("register.upgradeKey", self.upgradeKeyEdit)
#
#         grid = QGridLayout()
#         grid.addWidget(nameLabel, 0, 0)
#         grid.addWidget(nameEdit, 0, 1)
#         grid.addWidget(upgradeKeyLabel, 1, 0)
#         grid.addWidget(self.upgradeKeyEdit, 1, 1)
#
#         self.setLayout(grid)
#
#     # def nextId(self):
#     #     if len(self.upgradeKeyEdit.text()) > 0 :
#     #         return odml2tableWizard.PageConclusion
#     #     else:
#     #         return odml2tableWizard.PageDetails
#
#
# class DetailsPage(QWizardPage):
#     def __init__(self, parent=None):
#         super(DetailsPage, self).__init__(parent)
#
#         self.setTitle(self.tr("Fill in Your Details"))
#         self.setSubTitle(self.tr("Please fill all three fields. /n"
#                                  "Make sure to provide a valid "
#                                  "email address (e.g., tanaka.aya@example.com)."))
#         coLabel = QLabel(self.tr("&Company name: "))
#         coEdit = QLineEdit()
#         coLabel.setBuddy(coEdit)
#
#         emailLabel = QLabel(self.tr("&Email address: "))
#         emailEdit = QLineEdit()
#         emailEdit.setValidator(QRegExpValidator(QRegExp(".*@.*"), self))
#         emailLabel.setBuddy(emailEdit)
#
#         postLabel = QLabel(self.tr("&Postal address: "))
#         postEdit = QLineEdit()
#         postLabel.setBuddy(postEdit)
#
#         self.registerField("details.company*", coEdit)
#         self.registerField("details.email*", emailEdit)
#         self.registerField("details.postal*", postEdit)
#
#         grid = QGridLayout()
#         grid.addWidget(coLabel, 0, 0)
#         grid.addWidget(coEdit, 0, 1)
#         grid.addWidget(emailLabel, 1, 0)
#         grid.addWidget(emailEdit, 1, 1)
#         grid.addWidget(postLabel, 2, 0)
#         grid.addWidget(postEdit, 2, 1)
#         self.setLayout(grid)
#
#     # def nextId(self):
#     #     return odml2tableWizard.PageConclusion
#
# class ConclusionPage(QWizardPage):
#     def __init__(self, parent=None):
#         super(ConclusionPage, self).__init__(parent)
#
#         self.setTitle(self.tr("Complete Your Registration"))
#         self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
#
#         self.bottomLabel = QLabel()
#         self.bottomLabel.setWordWrap(True)
#
#         agreeBox = QCheckBox(self.tr("I agree to the terms of the license."))
#
#         self.registerField("conclusion.agree*", agreeBox)
#
#         vbox = QVBoxLayout()
#         vbox.addWidget(self.bottomLabel)
#         vbox.addWidget(agreeBox)
#         self.setLayout(vbox)
#
#     # def nextId(self):
#     #     return -1
#
#     def initializePage(self):
#         licenseText = ''
#
#         # if self.wizard().hasVisitedPage(odml2tableWizard.PageEvaluate):
#         #     licenseText = self.tr("<u>Evaluation License Agreement:</u> "
#         #                   "You can use this software for 30 days and make one "
#         #                   "backup, but you are not allowed to distribute it.")
#         # elif self.wizard().hasVisitedPage(odml2tableWizard.PageDetails):
#         #     licenseText = self.tr("<u>First-Time License Agreement:</u> "
#         #                   "You can use this software subject to the license "
#         #                   "you will receive by email.")
#         # else:
#         #     licenseText = self.tr("<u>Upgrade License Agreement:</u> "
#         #                   "This software is licensed under the terms of your "
#         #                   "current license.")
#
#         licenseText = 'Put License Text here.'
#
#         self.bottomLabel.setText(licenseText)
#
#     def setVisible(self, visible):
#         # only show the 'Print' button on the last page
#         QWizardPage.setVisible(self, visible)
#
#         if visible:
#             self.wizard().setButtonText(QWizard.CustomButton1, self.tr("&Print"))
#             self.wizard().setOption(QWizard.HaveCustomButton1, True)
#             self.wizard().customButtonClicked.connect(self._printButtonClicked)
#             self._configWizBtns(True)
#         else:
#             # only disconnect if button has been assigned and connected
#             btn = self.wizard().button(QWizard.CustomButton1)
#             if len(btn.text()) > 0:
#                 self.wizard().customButtonClicked.disconnect(self._printButtonClicked)
#
#             self.wizard().setOption(QWizard.HaveCustomButton1, False)
#             self._configWizBtns(False)
#
#     def _configWizBtns(self, state):
#         # position the Print button (CustomButton1) before the Finish button
#         if state:
#             btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
#                        QWizard.CustomButton1, QWizard.FinishButton,
#                        QWizard.CancelButton, QWizard.HelpButton]
#             self.wizard().setButtonLayout(btnList)
#         else:
#             # remove it if it's not visible
#             btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
#                        QWizard.FinishButton,
#                        QWizard.CancelButton, QWizard.HelpButton]
#             self.wizard().setButtonLayout(btnList)
#
#     @pyqtSlot()
#     def _printButtonClicked(self):
#         printer = QPrinter()
#         dialog = QPrintDialog(printer, self)
#         if dialog.exec_():
#             QMessageBox.warning(self,
#                                 self.tr("Print License"),
#                                 self.tr("As an environment friendly measure, the "
#                                         "license text will not actually be printed."))