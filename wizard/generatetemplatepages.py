# -*- coding: utf-8 -*-

import subprocess
import datetime

from PyQt4.QtGui import *

from pageutils import *

from  odmltables import odml_table, odml_xls_table, odml_csv_table, xls_style
import odml


mandatory_headers = ['Path to Section',
                        'Property Name',
                        'Value',
                        'odML Data Type']

class HeaderOrderPage(QIWizardPage):
    def __init__(self,parent=None):
        super(HeaderOrderPage, self).__init__(parent)

        self.setTitle("Customize the output table")
        self.setSubTitle("Select the columns for the output table by putting them in the list of selected columns and arranging the order using the buttons to the right")

        # Set up layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        hbox0 = QHBoxLayout()
        hbox0.addStretch()
        hbox0.addWidget(QLabel('available columns'))
        hbox0.addStretch()
        hbox0.addSpacing(90)
        hbox0.addWidget(QLabel('selected columns'))
        hbox0.addStretch()
        hbox0.addSpacing(30)

        vbox.addLayout(hbox0)

        # Adding input part
        odtables = odml_table.OdmlTable()
        self.header_names = odtables._header_titles.values()

        # generating selection lists
        self.header_list = QListWidget()
        self.header_list.setSelectionMode(3)
        self.selection_list = QListWidget()
        self.selection_list.setSelectionMode(3)


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

        default_selection_list = ['Path to Section',
                                  'Property Name',
                                  'Value',
                                  'Data Uncertainty',
                                  'Data Unit',
                                  'odML Data Type',
                                  'Value Definition',
                                  'Property Definition',
                                  'Section Definition']
        self.mandatory_headers = mandatory_headers
        for i,h in enumerate(self.header_names):
            if h not in default_selection_list:
                item = QListWidgetItem()
                item.setText(h)
                self.header_list.addItem(item)

        for i,h in enumerate(default_selection_list):
            item = QListWidgetItem()
            item.setText(h)
            self.selection_list.addItem(item)

            if h in self.mandatory_headers:
                item.setTextColor(QColor('red'))


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


    def initializePage(self):
        # Set up layout

        self.settings.register('LWselectedcolumns',self.selection_list)
        self.settings.register('LWnonselectedcolumns',self.header_list)


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
            if self.selection_list.item(row).text() in self.mandatory_headers:
                QMessageBox.warning(self, self.tr("Mandatory header"),
                                self.tr("'%s' is a mandatory header. This header is necessary to "
                                        "be able to convert the table into an odml."%self.selection_list.item(row).text()))
            else:
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



class SaveFilePage(QIWizardPage):
    def __init__(self,parent=None):
        super(SaveFilePage, self).__init__(parent)

        # Set up layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.setTitle("Save the result")
        self.setSubTitle("Select a location to save your file")

    def add_new_conf(self,configlist):
        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setText('<New Configuration>')
        configlist.insertItem(-1,item)

    def newconfname(self):
        sender = self.sender().currentItem()
        if sender.text() == '<New Configuration>':
            sender.setText('')

    def deleteconfname(self):
        if self.configlist.currentItem() == None:
            QMessageBox.warning(self,'No configuration selected','You need to select a configuration in'
                                                                 ' order to delete it.')
        else:
            conf_name = str(self.configlist.currentItem().text())
            quit_msg = "Are you sure you want to delete the configuration '%s'?"%(conf_name)
            reply = QMessageBox.question(self, 'Message',
                             quit_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.configlist.takeItem(self.configlist.currentRow())
                self.settings.delete_config(conf_name)
            else:
                pass


    def initializePage(self):

        self.expected_extension = '.xls'

        # Set up layout
        vbox = QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        vbox.addSpacing(40)

        # Add first horizontal box
        self.buttonbrowse = QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.buttonbrowse.setFocus()
        self.outputfilename = ''
        self.outputfile = QLabel(self.outputfilename)
        self.outputfile.setWordWrap(True)
        self.buttonshow = QPushButton("Open file")
        self.buttonshow.clicked.connect(self.show_file)
        self.buttonshow.setEnabled(False)

        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonbrowse)
        hbox.addWidget(self.outputfile)
        hbox.addStretch()


        vbox.addLayout(hbox)
        vbox.addSpacing(30)
        vbox.addWidget(self.buttonshow)
        vbox.addStretch()


        self.outputfilename = ''
        self.settings.register('outputfilename', self,useconfig=False)
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)




    def handlebuttonbrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setLabelText (QFileDialog.Accept, "Generate File" )
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))

        # dlg.setDirectory(self.settings.get_object('inputfilename'))

        dlg.setFilter("%s files (*%s);;all files (*)"%(self.expected_extension.strip('.'),self.expected_extension))

        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])


        print self.outputfilename

        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)


        if ((os.path.splitext(self.outputfilename)[1]!=self.expected_extension) and
                  (os.path.splitext(self.outputfilename)[1]!='')):
            QMessageBox.warning(self,'Wrong file format','The output file format is supposed to be "%s",'
                                                         ' but you selected "%s"'
                                                         ''%(self.expected_extension,
                                                             os.path.splitext(self.outputfilename)[1]))
            self.handlebuttonbrowse()

        elif self.outputfilename != '':
            createfile(self.settings)

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


def createfile(settings):
    odmldoc = setup_tutorodml()
    table = odml_xls_table.OdmlXlsTable()
    table.load_from_odmldoc(odmldoc)
    table.changing_point = None

    title_translator = {v:k for k,v in table._header_titles.iteritems()}
    mandatory_titles = [title_translator[m] for m in mandatory_headers]

    # setting custom header columns
    output_headers = [title_translator[str(settings.get_object('LWselectedcolumns').item(index).text())]
                      for index in range(settings.get_object('LWselectedcolumns').count())]
    table.change_header(**dict(zip(output_headers,range(1,len(output_headers)+1))))
    table.mark_columns(*[h for i,h in enumerate(output_headers) if h in mandatory_titles])

    # saving file
    table.write2file(settings.get_object('outputfilename'))


def setup_tutorodml():
    doc = odml.Document(version='0.0.x')
    doc.author = 'FirstName LastName'
    doc.date = datetime.date.today()
    doc.version = '0.0.x'
    doc.repository = '/myserver/myrepo'

    # APPEND MAIN SECTIONS
    doc.append(odml.Section(name='MySection1',type='sectiontype0', definition = 'This is my first section describing the first very important part of my experiment (eg. the experimental setup / hardware)'))
    doc.append(odml.Section(name='MySection2',type='sectiontype1', definition = 'This is my second section describing the second very important part of my experiment (eg. the subject performing the experiment)'))

    parent = doc['MySection1']
    parent.append(odml.Section('MySubsection1',type='sectiontype0', definition = 'This section contains information about a subpart of my experiment (eg. everything concerning the amplifier used...)'))
    parent.append(odml.Section('MySubsection2',type='sectiontype0', definition = 'This section contains information about another subpart of my experiment (eg. everything concerning the sensor used...)'))

    parent = doc['MySection2']
    parent.append(odml.Section('MySubsection3',type='sectiontype2', definition = 'This section contains information about yet another subpart of my experiment (eg. the history of the subject)'))


    # ADDING PROPERTIES
    parent = doc['MySection1']
    parent.append(odml.Property(name='SetupID', value=odml.Value('supersetup2016',dtype='str',unit='',uncertainty='',definition='ID of the setup used for this experiment'), definition = 'ID of the setup used for this experiment'))
    parent.append(odml.Property(name='SetupName', value=odml.Value('mysetup',dtype='str',unit='',uncertainty='',definition='Human readable setup name'), definition = 'Human readable setup name'))
    parent.append(odml.Property(name='SetupLocation', value=odml.Value('mylab, room 007',dtype='str',unit='',uncertainty='',definition='Location of the setup'), definition = 'Location of the setup'))

    parent = doc['MySection1']['MySubsection1']
    parent.append(odml.Property(name='HardwareID', value=odml.Value('superamplifier3000',dtype='str',unit='',uncertainty='',definition='ID of the amplifier used for this experiment'), definition = 'ID of the amplifier used for this experiment'))
    parent.append(odml.Property(name='AcquisitionDate', value=odml.Value(datetime.date(2000,01,01),dtype='date',unit='',uncertainty='1 week',definition='Recipience date of the hardware component'), definition = 'Purchase date of the hardware component'))
    parent.append(odml.Property(name='AmplificationFactor', value=[odml.Value(5,dtype='int',unit='V/V',uncertainty=0.01,definition='Signal amplification during calibration'),
                                                                    odml.Value(50,dtype='int',unit='V/V',uncertainty=0.01,definition='Signal amplification during main measurement')],
                                definition = 'Signal amplification factor used during the experiment'))

    parent = doc['MySection1']['MySubsection2']
    parent.append(odml.Property(name='HardwareID', value=odml.Value('supersensor5000',dtype='str',unit='',uncertainty='',definition='ID of the sensor used for this experiment'), definition = 'ID of the sensor used for this experiment'))
    parent.append(odml.Property(name='InstallationDate', value=odml.Value(datetime.date(2015,01,01),dtype='date',unit='',uncertainty='1 day',definition='Date of the initial start-up of the hardware component'), definition = 'Installation date of the hardware component'))
    parent.append(odml.Property(name='Sensitivity', value=odml.Value(10,dtype='float',unit='mV/N',uncertainty=0.001,definition='Sensitivity of the hardware component'),definition = 'Sensitivity of the hardware component'))
    parent.append(odml.Property(name='Range', value=[odml.Value(0.1,dtype='float',unit='N',uncertainty=0.05,definition='Lower measurement limit'),
                                                     odml.Value(10000,dtype='float',unit='N',uncertainty=100,definition='Upper measurement limit')],
                                definition = 'Active measurement range of the hardware component'))

    parent = doc['MySection2']
    parent.append(odml.Property(name='SubjectID', value=odml.Value('s1357',dtype='str',unit='',uncertainty='',definition='PassportID'), definition = 'ID of the subject taking part in the experiment'))
    parent.append(odml.Property(name='SubjectName', value=odml.Value('Sam Subject',dtype='str',unit='',uncertainty='',definition='First and last name of the subject'), definition = 'Name of the subject'))
    parent.append(odml.Property(name='Birthdate', value=odml.Value(datetime.date(1910,01,01),dtype='date',unit='',uncertainty='',definition='Birthdate'), definition = 'Birthdate of the subject'))

    parent = doc['MySection2']['MySubsection3']
    parent.append(odml.Property(name='Diseases', value=[odml.Value('Smallpox',dtype='str',unit='',uncertainty='',definition='Disease'),
                                                        odml.Value('Plague',dtype='str',unit='',uncertainty='',definition='Disease'),
                                                        odml.Value('Cholera',dtype='str',unit='',uncertainty='',definition='Disease')],
                                definition = 'Past diseases of the subject'))
    parent.append(odml.Property(name='BiologicalAge', value=odml.Value(50,dtype='int',unit='years',uncertainty=5,definition='Age'), definition = 'Tested biological age of the subject'))

    return doc

