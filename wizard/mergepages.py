# -*- coding: utf-8 -*-


import copy
import subprocess

from PyQt4.QtGui import *

from pageutils import *

from  odmltables import odml_table, odml_xls_table, odml_csv_table, \
    xls_style


class LoadFilePage(QIWizardPage):
    def __init__(self,parent=None):
        super(LoadFilePage,self).__init__(parent)

        # Set up layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def initializePage(self):

        self.setTitle("Select an input file")
        self.setSubTitle("Select the files you want to merge and specify the"
                         " merge settings")

        vbox = self.layout

        # Adding prime input part
        topLabel = QLabel(self.tr("Choose a primary odML file to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        # vbox.addSpacing(10)

        # Add first horizontal box
        self.buttonbrowse1 = QPushButton("Browse")
        self.buttonbrowse1.clicked.connect(self.handlebuttonbrowse)
        self.inputfilename1 = ''
        self.inputfile1 = QLabel(self.inputfilename1)
        self.inputfile1.setWordWrap(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.buttonbrowse1)
        hbox1.addWidget(self.inputfile1)

        hbox1.addStretch()
        vbox.addLayout(hbox1)

        # Adding secondary input part
        topLabel = QLabel(self.tr("Choose a secondary odML file to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        # vbox.addSpacing(10)

        # Add first horizontal box
        self.buttonbrowse2 = QPushButton("Browse")
        self.buttonbrowse2.clicked.connect(self.handlebuttonbrowse)
        self.inputfilename2 = ''
        self.inputfile2 = QLabel(self.inputfilename2)
        self.inputfile2.setWordWrap(True)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.buttonbrowse2)
        hbox2.addWidget(self.inputfile2)

        hbox2.addStretch()
        vbox.addLayout(hbox2)

        # self.cbcustominput = QCheckBox('I changed the column names in the'
        #                                ' input table.')
        # self.cbcustominput.setEnabled(False)
        # self.settings.register('CBcustominput',self.cbcustominput)
        # vbox.addWidget(self.cbcustominput)
        vbox.addStretch()

        #adding separator
        horizontalLine = QFrame()
        horizontalLine.setFrameStyle(QFrame.HLine)
        horizontalLine.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)





    def selectconfig(self):
        if self.configselection.currentIndex() != 0:
            self.settings.load_config(str(self.configselection.currentText()))

            # loading output format choice
            self.settings.register('RBoutputxls',self.rbuttonxls)
            self.settings.register('RBoutputcsv',self.rbuttoncsv)
            self.settings.register('RBoutputodml', self.rbuttonodml)
            self.settings.register('CBcustominput',self.cbcustominput)
            self.settings.register('inputfilename', self,useconfig=False)
            short_filename = shorten_path(self.settings.get_object(
                                                            'inputfilename'))
            self.inputfile.setText(short_filename)
            # self.settings.get_object('RBoutputxls')


    def handlebuttonbrowse(self):
        self.inputfilename = str(QFileDialog().getOpenFileName())

        self.settings.register('inputfilename', self,useconfig=False)
        short_filename = shorten_path(self.inputfilename)
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
            QMessageBox.warning(self,'Select a format','You need to select a '
                                                       'table format to '
                                                       'continue.')
            return 0

        if ((not self.settings.is_registered('inputfilename')) or
            (not self.settings.get_object('inputfilename'))):
            QMessageBox.warning(self,'Select an input file','You need to select'
                                                            ' an input file to '
                                                            'continue.')
            return 0

        elif self.settings.get_object('inputfilename').split('.')[-1] not in \
                ['xls', 'csv', 'odml']:
            QMessageBox.warning(self,'Wrong input format','The input file has '
                                                          'to be an ".xls", '
                                                          '".csv" or ".odml" '
                                                          'file.')
            return 0

        return 1



    def nextId(self):

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








class SaveFilePage(QIWizardPage):
    def __init__(self,parent=None):
        super(SaveFilePage, self).__init__(parent)

        self.setTitle("Save the result")
        self.setSubTitle("Select a location to save your file. You can save the"
                         " settings made during this generation with a custom "
                         "configuration name. This configuration can be used "
                         "in future runs of the wizard.")

        # Set up layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

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
            QMessageBox.warning(self,'No configuration selected',
                                'You need to select a configuration in'
                                ' order to delete it.')
        else:
            conf_name = str(self.configlist.currentItem().text())
            quit_msg = "Are you sure you want to delete the configuration " \
                       "'%s'?"%(conf_name)
            reply = QMessageBox.question(self, 'Message',
                             quit_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.configlist.takeItem(self.configlist.currentRow())
                self.settings.delete_config(conf_name)
            else:
                pass

    def initializePage(self):

        # Set up layout
        vbox = QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)

        # adding pattern selection part
        self.topLabel = QLabel(self.tr("Where do you want to save your file?"))
        self.topLabel.setWordWrap(True)
        vbox.addWidget(self.topLabel)
        # vbox.addSpacing(40)

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
        self.buttonsaveconfig = QPushButton("Save configuration")
        self.buttonsaveconfig.clicked.connect(self.saveconfig)
        self.buttondeleteconfig = QPushButton("Delete configuration")
        self.buttondeleteconfig.clicked.connect(self.deleteconfname)

        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonbrowse)
        hbox.addWidget(self.outputfile)
        hbox.addStretch()

        vbox.addLayout(hbox)
        # vbox.addSpacing(10)
        vbox.addWidget(self.buttonshow)
        vbox.addStretch()

        # adding separator
        horizontalLine = QFrame()
        horizontalLine.setFrameStyle(QFrame.HLine)
        horizontalLine.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        vbox.addWidget(horizontalLine)
        vbox.addWidget(QLabel('You can save the configuration used in '
                              'this run'))
        grid = QGridLayout()
        self.configlist = QListWidget()
        self.configlist.itemActivated.connect(self.newconfname)
        self.add_new_conf(self.configlist)
        grid.addWidget(self.configlist,0,0,1,2)
        grid.addWidget(self.buttonsaveconfig,1,0)
        grid.addWidget(self.buttondeleteconfig,1,1)
        vbox.addLayout(grid)

        self.outputfilename = ''
        self.settings.register('outputfilename', self,useconfig=False)
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        if self.settings.get_object('RBoutputxls').isChecked():
            self.expected_extension = '.xls'
        elif self.settings.get_object('RBoutputcsv').isChecked():
            self.expected_extension = '.csv'
        elif self.settings.get_object('RBoutputodml').isChecked():
            self.expected_extension = '.odml'
        else:
            raise ValueError('Can not save file without selection of '
                             'output format.')

        self.topLabel.setText("Where do you want to save your "
                              "%s file?"%self.expected_extension.strip('.'))

        self.configlist.addItems(self.settings.get_all_config_names())


    def handlebuttonbrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setLabelText (QFileDialog.Accept, "Generate File" )
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))

        print self.settings.get_object('inputfilename')
        dlg.setDirectory(self.settings.get_object('inputfilename'))

        dlg.setFilter("%s files (*%s);;all files (*)"
                      ""%(self.expected_extension.strip('.'),
                          self.expected_extension))
        # filenames = []

        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])


         # extending filename if no extension is present
        if (self.outputfilename != '' and
                    os.path.splitext(self.outputfilename)[1]==''):
            self.outputfilename += self.expected_extension
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)


        if ((os.path.splitext(self.outputfilename)[1]!=self.expected_extension) and
                  (os.path.splitext(self.outputfilename)[1]!='')):
            QMessageBox.warning(self,'Wrong file format',
                                'The output file format is supposed to be "%s",'
                                 ' but you selected "%s"'
                                 ''%(self.expected_extension,
                                     os.path.splitext(self.outputfilename)[1]))
            self.handlebuttonbrowse()

        elif self.outputfilename != '':
            convert(self.settings)

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

    def saveconfig(self):
        if ((self.configlist.currentItem() == None) or
                (str(self.configlist.currentItem().text()) in
                     ['','<New Configuration>'])):
            QMessageBox.warning(self,'No configuration name selected',
                                'You need to select a name for your '
                                'configuration if you want to save it or '
                                'define a new one (<New Configuration>)')
        else:
            config_name = str(self.configlist.currentItem().text())
            curritem = self.configlist.currentItem()
            if self.configlist.currentRow() != 0:
                self.configlist.item(0).setText('<New Configuration>')
            elif config_name in self.settings.get_all_config_names():
                QMessageBox.warning(self,'Configuration already exists',
                        'You need to chose a new name for your configuration.'
                        'The name "%s" already exists'%config_name)
            else:
                curritem.setFlags(( Qt.ItemIsSelectable |  Qt.ItemIsEnabled ))
                self.add_new_conf(self.configlist)
            self.settings.config_name = config_name
            self.settings.save_config()


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
            self.setItemData(i, QColor(*self.xlwt_rgbcolors[i]),
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
                         ''%os.path.splitext(settings.get_object(
                                                        'outputfilename'))[1])

    # setting xls_table or csv_table headers if necessary
    title_translator = {v:k for k,v in table._header_titles.iteritems()}
    if ((os.path.splitext(settings.get_object('inputfilename'))[1]
         in ['.xls','.csv']) and
            (settings.get_object('CBcustominput').isChecked())):
        inputheaderlabels = [str(l.text())
                             for l in settings.get_object('headerlabels')]
        inputcustomheaders = [str(cb.currentText())
                              for cb in settings.get_object('customheaders')]
        inputcolumnnames = [title_translator[label]
                            for label in inputcustomheaders]
        table.change_header_titles(**dict(zip(inputcolumnnames,
                                              inputheaderlabels)))

    # loading input file
    if os.path.splitext(settings.get_object('inputfilename'))[1] == '.xls':
        table.load_from_xls_table(settings.get_object('inputfilename'))
    elif os.path.splitext(settings.get_object('inputfilename'))[1] == '.csv':
        table.load_from_csv_table(settings.get_object('inputfilename'))
    elif os.path.splitext(settings.get_object('inputfilename'))[1] == '.odml':
        table.load_from_file(settings.get_object('inputfilename'))
    else:
        raise ValueError('Unknown input file extension "%s"'
                         ''%os.path.splitext(settings.get_object(
                                                        'inputfilename'))[1])


    # setting custom header selection and custom header titles if necessary
    if (os.path.splitext(settings.get_object('outputfilename'))[1]
                                                            in ['.xls','.csv']):

        # setting custom header columns
        output_headers = [title_translator[str(settings.get_object(
                'LWselectedcolumns').item(index).text())] for index in
                        range(settings.get_object(
                                   'LWselectedcolumns').count())]
        table.change_header(**dict(zip(output_headers,
                                       range(1,len(output_headers)+1))))

        # setting custom header labels
        # if settings.get_object('CBcustomheader').isChecked():
        customoutputlabels = [str(le.text())
                            for le in settings.get_object('customheaderlabels')]
        table.change_header_titles(**dict(zip(output_headers,customoutputlabels)))

        # adding extra layout specifications to xls output files
        if os.path.splitext(settings.get_object('outputfilename'))[1] == '.xls':
            # marking columns
            marked_columns = [cb.isChecked()
                              for cb in settings.get_object('columnmarkings')]
            if any(marked_columns):
                table.mark_columns(*[h for i,h in enumerate(output_headers)
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

            style_names = ['header_style','first_style','second_style',
                           'first_marked_style','second_marked_style',
                           'highlight_style']
            style_labels = ['Header','Standard\nRow 1', 'Standard\nRow 2',
                            'Marked \nRow 1','Marked \nRow 2','Default Value']
            style_buttons = [settings.get_object(style_label)
                             for style_label in style_labels]

            for i,style_name in enumerate(style_names):
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
                font_string = get_property(style_button.styleSheet(),'font')
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
                setattr(table,style_name,style)


            # setting highlight defaults
            table.highlight_defaults = settings.get_object(
                     'CBhighlightdefaults').isChecked()

    # saving file
    if os.path.splitext(settings.get_object('outputfilename'))[1] in [
         '.xls','.csv']:
        table.write2file(settings.get_object('outputfilename'))
    elif os.path.splitext(settings.get_object('outputfilename'))[1] == '.odml':
        table.write2odml(settings.get_object('outputfilename'))