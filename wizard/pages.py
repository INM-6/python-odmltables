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
import copy
from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
                         QRadioButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout,
                         QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
                         QMessageBox,QWidget,QPushButton, QFileDialog, QComboBox,QListWidget,
                         QListWidgetItem,
                         QToolButton)
from PyQt4.QtCore import (pyqtSlot, QRegExp, Qt,pyqtProperty)

import odmltables.odml_table

class LoadFilePage(QWizardPage):
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
        self.inputfile = QLabel("")
        self.inputfile.setWordWrap(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.buttonbrowse)
        hbox1.addWidget(self.inputfile)

        hbox1.addStretch()
        vbox.addLayout(hbox1)

        self.cbcustominput = QCheckBox('I changed the column names in the input table.')
        self.cbcustominput.setEnabled(False)
        self.registerField('CBcustominput',self.cbcustominput)
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
        self.registerField('RBxls',self.rbuttonxls)
        self.registerField('RBcsv',self.rbuttoncsv)
        self.registerField('RBodml',self.rbuttonodml)

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
        filename = QFileDialog().getOpenFileName()
        self.inputpath = QLineEdit(filename)
        self.registerField('Linputfile',self.inputpath)
        # filename = QFileDialog.getOpenFileName()
        short_filename = self._shorten_path(str(filename))
        self.inputfile.setText(short_filename)

        if str(filename[-4:]) in ['.xls','.csv']:
            self.cbcustominput.setEnabled(True)
        else:
            self.cbcustominput.setEnabled(False)

        if str(filename[-4:]) in ['.xls','.csv']:
            self.rbuttonodml.setChecked(True)
        elif str(filename[-5:]) in ['.odml']:
            self.rbuttonxls.setChecked(True)

    def validatePage(self):
        if not any((self.field('RBxls').toBool(),
                    self.field('RBcsv').toBool(),
                    self.field('RBodml').toBool())):
            QMessageBox.warning(self,'Select a format','You need to select a table format to continue.')
            return 0

        if not self.field('Linputfile').toString():
            QMessageBox.warning(self,'Select an input file','You need to select an inupt file to continue.')
            return 0

        if self.field('Linputfile').toString().split('.')[-1] not in ['xls','csv','odml']:
            QMessageBox.warning(self,'Wrong input format','The input file has to be an ".xls", ".csv" or ".odml" file.')
            return 0

        return 1

    def _shorten_path(self,path):
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


    def nextId(self):
        if self.wizard().field('CBcustominput').toBool():
            return self.wizard().PageCustomInputHeader
        else:
            return self.wizard().currentId()+2



class CustomInputHeaderPage(QWizardPage):
    def __init__(self,parent=None):
        super(CustomInputHeaderPage, self).__init__(parent)

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
        load_from = str(self.wizard().field('Linputfile').toString())
        if load_from.endswith('.xls'):
            customheaders = odmltables.odml_table.OdmlTable.get_xls_header(load_from)
        elif load_from.endswith('.csv'):
            customheaders = odmltables.odml_table.OdmlTable.get_csv_header(load_from)
        else:
            raise TypeError('Header can be only read for xls or csv files.')


        odtables = odmltables.odml_table.OdmlTable()
        header_names = odtables._header_titles.values()

        self.n_headers = QLineEdit(str(len(customheaders)))
        self.registerField('LEn_headers',self.n_headers)

        for h, header in enumerate(customheaders):
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
            self.registerField('Lheader_%i'%(h),h_label)
            self.registerField('CBheadernames_%i'%(h),dd_list)

        self.update()

    def validatePage(self):
        header_names = []
        for h in range(int(self.wizard().field('LEn_headers').toString())):
            # header = self.wizard().field('Lheader_%i'%h).toString
            header_id = int(self.wizard().field('CBheadernames_%i'%h).toString())

            odtables = odmltables.odml_table.OdmlTable()
            header_name = odtables._header_titles.values()[header_id]

            if header_name in header_names:
                QMessageBox.warning(self, self.tr("Non-unique headers"), self.tr("Header assignment has"
                                                  " to be unique. '%s' has been"
                                                  " assigned multiple times"%header_name))
                return 0

            header_names.append(header_name)

        return 1


class QIListWidget(QListWidget):
    def __init__(self,parent=None):
        super(QIListWidget, self).__init__(parent)

    @pyqtProperty(list)
    def currentItemData(self):
        items = []
        for index in xrange(self.count()):
             items.append(self.item(index))
        labels = [i.text() for i in items]
        return items


class HeaderOrderPage(QWizardPage):
    def __init__(self,parent=None):
        super(HeaderOrderPage, self).__init__(parent)

        # Set up layout
        vbox = QVBoxLayout()

        # Adding input part
        topLabel = QLabel(self.tr("Select the columns for the output table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)


        odtables = odmltables.odml_table.OdmlTable()
        header_names = odtables._header_titles.values()

        # generating selection lists
        self.header_list = QListWidget()
        self.header_list.setSelectionMode(3)
        self.selection_list = QIListWidget()
        self.selection_list.setSelectionMode(3)
        self.registerField('LWcolumnselection',self.selection_list,'currentItemData') #TODO: Check how fields work properly
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
        self.registerField('CBcustomheader',self.cbcustomheader)
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
        if self.wizard().field('CBcustomheader').toBool:
            return self.wizard().PageCustomColumNames
        else:
            return self.wizard().currentId+1

    def validatePage(self):
        self.wizard().field('LWcolumnselection')


class CustomColumnNamesPage(QWizardPage):
    def __init__(self,parent=None):
        super(CustomColumnNamesPage, self).__init__(parent)

        # Set up layout
        vbox = QVBoxLayout()

        # Adding input part
        topLabel = QLabel(self.tr("Select the columns for the output table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)


























class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr("Introduction"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("This Wizard will help you register your copy of "
                                  "<i>Super Product One</i> or start "
                                  "evaluating the product."))
        topLabel.setWordWrap(True)

        regRBtn = QRadioButton(self.tr("&Register your copy"))
        self.evalRBtn = QRadioButton(self.tr("&Evaluate the product for 30 days"))
        regRBtn.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(regRBtn)
        layout.addWidget(self.evalRBtn)
        self.setLayout(layout)

        self.registerField('regRBtn',regRBtn)


    # def nextId(self):
    #     # if self.evalRBtn.isChecked():
    #     #     print 'Current ID %s'%(self.currentId())
    #     return self.currentId() + 1
    #     # else:
    #     #     return 2



class EvaluatePage(QWizardPage):
    def __init__(self, parent=None):
        super(EvaluatePage, self).__init__(parent)

        self.setTitle(self.tr("Evaluate <i>Super Product One</i>"))
        self.setSubTitle(self.tr("Please fill both fields. \nMake sure to provide "
                                 "a valid email address (e.g. john.smith@example.com)"))
        nameLabel = QLabel("Name: ")
        nameEdit = QLineEdit()
        nameLabel.setBuddy(nameEdit)

        emailLabel = QLabel(self.tr("&Email address: "))
        emailEdit = QLineEdit()
        emailEdit.setValidator(QRegExpValidator(
                QRegExp(".*@.*"), self))
        emailLabel.setBuddy(emailEdit)

        self.registerField("evaluate.name*", nameEdit)
        self.registerField("evaluate.email*", emailEdit)

        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(nameEdit, 0, 1)
        grid.addWidget(emailLabel, 1, 0)
        grid.addWidget(emailEdit, 1, 1)
        self.setLayout(grid)

    # def nextId(self):
    #     return odml2tableWizard.PageConclusion

    def validatePage(self):
        print 'validation'
        pass

class RegisterPage(QWizardPage):
    def __init__(self, parent=None):
        super(RegisterPage, self).__init__(parent)

        self.setTitle(self.tr("Register Your Copy of <i>Super Product One</i>"))
        self.setSubTitle(self.tr("If you have an upgrade key, please fill in "
                                 "the appropriate field."))
        nameLabel = QLabel(self.tr("N&ame"))
        nameEdit = QLineEdit()
        nameLabel.setBuddy(nameEdit)

        upgradeKeyLabel = QLabel(self.tr("&Upgrade key"))
        self.upgradeKeyEdit = QLineEdit()
        upgradeKeyLabel.setBuddy(self.upgradeKeyEdit)

        self.registerField("register.name*", nameEdit)
        self.registerField("register.upgradeKey", self.upgradeKeyEdit)

        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(nameEdit, 0, 1)
        grid.addWidget(upgradeKeyLabel, 1, 0)
        grid.addWidget(self.upgradeKeyEdit, 1, 1)

        self.setLayout(grid)

    # def nextId(self):
    #     if len(self.upgradeKeyEdit.text()) > 0 :
    #         return odml2tableWizard.PageConclusion
    #     else:
    #         return odml2tableWizard.PageDetails


class DetailsPage(QWizardPage):
    def __init__(self, parent=None):
        super(DetailsPage, self).__init__(parent)

        self.setTitle(self.tr("Fill in Your Details"))
        self.setSubTitle(self.tr("Please fill all three fields. /n"
                                 "Make sure to provide a valid "
                                 "email address (e.g., tanaka.aya@example.com)."))
        coLabel = QLabel(self.tr("&Company name: "))
        coEdit = QLineEdit()
        coLabel.setBuddy(coEdit)

        emailLabel = QLabel(self.tr("&Email address: "))
        emailEdit = QLineEdit()
        emailEdit.setValidator(QRegExpValidator(QRegExp(".*@.*"), self))
        emailLabel.setBuddy(emailEdit)

        postLabel = QLabel(self.tr("&Postal address: "))
        postEdit = QLineEdit()
        postLabel.setBuddy(postEdit)

        self.registerField("details.company*", coEdit)
        self.registerField("details.email*", emailEdit)
        self.registerField("details.postal*", postEdit)

        grid = QGridLayout()
        grid.addWidget(coLabel, 0, 0)
        grid.addWidget(coEdit, 0, 1)
        grid.addWidget(emailLabel, 1, 0)
        grid.addWidget(emailEdit, 1, 1)
        grid.addWidget(postLabel, 2, 0)
        grid.addWidget(postEdit, 2, 1)
        self.setLayout(grid)

    # def nextId(self):
    #     return odml2tableWizard.PageConclusion

class ConclusionPage(QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle(self.tr("Complete Your Registration"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))

        self.bottomLabel = QLabel()
        self.bottomLabel.setWordWrap(True)

        agreeBox = QCheckBox(self.tr("I agree to the terms of the license."))

        self.registerField("conclusion.agree*", agreeBox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.bottomLabel)
        vbox.addWidget(agreeBox)
        self.setLayout(vbox)

    # def nextId(self):
    #     return -1

    def initializePage(self):
        licenseText = ''

        # if self.wizard().hasVisitedPage(odml2tableWizard.PageEvaluate):
        #     licenseText = self.tr("<u>Evaluation License Agreement:</u> "
        #                   "You can use this software for 30 days and make one "
        #                   "backup, but you are not allowed to distribute it.")
        # elif self.wizard().hasVisitedPage(odml2tableWizard.PageDetails):
        #     licenseText = self.tr("<u>First-Time License Agreement:</u> "
        #                   "You can use this software subject to the license "
        #                   "you will receive by email.")
        # else:
        #     licenseText = self.tr("<u>Upgrade License Agreement:</u> "
        #                   "This software is licensed under the terms of your "
        #                   "current license.")

        licenseText = 'Put License Text here.'

        self.bottomLabel.setText(licenseText)

    def setVisible(self, visible):
        # only show the 'Print' button on the last page
        QWizardPage.setVisible(self, visible)

        if visible:
            self.wizard().setButtonText(QWizard.CustomButton1, self.tr("&Print"))
            self.wizard().setOption(QWizard.HaveCustomButton1, True)
            self.wizard().customButtonClicked.connect(self._printButtonClicked)
            self._configWizBtns(True)
        else:
            # only disconnect if button has been assigned and connected
            btn = self.wizard().button(QWizard.CustomButton1)
            if len(btn.text()) > 0:
                self.wizard().customButtonClicked.disconnect(self._printButtonClicked)

            self.wizard().setOption(QWizard.HaveCustomButton1, False)
            self._configWizBtns(False)

    def _configWizBtns(self, state):
        # position the Print button (CustomButton1) before the Finish button
        if state:
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.CustomButton1, QWizard.FinishButton,
                       QWizard.CancelButton, QWizard.HelpButton]
            self.wizard().setButtonLayout(btnList)
        else:
            # remove it if it's not visible
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.FinishButton,
                       QWizard.CancelButton, QWizard.HelpButton]
            self.wizard().setButtonLayout(btnList)

    @pyqtSlot()
    def _printButtonClicked(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_():
            QMessageBox.warning(self,
                                self.tr("Print License"),
                                self.tr("As an environment friendly measure, the "
                                        "license text will not actually be printed."))