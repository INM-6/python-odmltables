# -*- coding: utf-8 -*-


import sys
import os
import subprocess

from PyQt4.QtGui import *
from PyQt4.QtCore import QSize

from pageutils import *
from wizutils import get_graphic_path

from  odmltables import odml_table, odml_xls_table, odml_csv_table, \
    xls_style


class LoadFilePage(QIWizardPage):
    def __init__(self, parent=None):
        super(LoadFilePage, self).__init__(parent)

        graphic_path = get_graphic_path()

        # Set up layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setTitle("Select an input file")
        self.setSubTitle("Select the files you want to merge and specify the"
                         " merge mode and location to save your file ")

        vbox = self.layout

        # setting inputfile variables
        self.inputfilename1 = ''
        self.inputfilename2 = ''
        self.settings.register('inputfilename1', self, useconfig=False)
        self.settings.register('inputfilename2', self, useconfig=False)

        # Adding primary input part
        topLabel = QLabel(self.tr("Choose two odml files to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)

        # Add first horizontal box
        self.buttonbrowse1 = self.generate_toolbutton("Browse for basic\nodml"
                                                      "file", 'odmlA.svg')
        self.buttonbrowse1.clicked.connect(self.browse2open, 1)
        self.inputfilename1 = ''
        self.inputfile1 = QLabel(self.inputfilename1)
        self.inputfile1.setWordWrap(True)
        hbox1 = QHBoxLayout()
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
        self.inputfilename2 = ''
        self.inputfile2 = QLabel(self.inputfilename2)
        self.inputfile2.setWordWrap(True)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.buttonbrowse2)
        hbox2.addWidget(self.inputfile2)
        hbox2.addStretch()
        vbox.addLayout(hbox2)

        vbox.addStretch()

        # adding first separator
        horizontalLine = QFrame()
        horizontalLine.setFrameStyle(QFrame.HLine)
        horizontalLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)

        # adding merge mode part
        vbox.addWidget(QLabel('Select a mode for merging the two files'))
        self.rbstrict = QRadioButton('strict merge')
        self.rbstrict.setIcon(QIcon(os.path.join(graphic_path,
                                                 'mergestrict.svg')))
        self.rbstrict.setIconSize(QSize(100, 100))
        self.rboverwrite = QRadioButton('overwrite')
        self.rboverwrite.setIcon(QIcon(os.path.join(graphic_path,
                                                    'mergeoverwrite.svg')))
        self.rboverwrite.setIconSize(QSize(100, 100))

        self.settings.register('rbstrict', self.rbstrict)
        self.settings.register('rboverwrite', self.rboverwrite)

        self.rbstrict.setChecked(True)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.rbstrict)

        hbox3.addSpacing(20)
        hbox3.addWidget(self.rboverwrite)
        vbox.addLayout(hbox3)

        # adding second separator
        horizontalLine = QFrame()
        horizontalLine.setFrameStyle(QFrame.HLine)
        horizontalLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)

        # adding save part
        self.topLabel = QLabel(self.tr("Where do you want to save your file?"))
        self.topLabel.setWordWrap(True)
        vbox.addWidget(self.topLabel)

        self.buttonbrowsesave = QPushButton("Browse")
        self.buttonbrowsesave.clicked.connect(self.browse2save)
        self.buttonbrowsesave.setEnabled(False)
        self.outputfilename = ''
        self.settings.register('outputfilename', self)
        self.outputfile = QLabel(self.outputfilename)
        self.outputfile.setWordWrap(True)
        self.buttonshow = QPushButton("Open file")
        self.buttonshow.clicked.connect(self.show_file)
        self.buttonshow.setEnabled(False)

        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonbrowsesave)
        hbox.addWidget(self.outputfile)
        hbox.addStretch()

        vbox.addLayout(hbox)
        # vbox.addSpacing(10)
        vbox.addWidget(self.buttonshow)
        vbox.addStretch()

    def generate_toolbutton(self, text, graphic_name):
        graphic_path = get_graphic_path()
        button = QToolButton()
        button.setText(self.tr(text))
        button.setIcon(QIcon(os.path.join(graphic_path, graphic_name)))
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

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setLabelText(QFileDialog.Accept, "Open")
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))

        dir = None
        if self.settings.get_object('inputfilename1'):
            dir = self.settings.get_object('inputfilename1')
        elif self.settings.get_object('inputfilename2'):
            dir = self.settings.get_object('inputfilename2')

        if dir:
            dlg.setDirectory(dir)

        dlg.setFilter("%s files (*%s);;all files (*)"
                      "" % (self.expected_extension.strip('.'),
                            self.expected_extension))

        inputname = ''
        if dlg.exec_():
            inputname = str(dlg.selectedFiles()[0])
            setattr(self, 'inputfilename%i' % input_id, inputname)

        self.settings.register('inputfilename%i' % input_id, self,
                               useconfig=False)
        short_filename = shorten_path(inputname)
        getattr(self, 'inputfile%i' % input_id).setText(short_filename)

        if self.inputfile1 and self.inputfilename2:
            self.buttonbrowsesave.setEnabled(True)

    def browse2save(self):
        # check generation prerequisites
        if (not self.inputfilename1) or (not self.inputfilename2):
            QMessageBox.warning(self, 'Not enough input files provided',
                                'You need to provide two inputfiles to be '
                                'merged')
            return
        elif ((not self.rbstrict.isChecked()) and
                  (not self.rboverwrite.isChecked())):
            QMessageBox.warning(self, 'No merge mode selected',
                                'You need to select one of the two merge '
                                'modes: "strict merge" or "overwrite merge".')
            return

        self.expected_extension = '.odml'

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setLabelText(QFileDialog.Accept, "Generate File")
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))
        dlg.setDirectory(self.settings.get_object('inputfilename1'))

        dlg.setFilter("%s files (*%s);;all files (*)"
                      "" % (self.expected_extension.strip('.'),
                            self.expected_extension))

        self.outputfilename = ''
        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])

        if not self.outputfilename:
            QMessageBox.warning(self, 'No output file selected',
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
            QMessageBox.warning(self, 'Wrong file format',
                                'The output file format is supposed to be "%s",'
                                ' but you selected "%s"'
                                '' % (self.expected_extension,
                                      os.path.splitext(self.outputfilename)[1]))
            self.handlebuttonbrowse()

        elif self.outputfilename != '':
            success = self.convert(self.settings)

            if success:
                print 'Complete!'
                self.buttonshow.setEnabled(True)

    def show_file(self):
        system = os.name
        if system == 'posix':
            subprocess.Popen(["nohup", "see", self.outputfilename])
            # os.system('see %s'%self.outputfilename)
        elif system == 'nt':
            subprocess.Popen(["start", self.outputfilename])
            # os.system("start %s"%self.outputfilename)

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
        elif settings.get_object('rboverwrite').isChecked():
            mode = 'overwrite'

        # merging inputfiles
        try:
            table1.merge(table2, mode=mode)
        except ValueError as e:
            QMessageBox.warning(self, 'Error while merging files',
                                'Value error: %s. Can not merge into '
                                'non-default values in merge mode "strict". '
                                'Data '
                                'could be lost in the process. Please fix '
                                'your odml '
                                'files or change to merge mode "overwrite".' % (
                                    e.message))
            return False
        except:
            QMessageBox.warning(self, 'Unexpected error:', sys.exc_info()[0])
            return False

        # saving file
        table1.write2odml(settings.get_object('outputfilename'))
