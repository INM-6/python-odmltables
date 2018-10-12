# -*- coding: utf-8 -*-
import copy
import sys
import os
import subprocess
import xlwt

from future.utils import iteritems

from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg

from .pageutils import QIWizardPage, clearLayout, get_property, get_rgb, shorten_path
from odmltables import odml_table, odml_xls_table, odml_csv_table, xls_style


class LoadFilePage(QIWizardPage):
    def __init__(self, parent=None, filename=None):
        super(LoadFilePage, self).__init__(parent)

        if filename is None:
            self.inputfilename = ''
        else:
            self.inputfilename = filename
        self.settings.register('inputfilename', self, useconfig=False)

        # Set up layout
        self.layout = Qtw.QVBoxLayout()
        self.setLayout(self.layout)

    def initializePage(self):

        self.setTitle("Select an input file")
        self.setSubTitle("Select the file you want to convert and specify the"
                         " output format you want to generate")

        vbox = self.layout

        # Adding input part
        topLabel = Qtw.QLabel(self.tr("Choose a file to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        # vbox.addSpacing(10)

        # Add first horizontal box
        self.buttonbrowse = Qtw.QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.inputfile = Qtw.QLabel(self.inputfilename)
        self.inputfile.setWordWrap(True)
        hbox1 = Qtw.QHBoxLayout()
        hbox1.addWidget(self.buttonbrowse)
        hbox1.addWidget(self.inputfile)

        hbox1.addStretch()
        vbox.addLayout(hbox1)

        self.cbcustominput = Qtw.QCheckBox('I changed the column names in the'
                                           ' input table.')
        self.cbcustominput.setEnabled(False)
        self.settings.register('CBcustominput', self.cbcustominput)
        vbox.addWidget(self.cbcustominput)
        vbox.addStretch()

        # adding configuration selection
        configlabel = Qtw.QLabel('Load a configuration from a previous run')
        vbox.addWidget(configlabel)
        self.configselection = Qtw.QComboBox()
        self.configselection.addItems(self.settings.get_all_config_names())
        self.configselection.insertItem(0, '-- No configuration --')
        self.configselection.setCurrentIndex(0)
        self.configselection.activated.connect(self.selectconfig)
        vbox.addWidget(self.configselection)

        # adding separator
        horizontalLine = Qtw.QFrame()
        horizontalLine.setFrameStyle(Qtw.QFrame.HLine)
        horizontalLine.setSizePolicy(Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)

        # Adding output part
        bottomLabel = Qtw.QLabel(self.tr("Select an output format"))
        bottomLabel.setWordWrap(True)
        vbox.addWidget(bottomLabel)
        vbox.addWidget(bottomLabel)

        # Add second horizontal box
        self.rbuttonxls = Qtw.QRadioButton(self.tr("xls"))
        self.rbuttoncsv = Qtw.QRadioButton(self.tr("csv"))
        self.rbuttonodml = Qtw.QRadioButton(self.tr("odml"))

        self.settings.register('RBoutputxls', self.rbuttonxls)
        self.settings.register('RBoutputcsv', self.rbuttoncsv)
        self.settings.register('RBoutputodml', self.rbuttonodml)

        hbox2 = Qtw.QHBoxLayout()
        hbox2.addWidget(self.rbuttonxls)
        hbox2.addSpacing(50)
        hbox2.addWidget(self.rbuttoncsv)
        hbox2.addSpacing(50)
        hbox2.addWidget(self.rbuttonodml)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        vbox.addStretch()

    def selectconfig(self):
        if self.configselection.currentIndex() != 0:
            self.settings.load_config(str(self.configselection.currentText()))

            # loading output format choice
            self.settings.register('RBoutputxls', self.rbuttonxls)
            self.settings.register('RBoutputcsv', self.rbuttoncsv)
            self.settings.register('RBoutputodml', self.rbuttonodml)
            self.settings.register('CBcustominput', self.cbcustominput)
            self.settings.register('inputfilename', self, useconfig=False)
            short_filename = shorten_path(self.settings.get_object('inputfilename'))
            self.inputfile.setText(short_filename)
            # self.settings.get_object('RBoutputxls')

    def handlebuttonbrowse(self):
        dlg = Qtw.QFileDialog()
        fn = self.settings.get_object('inputfilename')
        if fn:
            dlg.selectFile(fn)

        if dlg.exec_():
            self.inputfilename = str(dlg.selectedFiles()[0])

        self.settings.register('inputfilename', self, useconfig=False)
        self.inputfile.setText(shorten_path(self.inputfilename))

        if str(self.inputfilename[-4:]) in ['.xls', '.csv']:
            self.cbcustominput.setEnabled(True)
        else:
            self.cbcustominput.setEnabled(False)

        if not (self.rbuttonxls.isChecked()
                or self.rbuttoncsv.isChecked()
                or self.rbuttonodml.isChecked()):
            if str(self.inputfilename[-4:]) in ['.xls', '.csv']:
                self.rbuttonodml.setChecked(True)
            elif (str(self.inputfilename[-5:]) in ['.odml']
                  or str(self.inputfilename[-4:]) in ['.xml']):
                self.rbuttonxls.setChecked(True)

    def validatePage(self):
        if not any((self.settings.get_object('RBoutputxls').isChecked(),
                    self.settings.get_object('RBoutputcsv').isChecked(),
                    self.settings.get_object('RBoutputodml').isChecked())):
            Qtw.QMessageBox.warning(self, 'Select a format', 'You need to select a '
                                                             'table format to '
                                                             'continue.')
            return 0

        if ((not self.settings.is_registered('inputfilename')) or
                (not self.settings.get_object('inputfilename'))):
            Qtw.QMessageBox.warning(self, 'Select an input file',
                                    'You need to select'
                                    ' an input file to '
                                    'continue.')
            return 0

        elif self.settings.get_object('inputfilename').split('.')[-1] not in \
                ['xls', 'csv', 'odml', 'xml']:
            Qtw.QMessageBox.warning(self, 'Wrong input format',
                                    'The input file has to be an ".xls", ".csv", ".odml" or '
                                    '".xml" file.')
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
    def __init__(self, parent=None):
        super(CustomInputHeaderPage, self).__init__(parent)

        self.setTitle("Provide information about your input file")
        self.setSubTitle("Which titles were used for which odml column in you "
                         "input file. Select the corresponding odml columns.")

        # Set up layout
        self.vbox = Qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        # self.vbox = QVBoxLayout()
        # self.layout.addLayout(self.vbox)

    def initializePage(self):

        # Set up layout
        vbox = Qtw.QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        # Adding input part
        topLabel = Qtw.QLabel(self.tr("Provide the column types used in the input "
                                      "table"))
        topLabel.setWordWrap(True)
        vbox.addSpacing(20)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        self.grid = Qtw.QGridLayout()
        vbox.addLayout(self.grid)

        # self.setLayout(vbox)

        # get header names from input file
        load_from = str(self.settings.get_object('inputfilename'))
        if load_from.endswith('.xls'):
            inputxlsheaders = odml_table.OdmlTable.get_xls_header(load_from)
        elif load_from.endswith('.csv'):
            inputxlsheaders = odml_table.OdmlTable.get_csv_header(load_from)
        else:
            raise TypeError('Header can be only read for xls or csv files.')

        odtables = odml_table.OdmlTable()
        header_names = list(odtables._header_titles.values())

        self.headerlabels = []
        self.customheaders = []

        for h, header in enumerate(inputxlsheaders):
            # set up individual row for header association
            h_label = Qtw.QLabel(header)
            dd_list = Qtw.QComboBox()
            dd_list.addItems(header_names)
            # Preselect fitting header name if possible
            if header in header_names:
                ind = header_names.index(header)
                dd_list.setCurrentIndex(ind)
            self.grid.addWidget(h_label, h, 0)
            self.grid.addWidget(dd_list, h, 1)
            self.headerlabels.append(h_label)
            self.customheaders.append(dd_list)

        self.settings.register('headerlabels', self.headerlabels)
        self.settings.register('customheaders', self.customheaders)

        self.update()

    def validatePage(self):
        header_names = []

        # check for duplicate headers
        for h in self.customheaders:
            header_name = h.currentText()
            if header_name in header_names:
                Qtw.QMessageBox.warning(self,
                                        self.tr("Non-unique headers"),
                                        self.tr("Header assignment has"
                                                " to be unique. '%s' has been"
                                                " assigned multiple times" %
                                                header_name))
                return 0
            header_names.append(header_name)

        # check for mandatory headers
        mandatory_headers = ['Path to Section', 'Property Name', 'Value',
                             'odML Data Type']
        for mand_head in mandatory_headers:
            if mand_head not in header_names:
                Qtw.QMessageBox.warning(self,
                                        self.tr("Incomplete headers"),
                                        self.tr("You need to have the mandatory"
                                                " headers %s in you table to be"
                                                " able to reconstruct an odml"
                                                "" % mandatory_headers))
                return 0
        return 1

    def nextId(self):
        if self.settings.get_object('RBoutputodml').isChecked():
            return self.wizard().PageSaveFile

        return self.wizard().PageHeaderOrder


class HeaderOrderPage(QIWizardPage):
    def __init__(self, parent=None):
        super(HeaderOrderPage, self).__init__(parent)

        self.setTitle("Customize the output table")
        self.setSubTitle("Select the columns for the output table by putting "
                         "them in the list of selected columns and arranging "
                         "the order using the buttons to the right")

        # Set up layout
        vbox = Qtw.QVBoxLayout()
        self.setLayout(vbox)

        topLabel = Qtw.QLabel(self.tr("Select the columns for the output table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        hbox0 = Qtw.QHBoxLayout()
        hbox0.addStretch()
        hbox0.addWidget(Qtw.QLabel('available columns'))
        hbox0.addStretch()
        hbox0.addSpacing(90)
        hbox0.addWidget(Qtw.QLabel('selected columns'))
        hbox0.addStretch()
        hbox0.addSpacing(30)

        vbox.addLayout(hbox0)

        # Adding input part
        odtables = odml_table.OdmlTable()
        self.header_names = list(odtables._header_titles.values())

        # generating selection lists
        self.header_list = Qtw.QListWidget()
        self.header_list.setSelectionMode(3)
        self.header_list.itemDoubleClicked.connect(self.itemdoubleclicked)
        self.selection_list = Qtw.QListWidget()
        self.selection_list.setSelectionMode(3)
        self.selection_list.itemDoubleClicked.connect(self.itemdoubleclicked)

        toright = Qtw.QToolButton()
        toright.setArrowType(Qt.RightArrow)
        toright.clicked.connect(self.toright)
        toleft = Qtw.QToolButton()
        toleft.setArrowType(Qt.LeftArrow)
        toleft.clicked.connect(self.toleft)

        hbox = Qtw.QHBoxLayout()
        hbox.addWidget(self.header_list)
        vboxbuttons = Qtw.QVBoxLayout()
        vboxbuttons.addStretch()
        vboxbuttons.addWidget(toright)
        vboxbuttons.addSpacing(30)
        vboxbuttons.addWidget(toleft)
        vboxbuttons.addStretch()
        hbox.addLayout(vboxbuttons)

        vbox.addLayout(hbox)

        default_selection_list = ['Path to Section',
                                  'Property Name',
                                  'Value',
                                  'odML Data Type']
        self.mandatory_headers = copy.deepcopy(default_selection_list)
        for i, h in enumerate(self.header_names):
            if h not in default_selection_list:
                item = Qtw.QListWidgetItem()
                item.setText(h)
                self.header_list.addItem(item)
            else:
                item = Qtw.QListWidgetItem()
                item.setText(h)

                self.selection_list.addItem(item)

        hbox.addWidget(self.selection_list)

        # adding up and down buttons
        up = Qtw.QToolButton()
        up.setArrowType(Qt.UpArrow)
        up.clicked.connect(self.up)
        down = Qtw.QToolButton()
        down.setArrowType(Qt.DownArrow)
        down.clicked.connect(self.down)

        vboxbuttons2 = Qtw.QVBoxLayout()
        vboxbuttons2.addStretch()
        vboxbuttons2.addWidget(up)
        vboxbuttons2.addSpacing(30)
        vboxbuttons2.addWidget(down)
        vboxbuttons2.addStretch()
        hbox.addLayout(vboxbuttons2)

        vbox.addSpacing(20)

    def initializePage(self):
        # Set up layout

        self.settings.register('LWselectedcolumns', self.selection_list)
        self.settings.register('LWnonselectedcolumns', self.header_list)

    def toright(self):
        # sort rows in descending order in order to compensate shifting
        # due to takeItem
        rows = sorted(
            [index.row() for index in self.header_list.selectedIndexes()],
            reverse=True)
        for row in rows:
            self.selection_list.addItem(self.header_list.takeItem(row))

    def toleft(self):
        # sort rows in descending order in order to compensate shifting
        #  due to takeItem
        rows = sorted([index.row() for index in
                       self.selection_list.selectedIndexes()],
                      reverse=True)
        for row in rows:
            self.header_list.addItem(self.selection_list.takeItem(row))

    def up(self):
        currentRow = self.selection_list.currentRow()
        currentItem = self.selection_list.takeItem(currentRow)
        self.selection_list.insertItem(currentRow - 1, currentItem)
        self.selection_list.setCurrentRow(currentRow - 1)

    def down(self):
        currentRow = self.selection_list.currentRow()
        currentItem = self.selection_list.takeItem(currentRow)
        self.selection_list.insertItem(currentRow + 1, currentItem)
        self.selection_list.setCurrentRow(currentRow + 1)

    def itemdoubleclicked(self):
        sender = self.sender()

        if sender == self.header_list:
            self.toright()
        elif sender == self.selection_list:
            self.toleft()
        else:
            raise ValueError('Unknown sender')

    def validatePage(self):

        # check number of selected headers
        if self.settings.get_object('LWselectedcolumns').count() < 1:
            Qtw.QMessageBox.warning(self, self.tr("No header selected"),
                                    self.tr("You need to select at least one header"
                                            " to generate a table representation "
                                            "of an odml."))
            return 0

        selectedheaderstrings = []
        for itemid in list(range(self.settings.get_object(
                'LWselectedcolumns').count())):
            selectedheaderstrings.append(self.settings.get_object(
                'LWselectedcolumns').item(itemid).text())

        missing_headers = []
        for mand_header in self.mandatory_headers:
            if mand_header not in selectedheaderstrings:
                missing_headers.append(mand_header)

        if missing_headers != []:
            Qtw.QMessageBox.warning(self, self.tr("Incomplete odml"),
                                    self.tr("You need to include the headers %s "
                                            " in your table if you want to be "
                                            "able to generate an odml from the table." % (
                                                missing_headers)))

        return 1


class CustomColumnNamesPage(QIWizardPage):
    def __init__(self, parent=None):
        super(CustomColumnNamesPage, self).__init__(parent)

        # Set up layout
        vbox = Qtw.QVBoxLayout()
        self.setLayout(vbox)

        self.setTitle("Customize the output table")
        self.setSubTitle("Define the titles to be displayed for the "
                         "different odml columns in your output table")

    def initializePage(self):
        # Set up layout
        vbox = Qtw.QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        topLabel = Qtw.QLabel(self.tr("Customize header names of output table"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        self.grid = Qtw.QGridLayout()
        vbox.addLayout(self.grid)

        # Adding input part
        # get selected columns from HeaderOrderPage
        selectedheaderstrings = []
        for itemid in list(range(self.settings.get_object(
                'LWselectedcolumns').count())):
            selectedheaderstrings.append(self.settings.get_object(
                'LWselectedcolumns').item(itemid).text())

        # show marking option only for xls output
        enable_marking = False
        if self.settings.get_object('RBoutputxls').isChecked():
            enable_marking = True

        # clear grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
            # self.grid.removeWidget(widget)
        self.grid.invalidate()

        self.customheaderlabels = []
        self.columnmarkings = False
        headerlabel = Qtw.QLabel('Odml Header')
        headerlabel.setStyleSheet('font: bold 14px')
        self.grid.addWidget(headerlabel, 0, 0)
        customlabel = Qtw.QLabel('Customized Label')
        customlabel.setStyleSheet('font: bold 14px')
        self.grid.addWidget(customlabel, 0, 1)
        if enable_marking:
            markinglabel = Qtw.QLabel('Highlight Column')
            markinglabel.setStyleSheet('font: bold 14px')
            self.grid.addWidget(markinglabel, 0, 2)

        for h, selheaderstr in enumerate(selectedheaderstrings):
            label = Qtw.QLabel(selheaderstr)
            customheader = Qtw.QLineEdit()
            customheader.setText(selheaderstr)
            self.customheaderlabels.append(customheader)
            self.grid.addWidget(label, h + 1, 0)
            self.grid.addWidget(customheader, h + 1, 1)
            if enable_marking:
                cbmarking = Qtw.QCheckBox()
                self.grid.addWidget(cbmarking, h + 1, 2)
                if self.columnmarkings == False:
                    self.columnmarkings = []
                self.columnmarkings.append(cbmarking)
                self.grid.setAlignment(cbmarking, Qt.AlignCenter)

        try:
            self.settings.register('customheaderlabels',
                                   self.customheaderlabels)
            self.settings.register('columnmarkings', self)
        except IndexError:
            self.settings.register('customheaderlabels',
                                   self.customheaderlabels,
                                   useconfig=False)
            self.settings.register('columnmarkings', self.columnmarkings,
                                   useconfig=False)

    def validatePage(self):
        # get manually entered labels
        customlabels = [le.text() for le in self.settings.get_object('customheaderlabels')]

        if any([label == '' for label in customlabels]):
            Qtw.QMessageBox.warning(self, self.tr("Empty header name"),
                                    self.tr(
                                        "You need to provide a unique, "
                                        "non empty "
                                        "name for each of your selected "
                                        "headers"))
            return 0

        for l, label in enumerate(customlabels):
            if label in customlabels[:l] + customlabels[l + 1:]:
                Qtw.QMessageBox.warning(self, self.tr("Ambiguous header name"),
                                        self.tr(
                                            "You used '%s' as label for "
                                            "multiple "
                                            "headers. "
                                            " You need to provide a unique "
                                            " name for each of your selected "
                                            "headers" % (
                                                label)))
                return 0

        return 1

    def nextId(self):
        if self.settings.get_object('RBoutputxls').isChecked():
            return self.wizard().currentId() + 1
        else:
            return self.wizard().PageSaveFile


class ColorPatternPage(QIWizardPage):
    def __init__(self, parent=None):
        super(ColorPatternPage, self).__init__(parent)

        self.setTitle("Customize the output table")
        self.setSubTitle("Select the color pattern and style to be used in "
                         "the xls table")

        # Set up layout
        self.vbox = Qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def initializePage(self):
        # Set up layout
        vbox = Qtw.QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        # adding pattern selection part
        topLabel = Qtw.QLabel(self.tr("Which color pattern shall be used?"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        self.rbalternating = Qtw.QRadioButton('alternating')
        self.rbcheckerboard = Qtw.QRadioButton('checkerboard')
        self.rbnopattern = Qtw.QRadioButton('no pattern')

        patterngroup = Qtw.QButtonGroup(vbox)
        patterngroup.addButton(self.rbalternating)
        patterngroup.addButton(self.rbcheckerboard)
        patterngroup.addButton(self.rbnopattern)

        self.rbalternating.setChecked(True)
        self.rbnopattern.toggled.connect(self.updatelayout)

        self.settings.register('RBalternating', self.rbalternating)
        self.settings.register('RBcheckerboard', self.rbcheckerboard)
        self.settings.register('RBnopattern', self.rbnopattern)

        vbox.addWidget(self.rbalternating)
        vbox.addWidget(self.rbcheckerboard)
        vbox.addWidget(self.rbnopattern)

        vbox.addSpacing(40)

        # adding style switch part
        self.bottomLabel = Qtw.QLabel(self.tr("When shall the style switch? "
                                              "Beginning of a new"))
        self.bottomLabel.setWordWrap(True)
        # self.bottomLabel.setEnabled(False)
        vbox.addWidget(self.bottomLabel)
        vbox.addSpacing(20)

        self.rbsection = Qtw.QRadioButton('Section')
        self.rbproperty = Qtw.QRadioButton('Property')
        self.rbvalue = Qtw.QRadioButton('Value')

        self.rbsection.setChecked(True)

        # self.rbsection.setEnabled(False)
        # self.rbproperty.setEnabled(False)
        # self.rbvalue.setEnabled(False)

        self.settings.register('RBsection', self.rbsection)
        self.settings.register('RBproperty', self.rbproperty)
        self.settings.register('RBvalue', self.rbvalue)

        changegroup = Qtw.QButtonGroup(vbox)
        changegroup.addButton(self.rbsection)
        changegroup.addButton(self.rbproperty)
        changegroup.addButton(self.rbvalue)

        vbox.addWidget(self.rbsection)
        vbox.addWidget(self.rbproperty)
        vbox.addWidget(self.rbvalue)

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
    def __init__(self, parent=None):
        super(ChangeStylePage, self).__init__(parent)

        self.setTitle("Customize the output table")
        self.setSubTitle("Select the color colors and fontstyles to be used "
                         "in the xls table")

        # Set up layout
        self.vbox = Qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def initializePage(self):
        # Set up layout
        vbox = Qtw.QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        # adding pattern selection part
        topLabel = Qtw.QLabel(self.tr("Click on a field to choose the style for "
                                      "this field"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        hbox = Qtw.QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)

        texts = ['Header', 'Standard\nRow 1', 'Standard\nRow 2',
                 'Marked \nRow 1',
                 'Marked \nRow 2', 'Default Value']
        default_styles = [
            'color: rgb(255,255,255); background-color: rgb(51,51,51); '
            'font:bold',
            'color: rgb(255,255,255); background-color: rgb(0,128,0)',
            'color: rgb(255,255,255); background-color: rgb(0,0,128)',
            'color: rgb(0,0,0); background-color: rgb(204,255,204)',
            'color: rgb(0,0,0); background-color: rgb(204,255,255)',
            'color: rgb(0,0,0); background-color: rgb(255,0,0)']
        common_default = "; padding-left: 5px; padding-right: 5px;" \
                         " padding-top: 5px; padding-bottom: 5px;" \
                         " border-color: rgb(255,0,0)"
        # ''padding: 6px'
        positions = [(0, 0, 1, 2), (1, 0), (2, 0), (1, 1), (2, 1), (3, 0, 1, 2)]

        self.tablebuttons = [None] * len(texts)

        gridtable = Qtw.QGridLayout()
        for i in list(range(len(self.tablebuttons))):
            self.tablebuttons[i] = Qtw.QPushButton()
            self.tablebuttons[i].setText(texts[i])
            self.tablebuttons[i].setStyleSheet(default_styles[i])
            self.tablebuttons[i].setStyleSheet(
                self.tablebuttons[i].styleSheet() + common_default)
            self.tablebuttons[i].setAutoFillBackground(True)
            self.tablebuttons[i].clicked.connect(self.updatesettings)
            gridtable.addWidget(self.tablebuttons[i], *positions[i])

        self.cbhighlightdefaults = Qtw.QCheckBox('Highlight default values')
        self.cbhighlightdefaults.setChecked(True)

        # add spacer for invisible 'default value' button
        self.spacer = Qtw.QSpacerItem(10, 0)

        gridtable.setSpacing(0)

        vstretcher = Qtw.QVBoxLayout()
        vstretcher.addStretch(1)
        vstretcher.addLayout(gridtable)
        vstretcher.addSpacerItem(self.spacer)
        vstretcher.addSpacing(10)
        vstretcher.addWidget(self.cbhighlightdefaults)
        vstretcher.addStretch(1)

        hbox.addLayout(vstretcher)

        # adding separator
        verticalLine = Qtw.QFrame()
        verticalLine.setFrameStyle(Qtw.QFrame.VLine)
        verticalLine.setSizePolicy(Qtw.QSizePolicy.Minimum, Qtw.QSizePolicy.Expanding)

        hbox.addWidget(verticalLine)

        self.cbbgcolor = ColorListWidget()
        self.cbfontcolor = ColorListWidget()

        self.cbboldfont = Qtw.QCheckBox('bold')
        self.cbboldfont.setStyleSheet('font:bold')

        self.cbitalicfont = Qtw.QCheckBox('italic')
        self.cbitalicfont.setStyleSheet('font:italic')

        gridsettings = Qtw.QGridLayout()
        self.settingstitle = Qtw.QLabel()
        self.settingstitle.setText('-')
        self.settingstitle.setStyleSheet('font:bold 16px')
        gridsettings.addWidget(self.settingstitle, 0, 0, 1, 1)
        gridsettings.addWidget(Qtw.QLabel('Backgroundcolor'), 1, 0)
        gridsettings.addWidget(self.cbbgcolor, 1, 1)
        gridsettings.addWidget(Qtw.QLabel('Fontcolor'), 2, 0)
        gridsettings.addWidget(self.cbfontcolor, 2, 1)
        gridsettings.addWidget(Qtw.QLabel('Fontstyle'), 3, 0)
        gridsettings.addWidget(self.cbboldfont, 3, 1)
        gridsettings.addWidget(self.cbitalicfont, 4, 1)
        gridsettings.setSpacing(0)
        gridsettings.setAlignment(Qt.AlignCenter)

        hbox.addLayout(gridsettings)
        vbox.addLayout(hbox)

        self.currentbutton = self.tablebuttons[0]

        for i in list(range(len(self.tablebuttons))):
            self.settings.register(texts[i], self.tablebuttons[i])

        self.cbitalicfont.toggled.connect(self.updatetable)
        self.cbboldfont.toggled.connect(self.updatetable)

        self.cbhighlightdefaults.toggled.connect(self.updatedefaultbutton)
        self.settings.register('CBhighlightdefaults', self.cbhighlightdefaults)

        self.cbbgcolor.currentIndexChanged.connect(self.updatetable)
        self.settings.register('CBbgcolor', self.cbbgcolor, useconfig=False)

        self.cbfontcolor.currentIndexChanged.connect(self.updatetable)
        self.settings.register('CBfontcolor', self.cbfontcolor, useconfig=False)

    def updatesettings(self):
        sender = self.sender()
        self.currentbutton = sender
        # show selected button
        sender.setStyleSheet(sender.styleSheet() + '; border: 2px solid red')
        # unselect other buttons
        for button in self.tablebuttons:
            if button != sender:
                button.setStyleSheet(self.removestyle(button.styleSheet(),
                                                      'border'))

        # update header of selection part (right part)
        self.settingstitle.setText(sender.text().replace('\n', ' '))
        # update backgroundcolor
        color = get_rgb(get_property(sender.styleSheet(), 'background-color'))
        index = self.cbbgcolor.xlwt_rgbcolors.index(color)
        if index >= 0:
            self.cbbgcolor.setCurrentIndex(index)
        else:
            pass
        # update fontcolor
        color = get_rgb(get_property(sender.styleSheet(), 'color'))
        index = self.cbfontcolor.xlwt_rgbcolors.index(color)
        if index >= 0:
            self.cbfontcolor.setCurrentIndex(index)
        else:
            pass
        # update font style
        font_style = get_property(sender.styleSheet(), 'font')
        if font_style == None: font_style = ''
        self.cbboldfont.setChecked('bold' in font_style)
        self.cbitalicfont.setChecked('italic' in font_style)

    def updatetable(self):
        sender = self.sender()
        # updates from comboboxes
        if sender in [self.cbbgcolor, self.cbfontcolor]:
            if sender == self.cbbgcolor:
                to_update = 'background-color'
                new_style_value = 'rgb%s;' % (
                    str(self.cbbgcolor.get_current_rgb()))
            elif sender == self.cbfontcolor:
                to_update = 'color'
                new_style_value = 'rgb%s;' % (
                    str(self.cbfontcolor.get_current_rgb()))
            self.currentbutton.setStyleSheet(
                self.removestyle(self.currentbutton.styleSheet(), to_update)
                + '; %s:%s' % (to_update, new_style_value))

        # updates from checkboxes
        elif sender in [self.cbboldfont, self.cbitalicfont]:
            new_style = self.currentbutton.styleSheet()
            if sender == self.cbboldfont:
                new_value = 'bold'
            elif sender == self.cbitalicfont:
                new_value = 'italic'
            new_style.replace(new_value, '')
            if sender.isChecked():
                if 'font:' in new_style:
                    new_style.replace('font:', 'font: %s ' % new_value)
                else:
                    new_style += '; font:%s' % new_value
            elif get_property(new_style, 'font').strip(' ') == '':
                new_style.replace('font:', '')

            self.currentbutton.setStyleSheet(new_style)

    def removestyle(self, style, property):
        styles = [str(s) for s in style.split(';')]
        s = 0
        while s < len(styles):
            if styles[s].strip(' ').startswith(property + ':'):
                styles.pop(s)
                styles = [s.strip(' ').rstrip(' ') for s in styles
                          if s.strip(' ') != '']
            else:
                s += 1
        return '; '.join(styles)

    def updatedefaultbutton(self):
        self.layout().activate()
        self.tablebuttons[5].setVisible(self.cbhighlightdefaults.isChecked())
        if self.cbhighlightdefaults.isChecked():
            height = 0
        else:
            height = self.tablebuttons[5].height()
        self.spacer.changeSize(self.tablebuttons[5].width(), height,
                               Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Fixed)
        self.layout().invalidate()


class SaveFilePage(QIWizardPage):
    def __init__(self, parent=None):
        super(SaveFilePage, self).__init__(parent)

        self.setTitle("Save the result")
        self.setSubTitle("Select a location to save your file. You can save the"
                         " settings made during this generation with a custom "
                         "configuration name. This configuration can be used "
                         "in future runs of the gui.")

        # Set up layout
        self.vbox = Qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_new_conf(self, configlist):
        item = Qtw.QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setText('<Click here enter a new configuration name>')
        configlist.insertItem(-1, item)

    def newconfname(self):
        sender = self.sender().currentItem()
        if sender.text() == '<Click here enter a new configuration name>':
            sender.setText('')

    def deleteconfname(self):
        if self.configlist.currentItem() == None:
            Qtw.QMessageBox.warning(self, 'No configuration selected',
                                    'You need to select a configuration in'
                                    ' order to delete it.')
        else:
            conf_name = str(self.configlist.currentItem().text())
            quit_msg = "Are you sure you want to delete the configuration " \
                       "'%s'?" % (conf_name)
            reply = Qtw.QMessageBox.question(self, 'Message',
                                             quit_msg, Qtw.QMessageBox.Yes,
                                             Qtw.QMessageBox.No)

            if reply == Qtw.QMessageBox.Yes:
                self.configlist.takeItem(self.configlist.currentRow())
                self.settings.delete_config(conf_name)
            else:
                pass

    def initializePage(self):

        # Set up layout
        vbox = Qtw.QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        # adding pattern selection part
        self.topLabel = Qtw.QLabel(self.tr("Where do you want to save your file?"))
        self.topLabel.setWordWrap(True)
        vbox.addWidget(self.topLabel)
        # vbox.addSpacing(40)

        # Add first horizontal box
        self.buttonbrowse = Qtw.QPushButton("Save file")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.buttonbrowse.setFocus()
        self.outputfilename = ''
        self.outputfile = Qtw.QLabel(self.outputfilename)
        self.outputfile.setWordWrap(True)
        self.buttonshow = Qtw.QPushButton("Open file")
        self.buttonshow.clicked.connect(self.show_file)
        self.buttonshow.setEnabled(False)
        self.buttonsaveconfig = Qtw.QPushButton("Save configuration")
        self.buttonsaveconfig.clicked.connect(self.saveconfig)
        self.buttondeleteconfig = Qtw.QPushButton("Delete configuration")
        self.buttondeleteconfig.clicked.connect(self.deleteconfname)

        hbox = Qtw.QHBoxLayout()
        hbox.addWidget(self.buttonbrowse)
        hbox.addWidget(self.outputfile)
        hbox.addStretch()

        vbox.addLayout(hbox)
        # vbox.addSpacing(10)
        vbox.addWidget(self.buttonshow)
        vbox.addStretch()

        # adding separator
        horizontalLine = Qtw.QFrame()
        horizontalLine.setFrameStyle(Qtw.QFrame.HLine)
        horizontalLine.setSizePolicy(Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)
        vbox.addWidget(Qtw.QLabel('You can save the configuration used in '
                                  'this run'))
        grid = Qtw.QGridLayout()
        self.configlist = Qtw.QListWidget()
        self.configlist.itemActivated.connect(self.newconfname)
        self.add_new_conf(self.configlist)
        grid.addWidget(self.configlist, 0, 0, 1, 2)
        grid.addWidget(self.buttonsaveconfig, 1, 0)
        grid.addWidget(self.buttondeleteconfig, 1, 1)
        vbox.addLayout(grid)

        self.settings.register('outputfilename', self, useconfig=False)
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        if self.settings.get_object('RBoutputxls').isChecked():
            self.expected_extensions = ['.xls']
        elif self.settings.get_object('RBoutputcsv').isChecked():
            self.expected_extensions = ['.csv']
        elif self.settings.get_object('RBoutputodml').isChecked():
            self.expected_extensions = ['.odml', '.xml']
        else:
            raise ValueError('Can not save file without selection of '
                             'output format.')

        self.topLabel.setText("Where do you want to save your %s file?"
                              % '/'.join([ext.strip('.') for ext in self.expected_extensions]))

        self.configlist.addItems(self.settings.get_all_config_names())
        self.issaved = False

    def handlebuttonbrowse(self):
        dlg = Qtw.QFileDialog()
        dlg.setFileMode(Qtw.QFileDialog.AnyFile)
        dlg.setAcceptMode(Qtw.QFileDialog.AcceptSave)
        dlg.setLabelText(Qtw.QFileDialog.Accept, "Generate File")
        dlg.setDefaultSuffix(self.expected_extensions[0].strip('.'))

        inputfilename = self.settings.get_object('inputfilename')
        dirname = os.path.dirname(inputfilename)
        suggested_filename = os.path.splitext(os.path.basename(
            inputfilename))[0] + self.expected_extensions[0]
        dlg.setDirectory(dirname)
        dlg.selectFile(suggested_filename)

        filternames = ["%s files (*%s)" % (ext.strip('.'), ext) for ext in
                       self.expected_extensions]
        filternames += ['all files (*)']
        dlg.setNameFilters(filternames)
        # filenames = []

        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])


            # extending filename if no extension is present
        if (self.outputfilename != '' and
                    os.path.splitext(self.outputfilename)[1] == ''):
            self.outputfilename += self.expected_extensions[0]
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        if ((os.path.splitext(self.outputfilename)[
                 1] not in self.expected_extensions) and
                (os.path.splitext(self.outputfilename)[1] != '')):
            Qtw.QMessageBox.warning(self, 'Wrong file format',
                                    'The output file format is supposed to be "%s",'
                                    ' but you selected "%s"'
                                    '' % (' or '.join(self.expected_extension),
                                          os.path.splitext(self.outputfilename)[1]))
            self.handlebuttonbrowse()

        elif self.outputfilename != '':
            self.issaved = True
            convert(self.settings)

            print('Complete!')

            self.buttonshow.setEnabled(True)

    def show_file(self):
        platform = sys.platform
        if platform.startswith('linux'):
            subprocess.Popen(["nohup", "see", self.outputfilename])
        elif platform == 'darwin':
            subprocess.Popen(["open", self.outputfilename])
        elif platform.startswith('win'):
            subprocess.Popen(["start", self.outputfilename])
        else:
            raise ValueError('Unknown operating platform "{}".'.format(platform))

    def saveconfig(self):
        if ((self.configlist.currentItem() == None) or
                (str(self.configlist.currentItem().text()) in
                     ['', '<Click here enter a new configuration name>'])):
            Qtw.QMessageBox.warning(self, 'No configuration name selected',
                                    'You need to select a name for your '
                                    'configuration if you want to save it or '
                                    'define a new one (<Click here enter a new '
                                    'configuration name>)')
        else:
            config_name = str(self.configlist.currentItem().text())
            curritem = self.configlist.currentItem()
            if self.configlist.currentRow() != 0:
                self.configlist.item(0).setText(
                    '<Click here enter a new configuration name>')
            elif config_name in self.settings.get_all_config_names():
                Qtw.QMessageBox.warning(self, 'Configuration already exists',
                                        'You need to chose a new name for your '
                                        'configuration.'
                                        'The name "%s" already exists' %
                                        config_name)
            else:
                curritem.setFlags((Qt.ItemIsSelectable | Qt.ItemIsEnabled))
                self.add_new_conf(self.configlist)
            self.settings.config_name = config_name
            self.settings.save_config()

    def validatePage(self):
        if self.issaved == False:
            quit_msg = "Are you sure you want to exit the program without " \
                       "saving your file?"
            reply = Qtw.QMessageBox.question(self, 'Message',
                                             quit_msg, Qtw.QMessageBox.Yes, Qtw.QMessageBox.No)
            if reply == Qtw.QMessageBox.No:
                return 0
        return 1


class ColorListWidget(Qtw.QComboBox):
    _xlwt_rgbcolors = [
        (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (0, 0, 0), (255, 255, 255), (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0),
        (0, 128, 0),
        (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
        (192, 192, 192),
        (128, 128, 128), (153, 153, 255), (153, 51, 102), (255, 255, 204),
        (204, 255, 255), (102, 0, 102), (255, 128, 128), (0, 102, 204),
        (204, 204, 255),
        (0, 0, 128), (255, 0, 255), (255, 255, 0), (0, 255, 255), (128, 0, 128),
        (128, 0, 0), (0, 128, 128), (0, 0, 255), (0, 204, 255), (204, 255, 255),
        (204, 255, 204), (255, 255, 153), (153, 204, 255), (255, 153, 204),
        (204, 153, 255), (255, 204, 153), (51, 102, 255), (51, 204, 204),
        (153, 204, 0),
        (255, 204, 0), (255, 153, 0), (255, 102, 0), (102, 102, 153),
        (150, 150, 150),
        (0, 51, 102), (51, 153, 102), (0, 51, 0), (51, 51, 0), (153, 51, 0),
        (153, 51, 102),
        (51, 51, 153), (51, 51, 51)
    ]

    def __init__(self):
        super(ColorListWidget, self).__init__()
        cmap = xlwt.Style.colour_map
        self.xlwt_colornames = []
        self.xlwt_color_index = []
        self.xlwt_rgbcolors = []
        # self._xlwt_colorlabels = []
        for i in list(range(64)):
            cnames = [name for (name, index) in list(cmap.items()) if index == i]

            # self._xlwt_colorlabels.append(cnames[0] if len(cnames)>0 else '')
            if cnames != []:
                self.xlwt_colornames.append(', '.join(cnames))
                self.xlwt_color_index.append(i)
                self.xlwt_rgbcolors.append(self._xlwt_rgbcolors[i])

        for i, xlwtcolor in enumerate(self.xlwt_colornames):
            self.insertItem(i, xlwtcolor)
            self.setItemData(i, Qtg.QColor(*self.xlwt_rgbcolors[i]),
                             Qt.DecorationRole)

    def get_current_rgb(self):
        return self.xlwt_rgbcolors[self.currentIndex()]


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
                         '' % os.path.splitext(settings.get_object(
            'outputfilename'))[1])

    # setting xls_table or csv_table headers if necessary
    title_translator = {v: k for k, v in iteritems(table._header_titles)}
    if ((os.path.splitext(settings.get_object('inputfilename'))[1]
         in ['.xls', '.csv']) and
            (settings.get_object('CBcustominput').isChecked())):
        inputheaderlabels = [str(l.text()) for l in settings.get_object('headerlabels')]
        inputcustomheaders = [str(cb.currentText()) for cb in settings.get_object('customheaders')]
        inputcolumnnames = [title_translator[label] for label in inputcustomheaders]
        table.change_header_titles(**dict(zip(inputcolumnnames,
                                              inputheaderlabels)))

    # loading input file
    if os.path.splitext(settings.get_object('inputfilename'))[1] == '.xls':
        table.load_from_xls_table(settings.get_object('inputfilename'))
    elif os.path.splitext(settings.get_object('inputfilename'))[1] == '.csv':
        table.load_from_csv_table(settings.get_object('inputfilename'))
    elif os.path.splitext(settings.get_object('inputfilename'))[1] in ['.odml', '.xml']:
        table.load_from_file(settings.get_object('inputfilename'))
    else:
        raise ValueError('Unknown input file extension "%s"'
                         '' % os.path.splitext(settings.get_object('inputfilename'))[1])

    # setting custom header selection and custom header titles if necessary
    if (os.path.splitext(settings.get_object('outputfilename'))[1] in ['.xls', '.csv']):

        # setting custom header columns
        output_headers = [title_translator[str(settings.get_object(
            'LWselectedcolumns').item(index).text())] for index in
                          list(range(settings.get_object(
                              'LWselectedcolumns').count()))]
        table.change_header(**dict(zip(output_headers,
                                       list(range(1, len(output_headers) + 1)))))

        # setting custom header labels
        # if settings.get_object('CBcustomheader').isChecked():
        customoutputlabels = [str(le.text())
                              for le in
                              settings.get_object('customheaderlabels')]
        table.change_header_titles(
            **dict(zip(output_headers, customoutputlabels)))

        # adding extra layout specifications to xls output files
        if os.path.splitext(settings.get_object('outputfilename'))[1] == '.xls':
            # marking columns
            marked_columns = [cb.isChecked()
                              for cb in settings.get_object('columnmarkings')]
            if any(marked_columns):
                table.mark_columns(*[h for i, h in enumerate(output_headers)
                                     if marked_columns[i]])

            # setting color pattern and changing point
            if settings.get_object('RBalternating').isChecked():
                table.pattern = 'alternating'
            elif settings.get_object('RBcheckerboard').isChecked():
                table.pattern = 'checkerboard'

            if settings.get_object('RBnopattern').isChecked():
                table.changing_point = None
            elif settings.get_object('RBsection').isChecked():
                table.changing_point = "sections"
            elif settings.get_object('RBproperty').isChecked():
                table.changing_point = "properties"
            elif settings.get_object('RBvalue').isChecked():
                table.changing_point = "values"

            style_names = ['header_style', 'first_style', 'second_style',
                           'first_marked_style', 'second_marked_style',
                           'highlight_style']
            style_labels = ['Header', 'Standard\nRow 1', 'Standard\nRow 2',
                            'Marked \nRow 1', 'Marked \nRow 2', 'Default Value']
            style_buttons = [settings.get_object(style_label)
                             for style_label in style_labels]

            for i, style_name in enumerate(style_names):
                style_button = style_buttons[i]

                # get background color
                rgb_tuple = get_rgb(get_property(style_button.styleSheet(),
                                                 'background-color'))
                index = settings.get_object(
                    'CBbgcolor').xlwt_rgbcolors.index(rgb_tuple)
                bgcolor = settings.get_object('CBbgcolor').xlwt_colornames[
                    index].split(',')[0]

                # get font color
                rgb_tuple = get_rgb(get_property(style_button.styleSheet(),
                                                 'color'))
                index = settings.get_object(
                    'CBfontcolor').xlwt_rgbcolors.index(rgb_tuple)
                fontcolor = settings.get_object(
                    'CBfontcolor').xlwt_colornames[index].split(',')[0]

                # get font properties
                font_properties = ''
                font_string = get_property(style_button.styleSheet(), 'font')
                if 'bold' in font_string:
                    font_properties += 'bold 1'
                if 'italic' in font_string:
                    if font_properties != '':
                        font_properties += ', '
                    font_properties += 'italic 1'

                # construct style
                style = xls_style.XlsStyle(backcolor=bgcolor,
                                           fontcolor=fontcolor,
                                           fontstyle=font_properties)
                setattr(table, style_name, style)

            # setting highlight defaults
            table.highlight_defaults = settings.get_object(
                'CBhighlightdefaults').isChecked()

    # saving file
    if os.path.splitext(settings.get_object('outputfilename'))[1] in ['.xls', '.csv']:
        table.write2file(settings.get_object('outputfilename'))
    elif os.path.splitext(settings.get_object('outputfilename'))[1] in ['.odml', '.xml']:
        table.write2odml(settings.get_object('outputfilename'))
