# -*- coding: utf-8 -*-

import datetime
import sys
import os
import subprocess

from future.utils import iteritems

import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg
from PyQt5.QtCore import Qt

import odml
from odmltables import odml_table, odml_xls_table, odml_csv_table, xls_style
from .pageutils import QIWizardPage, clearLayout, shorten_path

mandatory_headers = ['Path to Section',
                     'Property Name',
                     'Value',
                     'odML Data Type']


class HeaderOrderPage(QIWizardPage):
    def __init__(self, parent=None):
        super(HeaderOrderPage, self).__init__(parent)

        self.setTitle("Customize the output table")
        self.setSubTitle(
            "Select the columns for the output table by putting them in "
            "the "
            "list of selected columns and arranging the order using the "
            "buttons to the right")

        # Set up layout
        vbox = Qtw.QVBoxLayout()
        self.setLayout(vbox)

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
                                  'Data Uncertainty',
                                  'Data Unit',
                                  'odML Data Type',
                                  'Property Definition',
                                  'Section Definition']
        self.mandatory_headers = mandatory_headers
        for i, h in enumerate(self.header_names):
            if h not in default_selection_list:
                item = Qtw.QListWidgetItem()
                item.setText(h)
                self.header_list.addItem(item)

        for i, h in enumerate(default_selection_list):
            item = Qtw.QListWidgetItem()
            item.setText(h)
            self.selection_list.addItem(item)

            if h in self.mandatory_headers:
                item.setForeground(Qtg.QColor('red'))

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
        # sort rows in descending order in order to compensate shifting due
        # to takeItem
        rows = sorted(
            [index.row() for index in self.header_list.selectedIndexes()],
            reverse=True)
        for row in rows:
            self.selection_list.addItem(self.header_list.takeItem(row))

    def toleft(self):
        # sort rows in descending order in order to compensate shifting due
        # to takeItem
        rows = sorted([index.row() for index in
                       self.selection_list.selectedIndexes()],
                      reverse=True)
        for row in rows:
            if self.selection_list.item(row).text() in self.mandatory_headers:
                Qtw.QMessageBox.warning(self, self.tr("Mandatory header"),
                                        self.tr(
                                            "'%s' is a mandatory header. This "
                                            "header is necessary to "
                                            "be able to convert the table "
                                            "into an "
                                            "odml." % self.selection_list.item(
                                                row).text()))
            else:
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
        for itemid in list(range(
                self.settings.get_object('LWselectedcolumns').count())):
            selectedheaderstrings.append(
                self.settings.get_object('LWselectedcolumns').item(
                    itemid).text())

        missing_headers = []
        for mand_header in self.mandatory_headers:
            if mand_header not in selectedheaderstrings:
                missing_headers.append(mand_header)

        if missing_headers != []:
            Qtw.QMessageBox.warning(self, self.tr("Incomplete odml"),
                                    self.tr("You need to include the headers %s "
                                            " in your table if you want to be "
                                            "able to"
                                            " generate an odml from the table." % (
                                                missing_headers)))

        return 1


class SaveFilePage(QIWizardPage):
    def __init__(self, parent=None):
        super(SaveFilePage, self).__init__(parent)

        # Set up layout
        self.vbox = Qtw.QVBoxLayout()
        self.setLayout(self.vbox)

        self.setTitle("Save the result")
        self.setSubTitle("Select a location to save your file")

    def add_new_conf(self, configlist):
        item = Qtw.QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setText('<New Configuration>')
        configlist.insertItem(-1, item)

    def newconfname(self):
        sender = self.sender().currentItem()
        if sender.text() == '<New Configuration>':
            sender.setText('')

    def deleteconfname(self):
        if self.configlist.currentItem() == None:
            Qtw.QMessageBox.warning(self, 'No configuration selected',
                                    'You need to select a configuration in'
                                    ' order to delete it.')
        else:
            conf_name = str(self.configlist.currentItem().text())
            quit_msg = "Are you sure you want to delete the configuration " \
                       "'%s'?" % (
                           conf_name)
            reply = Qtw.QMessageBox.question(self, 'Message',
                                             quit_msg, Qtw.QMessageBox.Yes,
                                             Qtw.QMessageBox.No)

            if reply == Qtw.QMessageBox.Yes:
                self.configlist.takeItem(self.configlist.currentRow())
                self.settings.delete_config(conf_name)
            else:
                pass

    def initializePage(self):

        self.expected_extension = '.xls'

        # Set up layout
        vbox = Qtw.QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        vbox.addSpacing(40)

        # Add first horizontal box
        self.buttonbrowse = Qtw.QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.buttonbrowse.setFocus()
        self.outputfilename = ''
        self.outputfile = Qtw.QLabel(self.outputfilename)
        self.outputfile.setWordWrap(True)
        self.buttonshow = Qtw.QPushButton("Open file")
        self.buttonshow.clicked.connect(self.show_file)
        self.buttonshow.setEnabled(False)

        hbox = Qtw.QHBoxLayout()
        hbox.addWidget(self.buttonbrowse)
        hbox.addWidget(self.outputfile)
        hbox.addStretch()

        vbox.addLayout(hbox)
        vbox.addSpacing(30)
        vbox.addWidget(self.buttonshow)
        vbox.addStretch()

        self.outputfilename = ''
        self.settings.register('outputfilename', self, useconfig=False)
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        self.issaved = False

    def handlebuttonbrowse(self):
        dlg = Qtw.QFileDialog()
        dlg.setFileMode(Qtw.QFileDialog.AnyFile)
        dlg.setAcceptMode(Qtw.QFileDialog.AcceptSave)
        dlg.setLabelText(Qtw.QFileDialog.Accept, "Generate File")
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))

        suggested_filename = 'template' + self.expected_extension
        dlg.selectFile(suggested_filename)

        filternames = ["%s files (*%s)" % (ext.strip('.'), ext) for ext in
                       [self.expected_extension]]
        filternames += ["all files (*)"]
        dlg.setNameFilters(filternames)

        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])

        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        if ((os.path.splitext(self.outputfilename)[1] != self.expected_extension) and
                (os.path.splitext(self.outputfilename)[1] != '')):
            Qtw.QMessageBox.warning(self, 'Wrong file format',
                                    'The output file format is supposed to be "%s",'
                                    ' but you selected "%s"'
                                    '' % (self.expected_extension,
                                          os.path.splitext(self.outputfilename)[1]))
            self.handlebuttonbrowse()

        elif self.outputfilename != '':
            createfile(self.settings)
            self.issaved = True

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

    def validatePage(self):
        if self.issaved == False:
            quit_msg = "Are you sure you want to exit the program without " \
                       "saving your file?"
            reply = Qtw.QMessageBox.question(self, 'Message',
                                             quit_msg, Qtw.QMessageBox.Yes, Qtw.QMessageBox.No)
            if reply == Qtw.QMessageBox.No:
                return 0
        return 1


def createfile(settings):
    odmldoc = setup_tutorodml()
    table = odml_xls_table.OdmlXlsTable()
    table.load_from_odmldoc(odmldoc)
    table.changing_point = None
    table.show_all_sections = False
    table.show_all_properties = False

    title_translator = {v: k for k, v in iteritems(table._header_titles)}
    # mandatory_titles = [title_translator[m] for m in mandatory_headers]

    # setting custom header columns
    output_headers = [title_translator[str(
        settings.get_object('LWselectedcolumns').item(index).text())]
                      for index in
                      list(range(settings.get_object('LWselectedcolumns').count()))]
    table.change_header(
        **dict(zip(output_headers, list(range(1, len(output_headers) + 1)))))
    # table.mark_columns(
    #         *[h for i, h in enumerate(output_headers) if h in mandatory_titles])

    # set all styles to plan black and white
    styles = ['first_style', 'second_style', 'first_marked_style',
              'second_marked_style', 'highlight_style']

    for style in styles:
        setattr(getattr(table, style), 'backcolor', 'white')
        setattr(getattr(table, style), 'fontcolor', 'black')

    table.highlight_defaults = True

    # saving file
    table.write2file(settings.get_object('outputfilename'))


def setup_tutorodml():
    doc = odml.Document(version='0.0.x')
    doc.author = 'FirstName LastName'
    doc.date = datetime.date.today()
    doc.version = '0.0.x'
    doc.repository = '/myserver/myrepo'

    # APPEND MAIN SECTIONS
    doc.append(odml.Section(name='MySection',
                            type='<Enter the type of data this section is'
                                 ' associated with, e.g. hardware>',
                            definition='<Describe the purpose of sections '
                                       'in short statements in this '
                                       'column.>'))
    doc.append(odml.Section(name='OneMoreSection',
                            type='<Enter the type of data this section is'
                                 ' associated with, e.g. software>',
                            definition='<Use only the first cell in this '
                                       'column to for the section '
                                       'description.>'))

    parent = doc['OneMoreSection']
    parent.append(odml.Section('MySubsection',
                               type='<Enter the type of data this section'
                                    ' is associated with, e.g. settings>',
                               definition='<Describe the purpose of this '
                                          'section here (eg. everything '
                                          'concerning the amplifier '
                                          'used...)'))

    # ADDING PROPERTIES
    parent = doc['MySection']
    parent.append(odml.Property(name='MyFirstProperty',
                                values='MyFirstValue',
                                dtype='str',
                                unit=None,
                                uncertainty=None,
                                definition='<Enter a short definition of '
                                           'the property and the associated '
                                           'value described here>'))
    parent.append(odml.Property(name='MultiValuedProperty',
                                values=[2.001, 4],
                                dtype='float',
                                unit='mm',
                                uncertainty=0.02,
                                definition='A section can have multiple properties attached and '
                                           'a property can contain multiple values.'))

    parent = doc['OneMoreSection']
    parent.append(odml.Property(name='MyEmptyProperty',
                                values=None,
                                dtype='int',
                                unit='mV',
                                uncertainty=None,
                                definition='This property contains an empty value.'
                                           'Empty values can be highlighted using odmltables.'))

    parent = doc['OneMoreSection']['MySubsection']
    parent.append(odml.Property(name='MyLastProperty',
                                values=datetime.datetime.today().date(),
                                dtype='date',
                                unit='AD',
                                uncertainty=None,
                                definition='You can define the hierarchical'
                                           ' location of a section via the'
                                           ' "path to section" column.'
                                           'The value contains todays date.'))
    return doc
