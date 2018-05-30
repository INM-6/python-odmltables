# -*- coding: utf-8 -*-

import sys
import os
import subprocess

import PyQt5.QtGui as Qtg
import PyQt5.QtWidgets as Qtw
from PyQt5.QtCore import QSize, Qt

from odmltables import odml_table, odml_xls_table, odml_csv_table, xls_style
from .pageutils import QIWizardPage, shorten_path
from .wizutils import get_graphic_path


class LoadFilePage(QIWizardPage):
    def __init__(self, parent=None, filenames=None):
        super(LoadFilePage, self).__init__(parent)

        self.inputfilename1 = ''
        self.inputfilename2 = ''
        if filenames:
            if len(filenames) > 0:
                self.inputfilename1 = filenames[0]
            if len(filenames) > 1:
                self.inputfilename2 = filenames[1]

        graphic_path = get_graphic_path()

        # Set up layout
        self.layout = Qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.setTitle("Select an input file")
        self.setSubTitle("Select the files you want to merge and specify the"
                         " merge mode and location to save your file ")

        vbox = self.layout

        # setting inputfile variables
        self.settings.register('inputfilename1', self, useconfig=False)
        self.settings.register('inputfilename2', self, useconfig=False)

        # Adding primary input part
        topLabel = Qtw.QLabel(self.tr("Choose two odml files to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)

        # Add first horizontal box
        self.buttonbrowse1 = self.generate_toolbutton("Browse for basic\nodml"
                                                      "file", 'odmlA.svg')
        self.buttonbrowse1.clicked.connect(self.browse2open, 1)
        self.inputfile1 = Qtw.QLabel(self.inputfilename1)
        self.inputfile1.setWordWrap(True)
        hbox1 = Qtw.QHBoxLayout()
        hbox1.addWidget(self.buttonbrowse1)
        hbox1.addWidget(self.inputfile1)

        hbox1.addStretch()
        vbox.addLayout(hbox1)

        # Adding secondary input part
        # topLabel = QLabel(self.tr("Choose an additional odML file to load"))
        # topLabel.setWordWrap(True)
        # vbox.addWidget(topLabel)

        # Add second horizontal box
        self.buttonbrowse2 = self.generate_toolbutton("Browse for second,\n"
                                                      "extending file",
                                                      'odmlB.svg')
        self.buttonbrowse2.clicked.connect(self.browse2open, 2)
        self.inputfile2 = Qtw.QLabel(self.inputfilename2)
        self.inputfile2.setWordWrap(True)
        hbox2 = Qtw.QHBoxLayout()
        hbox2.addWidget(self.buttonbrowse2)
        hbox2.addWidget(self.inputfile2)
        hbox2.addStretch()
        vbox.addLayout(hbox2)

        vbox.addStretch()

        # adding first separator
        horizontalLine = Qtw.QFrame()
        horizontalLine.setFrameStyle(Qtw.QFrame.HLine)
        horizontalLine.setSizePolicy(Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)

        # adding merge mode part
        vbox.addWidget(Qtw.QLabel('Select a mode for merging the two files'))
        self.rbstrict = Qtw.QRadioButton('strict merge')
        self.rbstrict.setIcon(Qtg.QIcon(os.path.join(graphic_path,'mergestrict.svg')))
        self.rbstrict.setIconSize(QSize(100, 100))
        self.rbappend = Qtw.QRadioButton('append')
        self.rbappend.setIcon(Qtg.QIcon(os.path.join(graphic_path,'mergeappend.svg')))
        self.rbappend.setIconSize(QSize(100, 100))

        self.settings.register('rbstrict', self.rbstrict)
        self.settings.register('rbappend', self.rbappend)

        self.rbstrict.setChecked(True)

        hbox3 = Qtw.QHBoxLayout()
        hbox3.addWidget(self.rbstrict)

        hbox3.addSpacing(20)
        hbox3.addWidget(self.rbappend)
        vbox.addLayout(hbox3)

        # adding second separator
        horizontalLine = Qtw.QFrame()
        horizontalLine.setFrameStyle(Qtw.QFrame.HLine)
        horizontalLine.setSizePolicy(Qtw.QSizePolicy.Expanding, Qtw.QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)

        # adding save part
        self.topLabel = Qtw.QLabel(self.tr("Where do you want to save your file?"))
        self.topLabel.setWordWrap(True)
        vbox.addWidget(self.topLabel)

        self.buttonbrowsesave = Qtw.QPushButton("Browse")
        self.buttonbrowsesave.clicked.connect(self.browse2save)
        self.buttonbrowsesave.setEnabled(False)
        self.outputfilename = ''
        self.settings.register('outputfilename', self)
        self.outputfile = Qtw.QLabel(self.outputfilename)
        self.outputfile.setWordWrap(True)
        self.buttonshow = Qtw.QPushButton("Open file")
        self.buttonshow.clicked.connect(self.show_file)
        self.buttonshow.setEnabled(False)

        hbox = Qtw.QHBoxLayout()
        hbox.addWidget(self.buttonbrowsesave)
        hbox.addWidget(self.outputfile)
        hbox.addStretch()

        vbox.addLayout(hbox)
        # vbox.addSpacing(10)
        vbox.addWidget(self.buttonshow)
        vbox.addStretch()

        self.issaved = False

    def generate_toolbutton(self, text, graphic_name):
        graphic_path = get_graphic_path()
        button = Qtw.QToolButton()
        button.setText(self.tr(text))
        button.setIcon(Qtg.QIcon(os.path.join(graphic_path, graphic_name)))
        button.setIconSize(QSize(60, 60))
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.setFixedWidth(200)

        return button

    def browse2open(self):
        sender = self.sender()
        if sender == self.buttonbrowse1:
            input_id = 1
        elif sender == self.buttonbrowse2:
            input_id = 2
        else:
            raise ValueError('Wrong browser.')

        self.expected_extension = '.odml'

        dlg = Qtw.QFileDialog()
        dlg.setFileMode(Qtw.QFileDialog.AnyFile)
        dlg.setAcceptMode(Qtw.QFileDialog.AcceptOpen)
        dlg.setLabelText(Qtw.QFileDialog.Accept, "Open")
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))

        dir = None
        if self.settings.get_object('inputfilename1'):
            dir = self.settings.get_object('inputfilename1')
        elif self.settings.get_object('inputfilename2'):
            dir = self.settings.get_object('inputfilename2')
        if dir:
            dlg.setDirectory(os.path.dirname(dir))

        if dlg.exec_():
            inputname = str(dlg.selectedFiles()[0])
            if ((os.path.splitext(inputname)[1] != self.expected_extension) and
                    (os.path.splitext(inputname)[1] != '')):
                Qtw.QMessageBox.warning(self, 'Wrong file format',
                                        'The input file format is supposed to be "%s",'
                                        ' but you selected "%s"'
                                        '' % (self.expected_extension,
                                              os.path.splitext(inputname)[1]))
            else:
                setattr(self, 'inputfilename%i' % input_id, inputname)


        self.settings.register('inputfilename%i' % input_id, self, useconfig=False)
        short_filename = shorten_path(getattr(self, 'inputfilename%i' % input_id))
        getattr(self, 'inputfile%i' % input_id).setText(short_filename)

        if self.inputfile1 and self.inputfilename2:
            self.buttonbrowsesave.setEnabled(True)

    def browse2save(self):
        # check generation prerequisites
        if (not self.inputfilename1) or (not self.inputfilename2):
            Qtw.QMessageBox.warning(self, 'Not enough input files provided',
                                    'You need to provide two inputfiles to be '
                                    'merged')
            return
        elif ((not self.rbstrict.isChecked()) and
                  (not self.rbappend.isChecked())):
            Qtw.QMessageBox.warning(self, 'No merge mode selected',
                                    'You need to select one of the two merge '
                                    'modes: "strict merge" or "append merge".')
            return

        self.expected_extension = '.odml'

        dlg = Qtw.QFileDialog()
        dlg.setFileMode(Qtw.QFileDialog.AnyFile)
        dlg.setAcceptMode(Qtw.QFileDialog.AcceptSave)
        dlg.setLabelText(Qtw.QFileDialog.Accept, "Generate File")
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))
        dlg.setDirectory(os.path.dirname(self.settings.get_object('inputfilename1')))

        dlg.setNameFilters(["%s files (*%s);;all files (*)"
                      "" % (self.expected_extension.strip('.'),
                            self.expected_extension)])

        self.outputfilename = ''
        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])

        if not self.outputfilename:
            Qtw.QMessageBox.warning(self, 'No output file selected',
                                    'You need to select an output odml file to '
                                    'save your data.')
            return

        # # extending filename if no extension is present
        # if (self.outputfilename != '' and
        #             os.path.splitext(self.outputfilename)[1]==''):
        #     self.outputfilename += self.expected_extension
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        if ((os.path.splitext(self.outputfilename)[
                 1] != self.expected_extension) and
                (os.path.splitext(self.outputfilename)[1] != '')):
            Qtw.QMessageBox.warning(self, 'Wrong file format',
                                    'The output file format is supposed to be "%s",'
                                    ' but you selected "%s"'
                                    '' % (self.expected_extension,
                                          os.path.splitext(self.outputfilename)[1]))
            self.handlebuttonbrowse()

        elif self.outputfilename != '':
            success = self.convert(self.settings)

            if success:
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

    def convert(self, settings):

        # generate odmltables objects
        table1 = odml_table.OdmlTable()
        table2 = odml_table.OdmlTable()

        # loading input files
        table1.load_from_file(settings.get_object('inputfilename1'))
        table2.load_from_file(settings.get_object('inputfilename2'))

        # extracting merge mode from selections
        mode = None
        if settings.get_object('rbstrict').isChecked():
            mode = 'strict'
        elif settings.get_object('rbappend').isChecked():
            mode = 'append'

        # merging inputfiles
        try:
            table1.merge(table2, mode=mode)
        except ValueError as e:
            message = e.message if hasattr(e, 'message') else (str(e))
            Qtw.QMessageBox.warning(self, 'Error while merging files',
                                    'Value error: %s. Can not merge into non-default values in '
                                    'merge mode "strict". Data could be lost in the process. '
                                    'Please fix your odml files or change to merge mode "append".'
                                    '' % (message))
            return False
        except:
            Qtw.QMessageBox.warning(self, 'Unexpected error:', sys.exc_info()[0])
            return False

        # saving file
        table1.write2odml(settings.get_object('outputfilename'))
        return True
