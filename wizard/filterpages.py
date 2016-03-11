# -*- coding: utf-8 -*-

import subprocess
import copy

from PyQt4.QtGui import *

from pageutils import *

from  odmltables import odml_table, odml_xls_table, odml_csv_table, xls_style


class LoadFilePage(QIWizardPage):
    def __init__(self,parent=None):
        super(LoadFilePage,self).__init__(parent)

        # Set up layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def initializePage(self):

        self.setTitle("Select an input file")
        self.setSubTitle("Select the file you want to filter")

        vbox = self.layout

        # Adding input part
        topLabel = QLabel(self.tr("Choose a file to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)

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

        # adding configuration selection
        configlabel = QLabel('Load a configuration from a previous run')
        vbox.addWidget(configlabel)
        self.configselection = QComboBox()
        self.configselection.addItems(self.settings.get_all_config_names())
        self.configselection.insertItem(0,'-- No configuration --')
        self.configselection.setCurrentIndex(0)
        self.configselection.activated.connect(self.selectconfig)
        vbox.addWidget(self.configselection)

        vbox.addStretch()



    def selectconfig(self):
        if self.configselection.currentIndex() != 0:
            self.settings.load_config(str(self.configselection.currentText()))

            # loading output format choice
            self.settings.register('CBcustominput',self.cbcustominput)
            self.settings.register('inputfilename', self,useconfig=False)
            short_filename = shorten_path(self.settings.get_object('inputfilename'))
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


    def validatePage(self):

        if (not self.settings.is_registered('inputfilename')) or (not self.settings.get_object('inputfilename')):
            QMessageBox.warning(self,'Select an input file','You need to select an input file to continue.')
            return 0

        elif self.settings.get_object('inputfilename').split('.')[-1] not in ['xls', 'csv', 'odml']:
            QMessageBox.warning(self,'Wrong input format','The input file has to be an ".xls", ".csv" or ".odml" file.')
            return 0

        return 1


    def nextId(self):
        if ((self.inputfilename[-5:] != '.odml') and
                (self.settings.get_object('CBcustominput').isChecked())):
            return self.wizard().PageCustomInputHeader

        else:
            return self.wizard().PageFilter



class CustomInputHeaderPage(QIWizardPage):
    def __init__(self,parent=None):
        super(CustomInputHeaderPage, self).__init__(parent)

        self.setTitle("Provide information about your input file")
        self.setSubTitle("Which titles were used for which odml column in you input file. Select the corresponding odml columns.")

        # Set up layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        # self.vbox = QVBoxLayout()
        # self.layout.addLayout(self.vbox)

    def initializePage(self):

        # Set up layout
        vbox = QVBoxLayout()
        clearLayout(self.layout())
        self.layout().addLayout(vbox)


        # Adding input part
        topLabel = QLabel(self.tr("Provide the column types used in the input table"))
        topLabel.setWordWrap(True)
        vbox.addSpacing(20)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        self.grid = QGridLayout()
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
        header_names = odtables._header_titles.values()

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

    def nextId(self):
        return self.wizard().PageFilter



class FilterPage(QIWizardPage):
    def __init__(self,parent=None):
        super(FilterPage, self).__init__(parent)

        self.odmltreeheaders = ['Content',
                                'Value','DataUncertainty','DataUnit','odmlDatatype','ValueDefinition',
                                'PropertyName','PropertyDefinition',
                                'SectionName','SectionType','SectionDefinition']

        self.setTitle("Filter your data")
        self.setSubTitle("Create your filters and apply them to the odml-tables structure.")

        self.filters = {}

        # filtersettingsframe = QFrame()
        # hbox = QHBoxLayout()
        # hbox.addWidget(filtersettingsframe)
        # self.setLayout(hbox)

        hbox = QVBoxLayout(self)

        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        left.setMinimumHeight(450)
        left.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.vboxleft = QVBoxLayout()
        left.setLayout(self.vboxleft)

        leftbottom = QFrame(self)
        leftbottom.setFrameShape(QFrame.StyledPanel)
        self.vboxleftbottom = QVBoxLayout()
        leftbottom.setLayout(self.vboxleftbottom)
        leftbottom.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)
        vboxright = QVBoxLayout()
        right.setLayout(vboxright)

        self.filtersettingsgrid = QGridLayout()
        self.filtersettingsgrid.addWidget(QLabel('mode'),0,0)
        self.filtersettingsgrid.addWidget(QLabel('invert'),1,0)
        self.filtersettingsgrid.addWidget(QLabel('recursive'),2,0)
        self.compfunclabel = QLabel(self.tr('comparison\nfunction'))
        self.filtersettingsgrid.addWidget(self.compfunclabel,3,0)

        self.rbAND = QRadioButton(self.tr('&& [AND]'))
        self.rbOR = QRadioButton('| [OR]')
        self.rbAND.setChecked(True)
        self.filtersettingsgrid.addWidget(self.rbAND,0,1)
        self.filtersettingsgrid.addWidget(self.rbOR,0,2)

        self.cbinvert = QCheckBox()
        self.filtersettingsgrid.addWidget(self.cbinvert,1,1)

        self.cbrecursive = QCheckBox()
        self.filtersettingsgrid.addWidget(self.cbrecursive,2,1)

        self.lwcomparisonfunc = QListWidget()
        self.lwcomparisonfunc.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.filtersettingsgrid.addWidget(self.lwcomparisonfunc,3,1,1,2)

#       ########### KEY-Value Part ##################
        self.keygrid = QGridLayout()
        self.keygrid.addWidget(QLabel('key'),0,0)
        self.keygrid.addWidget(QLabel('value'),0,1)

        # self.cbkeys = QComboBox()
        # self.cbvalue = QLineEdit()

        ###############################
        filtercreatorlabel = QLabel('Filter Creator')
        filtercreatorlabel.setStyleSheet('font: bold; font-size: 14pt')
        self.vboxleft.addWidget(filtercreatorlabel)
        self.vboxleft.addLayout(self.filtersettingsgrid)
        self.vboxleft.addStretch()
        # self.vboxleft.addWidget(QPushButton('test'))
        # self.vboxleft.addLayout(self.keygrid)
        self.filtersettingsgrid.addLayout(self.keygrid,4,0,1,3,)

        self.pbaddkey = QPushButton('+')
        self.pbremovekey = QPushButton('-')
        self.pbaddkey.clicked.connect(self._add_key_value_pair)
        self.pbremovekey.clicked.connect(self._remove_key_value_pair)
        self.pbaddkeylayout = QHBoxLayout()
        self.pbaddkeylayout.addStretch()
        self.pbaddkeylayout.addWidget(self.pbaddkey)
        self.pbaddkeylayout.addWidget(self.pbremovekey)
        self.pbaddkeylayout.addStretch()
        self.vboxleft.addLayout(self.pbaddkeylayout)
        self.vboxleft.addStretch()

        self.pbaddfilter = QPushButton('Add filter')
        self.pbaddfilter.clicked.connect(self.addfilter)
        self.vboxleft.addWidget(self.pbaddfilter)

        filterlabel = QLabel('Applied filters')
        filterlabel.setStyleSheet('font: bold; font-size: 14pt')
        self.vboxleftbottom.addWidget(filterlabel)

        self.lwfilters = QListWidget()
        self.lwfilters.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.vboxleftbottom.addWidget(self.lwfilters)

        self.pbremovefilter = QPushButton('Remove filter')
        self.pbremovefilter.clicked.connect(self.removefilter)
        self.vboxleftbottom.addWidget(self.pbremovefilter)

        ###################################
        self.odmltree = QTreeWidget()
        self.odmltree.setColumnCount(2)
        self.odmltree.setHeaderLabels(self.odmltreeheaders)
        self.odmltree.setSelectionMode(3)
        self.odmltree.setMinimumWidth(500)
        self.odmltree.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        columnwidths = [50]*len(self.odmltreeheaders)
        columnwidths[0:3] = [250,100,100]
        [self.odmltree.setColumnWidth(i,w) for i,w in enumerate(columnwidths)]



        vboxright.addWidget(self.odmltree)

        splitterv = QSplitter(Qt.Vertical)
        splitterv.addWidget(left)
        splitterv.addWidget(leftbottom)

        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitterv)
        splitter2.addWidget(right)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)


    def initializePage(self):
        self._add_key_value_pair()

        comparison_functions = {'==\t[x==y]': lambda x,y:x==y,
                                'endswith\t[hasattr(x,"endswith") and x.endswith(y)]': lambda x,y: hasattr(x,'endswith') and x.endswith(y),
                                'startswith\t[hasattr(x,"startswith") and x.startswith(y)]': lambda x,y: hasattr(x,'startswith') and x.startswith(y),
                                'is in list\t[x in y]': lambda  x,y: x in y,
                                'contains\t[type(x)==str and y in x]': lambda  x,y: type(x)==str and y in x}
        for cf_name in comparison_functions:
            self.lwcomparisonfunc.addItems([cf_name])
        self._add_custom_item_to_list(self.lwcomparisonfunc)
        # self.lwcomparisonfunc.item(0).setSelected(True)
        self.lwcomparisonfunc.setCurrentRow(0)
        self.lwcomparisonfunc.setFixedHeight(self.lwcomparisonfunc.sizeHintForRow(0) * (self.lwcomparisonfunc.count() +1) + 2 * self.lwcomparisonfunc.frameWidth())
        self.lwcomparisonfunc.setMinimumHeight(self.lwcomparisonfunc.sizeHintForRow(0) * (self.lwcomparisonfunc.count() +1) + 2 * self.lwcomparisonfunc.frameWidth())
        self.compfunclabel.setMinimumHeight(self.lwcomparisonfunc.sizeHintForRow(0) * (self.lwcomparisonfunc.count() +1) + 2 * self.lwcomparisonfunc.frameWidth())
        self.layout().invalidate()
        self.lwcomparisonfunc.itemChanged.connect(self.new_comparison_func)

        self.load_odml()

        self.odmltree.expandToDepth(0)


# def filter(self,mode='and',invert=False,recursive=False,comparison_func=lambda x,y: x==y,**kwargs):
        """
        filters odml properties according to provided kwargs.

        :param mode: Possible values: 'and', 'or'. For 'and' all keyword arguments
                must be satisfied for a property to be selected. For 'or' only one
                of the keyword arguments must be satisfied for the property to be
                selected. Default: 'and'
        :param invert: Inverts filter function. Previously accepted properties
                are rejected and the other way round. Default: False
        :param recursive: Delete also properties attached to subsections of the
                mother section and therefore complete branch
        :param comparison_func: Function used to compare dictionary entry to
               keyword. Eg. 'lambda x,y: x.startswith(y)' in case of strings or
               'lambda x,y: x in y' in case of multiple permitted values.
               Default: lambda x,y: x==y
        :param kwargs: keywords and values used for filtering
        :return: None
        """

    def _add_custom_item_to_list(self,list):
        item = QListWidgetItem('add custom function\t[f(x,y)]')
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        list.addItem(item)

    def new_comparison_func(self,item):
        # item = self.sender().currentItem()
        if str(item.text()) != 'add custom function\t[f(x,y)]':
            if '[' in item.text() and ']' in item.text():
                if item.flags() & Qt.ItemIsEditable:
                    # item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self._add_custom_item_to_list(self.sender())
            else:
                QMessageBox.warning(self,'No function defined','You need to define your comparison function within brakets [].')

    def _add_key_value_pair(self):
        all_keys =self.odmltreeheaders[1:]
        n_keys = self._get_number_of_keys()

        if n_keys >= len(all_keys):
            return

        keycb = QComboBox()
        keycb.addItems(all_keys)
        # for id in range(keycb.count()):
        #     if id in [self.keygrid.itemAtPosition(i,0).widget().currentIndex() for i in range(1,self._get_number_of_keys())]:
        #         keycb.model().item(id).setEnabled(False)
        #     else:
        #         keycb.model().item(id).setEnabled(True)
        valueedit = QLineEdit()
        keycb.setMinimumSize(keycb.sizeHint())
        valueedit.setMinimumSize(keycb.sizeHint())
        self.keygrid.addWidget(keycb,n_keys,0)
        self.keygrid.addWidget(valueedit,n_keys,1)
        # self.update_enabled_keys(combobox=keycb)
        keycb.currentIndexChanged.connect(self.update_enabled_keys)

        for i in [self.keygrid.itemAtPosition(w,0).widget().currentIndex() for w in range(1,self._get_number_of_keys()-1)]:
            keycb.model().item(i).setEnabled(False)

        # setting current index to first enabled one
        for i in range(keycb.count()):
            if keycb.model().item(i).isEnabled():
                keycb.setCurrentIndex(i)
                break

        # setting current index to first enabled one
        # for i in range(len(all_keys)):
        #     if i not in [self.keygrid.itemAtPosition(w,0).widget().currentIndex() for w in range(1,self._get_number_of_keys()-1)]: #current indices in all comboboxes
        #         keycb.setCurrentIndex(i)
        #         break

        # self.keygrid.addWidget(keyedit,i,0,alignment=Qt.AlignTop)
        # self.keygrid.addItem(valueedit,i,1,rowSpan=-1,columnSpan=-1)
        self.keygrid.invalidate()
        self.layout().invalidate()
        self.filtersettingsgrid.invalidate()
        self.vboxleft.invalidate()

    def update_enabled_keys(self):
        # get selected item_ids
        selected_ids = []
        for combobox_id in range(1,self._get_number_of_keys()):
            combobox = self.keygrid.itemAtPosition(combobox_id,0).widget()
            selected_ids.append(combobox.currentIndex())

        # set selected ids disabled in other comboboxes
        for combobox_id in range(1,self._get_number_of_keys()):
            combobox = self.keygrid.itemAtPosition(combobox_id,0).widget()
            for item_id in range(combobox.count()):
                if item_id in selected_ids and combobox.currentIndex() != item_id:
                    combobox.model().item(item_id).setEnabled(False)
                else:
                    combobox.model().item(item_id).setEnabled(True)

    def _remove_key_value_pair(self):
        n_keys = self._get_number_of_keys()
        if n_keys>1: # not removing the column titles
            tbr = [self.keygrid.itemAtPosition(n_keys-1,0).widget(),self.keygrid.itemAtPosition(n_keys-1,1).widget()]
            curr_ind = tbr[0].currentIndex()
            for tbr_item in tbr:
                self.keygrid.removeWidget(tbr_item)
                tbr_item.deleteLater()
            self.keygrid.invalidate()

            self.update_enabled_keys()
            # for nkey in range(1,n_keys-1):
            #     cb = self.keygrid.itemAtPosition(nkey,0).widget()
            #     cb.model().item(curr_ind).setEnabled(True)

    def _get_number_of_keys(self):
        i = 0
        while self.keygrid.itemAtPosition(i,0):
            i += 1
        return i

    def addfilter(self):

        compfuncstr = str(self.lwcomparisonfunc.currentItem().text())

        # checking data consistency
        if compfuncstr in ['endswith\t[hasattr(x,"endswith") and x.endswith(y)]', 'startswith\t[hasattr(x,"startswith") and x.startswith(y)]']:
            for i in range(1,self._get_number_of_keys()):
                value = str(self.keygrid.itemAtPosition(i,1).widget().text())
                try:
                    valuetype = type(eval(value))
                # if (value[0] not in ['"',"'"]) or (value[-1] not in ['"',"'"]):
                except:
                    valuetype = None

                if valuetype  not in [str,unicode]:
                    QMessageBox.warning(self,'String input required','To be able to use the startswith or endswith '
                                                                     'comparison function you need to provide a string '
                                                                     'to compare to. You can define a string by using '
                                                                     'quotation marks at the beginning and end of your '
                                                                     'text (eg. "my string")')
                    return

        elif compfuncstr == 'is in list\t[x in y]':
            for i in range(1,self._get_number_of_keys()):
                value = str(self.keygrid.itemAtPosition(i,1).widget().text())
                # if (value[0] !='[') or (value[-1] != ']'):
                try:
                    valuetype = type(eval(value))
                except:
                    valuetype = None

                if not hasattr(valuetype,'__iter__'):
                    QMessageBox.warning(self,'List input required','To be able to use the "is in" '
                                                                     'comparison function you need to provide a list '
                                                                     'to compare to. You can define a list by using '
                                                                     'square brackets at the beginning and end of your '
                                                                     'list (eg. ["option1","option2"] or [1,2,3,4])')
                    return



        filter = {}
        filter['mode'] = 'and' if self.rbAND.isChecked() else 'or'
        filter['invert'] = self.cbinvert.isChecked()
        filter['recursive'] = self.cbrecursive.isChecked()
        try:
            filter['compfunc'] = lambda x,y: eval(compfuncstr.split('[')[1].split(']')[0])
        except SyntaxError:
            QMessageBox.warning(self,'Incorrect syntax', 'Your comparison function has an incorrect syntax. Please fix it and try again.')
            return
        filter['kwargs'] = {}
        for i in range(1,self._get_number_of_keys()):
            key = self.keygrid.itemAtPosition(i,0).widget().currentText()
            value = self.keygrid.itemAtPosition(i,1).widget().text()
            filter['kwargs'][str(key)] = eval(str(value))

        filter_name = ''
        if filter['invert']:
            filter_name += 'invert; '
        if filter['recursive']:
            filter_name += 'recursive; '
        # filter_name += 'comp.func: %s; '%compfuncstr.split('[')[0].rstrip('\t')
        filter_name += (' ' + filter['mode'].upper() + ' ').join(['(%s %s %s)'%(key,compfuncstr.split('[')[0].rstrip('\t'),filter['kwargs'][key]) for key in filter['kwargs']])


        if filter_name not in self.filters:

            self.filters[filter_name] = filter


            self.run_single_filter(filter_name)

            self.lwfilters.addItems([filter_name])


    def removefilter(self):
        i = self.lwfilters.currentRow()
        filter_name = str(self.lwfilters.currentItem().text())
        self.filters.pop(filter_name)
        self.lwfilters.takeItem(i)

        self.run_all_filters()

    def run_all_filters(self):
        self.filtered_table = copy.deepcopy(self.table)
        for filter in self.filters.values():
            self.filtered_table.filter(mode=filter['mode'],invert=filter['invert'],recursive=filter['recursive'],comparison_func=filter['compfunc'],**filter['kwargs'])
        self.update_tree(self.filtered_table)

    def run_single_filter(self,filter_name):
        if self.filtered_table == None:
            self.filtered_table = copy.deepcopy(self.table)
        filter = self.filters[filter_name]
        self.filtered_table.filter(mode=filter['mode'],invert=filter['invert'],recursive=filter['recursive'],comparison_func=filter['compfunc'],**filter['kwargs'])
        self.update_tree(self.filtered_table)


    def load_odml(self):
        # loading odml file
        self.table = odml_table.OdmlTable()
        self.settings.get_object('inputfilename')

        # setting xls_table or csv_table headers if necessary
        title_translator = {v:k for k,v in self.table._header_titles.iteritems()}
        if ((os.path.splitext(self.settings.get_object('inputfilename'))[1] in ['.xls','.csv']) and
                (self.settings.get_object('CBcustominput').isChecked())):
            inputheaderlabels = [str(l.text()) for l in self.settings.get_object('headerlabels')]
            inputcustomheaders = [str(cb.currentText()) for cb in self.settings.get_object('customheaders')]
            inputcolumnnames = [title_translator[label] for label in inputcustomheaders]
            self.table.change_header_titles(**dict(zip(inputcolumnnames,inputheaderlabels)))

        # loading input file
        if os.path.splitext(self.settings.get_object('inputfilename'))[1] == '.xls':
            self.table.load_from_xls_table(self.settings.get_object('inputfilename'))
        elif os.path.splitext(self.settings.get_object('inputfilename'))[1] == '.csv':
            self.table.load_from_csv_table(self.settings.get_object('inputfilename'))
        elif os.path.splitext(self.settings.get_object('inputfilename'))[1] == '.odml':
            self.table.load_from_file(self.settings.get_object('inputfilename'))
        else:
            raise ValueError('Unknown input file extension "%s"'
                             ''%os.path.splitext(self.settings.get_object('inputfilename'))[1])

        self.update_tree(self.table)

        self.filtered_table = copy.deepcopy(self.table)
        self.settings.register('filtered_table',self.filtered_table)

    def update_tree(self,table):
        self.odmltree.clear()
        self.create_sectiontree(self.odmltree,table)
        self.create_proptree(self.odmltree,table)
        self.create_valuetree(self.odmltree,table)

        self.odmltree.expandToDepth(0)


# ['Content','Value','DataUncertainty','DataUnit','odmlDatatype',
#                                 'Value','ValueDefinition',
#                                 'PropertyName','PropertyDefinition',
#                                 'SectionName','SectionType','SectionDefinition']


    def create_sectiontree(self,tree,table):
        sections = {value['Path'].strip('/'):('','','','','','','',value['SectionName'],value['SectionType'],value['SectionDefinition']) for value in table._odmldict}
        for sec in sorted(sections):
            sec_names = sec.split('/')
            parent_sec = tree.invisibleRootItem()
            for i in range(len(sec_names)):
                child =self.find_child(parent_sec,sec_names[i])
                if child:
                    parent_sec = child
                else:
                    new_sec = QTreeWidgetItem(parent_sec,[sec_names[i]] + list(sections[sec]))
                    parent_sec = new_sec

    def create_proptree(self,tree,table):
        props = {value['Path'].strip('/') + '/' + value['PropertyName']:('','','','','',value['PropertyName'],value['PropertyDefinition'],'','') for value in table._odmldict}
        for prop in props:
            prop_path = prop.split('/')
            parent_sec = tree.invisibleRootItem()
            for i in range(len(prop_path)):
                child =self.find_child(parent_sec,prop_path[i])
                if child:
                    parent_sec = child
                else:
                    new_sec = QTreeWidgetItem(parent_sec,[prop_path[i]] + list(props[prop]))
                    parent_sec = new_sec

    def create_valuetree(self,tree,table):
        values = {value['Path'].strip('/') + '/' + value['PropertyName'] + '/' + str(v):(str(value['Value']),value['DataUncertainty'],value['DataUnit'],value['odmlDatatype'],value['ValueDefinition'],'','','','','') for v,value in enumerate(table._odmldict)}
        for value in sorted(values):
            value_path = value.split('/')
            parent_sec = tree.invisibleRootItem()
            for i in range(len(value_path)):
                child =self.find_child(parent_sec,value_path[i])
                if child:
                    parent_sec = child
                if i == len(value_path)-2:
                    val = [str(v) for v in values[value]]
                    new_sec = QTreeWidgetItem(parent_sec,[''] + val)
                    parent_sec = new_sec



    def find_child(self,tree_sec,child_name):
        i = 0
        result = None
        while i < tree_sec.childCount():
            if tree_sec.child(i).text(0) == child_name:
                result = tree_sec.child(i)
                break
            i += 1

        return result




class SaveFilePage(QIWizardPage):
    def __init__(self,parent=None):
        super(SaveFilePage, self).__init__(parent)

        self.setTitle("Save the result")
        self.setSubTitle("Select a location to save your file. You can save the settings made during this generation with a custom configuration name. This configuration can be used in future runs of the wizard.")

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
        vbox.addWidget(QLabel('You can save the configuration used in this run'))
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

        self.expected_extension = '.odml'


        self.topLabel.setText("Where do you want to save your %s file?"%self.expected_extension.strip('.'))

        self.configlist.addItems(self.settings.get_all_config_names())


    def handlebuttonbrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setLabelText (QFileDialog.Accept, "Generate File" )
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))

        print self.settings.get_object('inputfilename')
        dlg.setDirectory(self.settings.get_object('inputfilename'))

        dlg.setFilter("%s files (*%s);;all files (*)"%(self.expected_extension.strip('.'),self.expected_extension))
        # filenames = []

        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])

        # self.outputfilename = str(QFileDialog.getSaveFileName(self, self.tr("Save File"),
        #                     os.path.dirname(self.settings.get_object('inputfilename')),"%s files (*%s);;all files (*)"%(self.expected_extension.strip('.'),self.expected_extension)))

         # extending filename if no extension is present
        if (self.outputfilename != '' and os.path.splitext(self.outputfilename)[1]==''):
            self.outputfilename += self.expected_extension
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
            filtered_table = self.settings.get_object('filtered_table')
            filtered_table.write2odml(self.settings.get_object('outputfilename'))

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
        if ((self.configlist.currentItem() == None) or (str(self.configlist.currentItem().text()) in ['','<New Configuration>'])):
            QMessageBox.warning(self,'No configuration name selected','You need to select a name for your '
                                                                      'configuration if you want to save it or '
                                                                      'define a new one (<New Configuration>)')
        else:
            config_name = str(self.configlist.currentItem().text())
            curritem = self.configlist.currentItem()
            if self.configlist.currentRow() != 0:
                self.configlist.item(0).setText('<New Configuration>')
            elif config_name in self.settings.get_all_config_names():
                QMessageBox.warning(self,'Configuration already exists','You need to chose a new name for your configuration.'
                                                                        'The name "%s" already exists'%config_name)
            else:
                curritem.setFlags(( Qt.ItemIsSelectable | Qt.ItemIsEnabled ))
                self.add_new_conf(self.configlist)
            self.settings.config_name = config_name
            self.settings.save_config()









