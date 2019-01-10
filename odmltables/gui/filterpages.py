# -*- coding: utf-8 -*-

import copy
import os
import sys
import subprocess

from future.utils import iteritems

# Workaround Python 2 and 3 unicode handling.
try:
    unicode = unicode
except NameError:
    unicode = str

from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as Qtw

from odmltables import odml_table
from .pageutils import QIWizardPage, clearLayout, shorten_path


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
        self.setSubTitle("Select the file you want to filter")

        vbox = self.layout

        # Adding input part
        topLabel = Qtw.QLabel(self.tr("Choose a file to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)

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

        self.cbcustominput = Qtw.QCheckBox('I changed the column names in the i'
                                           'nput table.')
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

        vbox.addStretch()

    def selectconfig(self):
        if self.configselection.currentIndex() != 0:
            self.settings.load_config(str(self.configselection.currentText()))

            # loading output format choice
            self.settings.register('CBcustominput', self.cbcustominput)
            self.settings.register('inputfilename', self, useconfig=False)
            short_filename = shorten_path(self.settings.get_object(
                'inputfilename'))
            self.inputfile.setText(short_filename)
            # self.settings.get_object('RBoutputxls')

    def handlebuttonbrowse(self):
        dlg = Qtw.QFileDialog()
        dlg.setNameFilters(["%s files (*%s)" % ('odml', '.odml'),
                            "%s files (*%s)" % ('xml', '.xml')])
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

    def validatePage(self):

        if ((not self.settings.is_registered('inputfilename')) or
                (not self.settings.get_object('inputfilename'))):
            Qtw.QMessageBox.warning(self, 'Select an input file',
                                    'You need to select an input file to continue.')
            return 0

        elif self.settings.get_object('inputfilename').split('.')[-1] \
                not in ['xls', 'csv', 'odml', 'xml']:
            Qtw.QMessageBox.warning(self, 'Wrong input format',
                                    'The input file has to be an ".xls", ".csv", '
                                    '".odml" or ".xml" file.')
            return 0

        return 1

    def nextId(self):
        if (((self.inputfilename[-5:] != '.odml') or (self.inputfilename[-4:] != '.xml')) and
                (self.settings.get_object('CBcustominput').isChecked())):
            return self.wizard().PageCustomInputHeader

        else:
            return self.wizard().PageFilter


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
        topLabel = Qtw.QLabel(self.tr("Provide the column types used in the "
                                      "input table"))
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
                Qtw.QMessageBox.warning(self, self.tr("Non-unique headers"),
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
                Qtw.QMessageBox.warning(self, self.tr("Incomplete headers"),
                                        self.tr("You need to have the mandatory"
                                                " headers %s in you table to be"
                                                " able to reconstruct an odml"
                                                "" % mandatory_headers))
                return 0
        return 1

    def nextId(self):
        return self.wizard().PageFilter


class FilterPage(QIWizardPage):
    def __init__(self, parent=None):
        super(FilterPage, self).__init__(parent)

        self.odmltreeheaders = ['Content',
                                'Value', 'DataUncertainty', 'DataUnit',
                                'odmlDatatype', 'PropertyName', 'PropertyDefinition',
                                'SectionName', 'SectionType',
                                'SectionDefinition']

        self.setTitle("Filter your data")
        self.setSubTitle("Create your filters and apply them to the "
                         "odmltables structure.")

        self.filters = {}

        hbox = Qtw.QVBoxLayout(self)

        # set up FILTER CREATOR FRAME
        frame_filtercreator = Qtw.QFrame(self)
        frame_filtercreator.setFrameShape(Qtw.QFrame.StyledPanel)
        frame_filtercreator.setMinimumHeight(600)
        frame_filtercreator.setSizePolicy(Qtw.QSizePolicy.Expanding,
                                          Qtw.QSizePolicy.Expanding)
        self.vbox_filtercreator = Qtw.QVBoxLayout()
        frame_filtercreator.setLayout(self.vbox_filtercreator)

        # Title
        filtercreatorlabel = Qtw.QLabel('Filter Creator')
        filtercreatorlabel.setStyleSheet('font: bold; font-size: 14pt')
        self.vbox_filtercreator.addWidget(filtercreatorlabel)

        # set up FILTER MODE FRAME
        groupbox_filtermode = Qtw.QGroupBox(self.tr('Mode'))
        groupbox_filtermode.setStyleSheet('QGroupBox {border: 1px solid gray; '
                                          'border-radius: 5px; margin-top: '
                                          '0.5em}'
                                          'QGroupBox::title {'
                                          'subcontrol-origin: margin;'
                                          'left: 10px;'
                                          'padding: 0 3px 0 3px;}')
        self.grid_filtermode = Qtw.QGridLayout()
        groupbox_filtermode.setLayout(self.grid_filtermode)

        self.rbAND = Qtw.QRadioButton(self.tr('&& [AND]'))
        self.rbOR = Qtw.QRadioButton('| [OR]')
        self.rbAND.setChecked(True)
        self.cbinvert = Qtw.QCheckBox('invert')
        self.cbrecursive = Qtw.QCheckBox('recursive')
        self.grid_filtermode.addWidget(self.rbAND, 0, 0)
        self.grid_filtermode.addWidget(self.rbOR, 0, 1)
        self.grid_filtermode.addWidget(self.cbinvert)
        self.grid_filtermode.addWidget(self.cbrecursive)

        self.vbox_filtercreator.addWidget(groupbox_filtermode)

        # set up FILTER FUNCTION FRAME
        groupbox_filterfunction = Qtw.QGroupBox(self.tr('Filter Function'))
        groupbox_filterfunction.setStyleSheet('QGroupBox {border: 1px solid '
                                              'gray; '
                                              'border-radius: 5px; margin-top: '
                                              '0.5em}'
                                              'QGroupBox::title {'
                                              'subcontrol-origin: margin;'
                                              'left: 10px;'
                                              'padding: 0 3px 0 3px;}')
        self.grid_filterfunction = Qtw.QGridLayout()
        groupbox_filterfunction.setLayout(self.grid_filterfunction)

        self.vbox_filtercreator.addWidget(groupbox_filterfunction)

        # set up ADD FILTER FUNCTION FRAME
        groupbox_addfilterfunction = Qtw.QGroupBox(self.tr('Custom Filter '
                                                           'Function Creator'))
        groupbox_addfilterfunction.setStyleSheet('QGroupBox {border: 1px solid '
                                                 'gray; '
                                                 'border-radius: 5px; '
                                                 'margin-top: '
                                                 '0.5em}'
                                                 'QGroupBox::title {'
                                                 'subcontrol-origin: margin;'
                                                 'left: 10px;'
                                                 'padding: 0 3px 0 3px;}')

        self.grid_addfilterfunction = Qtw.QGridLayout()
        self.grid_addfilterfunction.setSizeConstraint(Qtw.QLayout.SetMinimumSize)
        groupbox_addfilterfunction.setLayout(self.grid_addfilterfunction)

        self.grid_addfilterfunction.addWidget(Qtw.QLabel('Filter Function Name'),
                                              0, 0)
        self.grid_addfilterfunction.addWidget(Qtw.QLabel('Filter Function'), 0, 1)

        fname_layout = Qtw.QHBoxLayout()
        self.lineedit_filtername = Qtw.QLineEdit()
        fname_layout.addWidget(self.lineedit_filtername)
        fname_layout.addSpacing(30)
        self.grid_addfilterfunction.addLayout(fname_layout, 1, 0)
        fxy_layout = Qtw.QHBoxLayout()
        fxy_layout.addWidget(Qtw.QLabel('f(x,y)='))
        self.lineedit_fxy = Qtw.QLineEdit()
        fxy_layout.addWidget(self.lineedit_fxy)
        self.grid_addfilterfunction.addLayout(fxy_layout, 1, 1)
        add_button = Qtw.QPushButton('Add')
        add_button.setFixedWidth(50)
        add_button.clicked.connect(self.new_filter_func)
        self.grid_addfilterfunction.addWidget(add_button, 1, 2)

        self.vbox_filtercreator.addWidget(groupbox_addfilterfunction)

        # set up ATTRIBUTE FRAME
        self.groupbox_attributes = Qtw.QGroupBox(self.tr('Attribute Criteria'))
        self.groupbox_attributes.setStyleSheet('QGroupBox {border: 1px solid '
                                               'gray; '
                                               'border-radius: 5px; '
                                               'margin-top: '
                                               '0.5em}'
                                               'QGroupBox::title {'
                                               'subcontrol-origin: margin;'
                                               'left: 10px;'
                                               'padding: 0 3px 0 3px;}')

        self.grid_attributes = Qtw.QGridLayout()
        self.grid_attributes.setSizeConstraint(Qtw.QLayout.SetMinimumSize)
        self.groupbox_attributes.setLayout(self.grid_attributes)

        self.grid_attributes.addWidget(Qtw.QLabel('Attribute (x)'), 0, 1)
        self.grid_attributes.addWidget(Qtw.QLabel('Value (y)'), 0, 2)

        add_button = Qtw.QPushButton('+')
        add_button.setFixedWidth(30)
        add_button.clicked.connect(self.update_attributes)
        self.grid_attributes.addWidget(add_button, 1, 0)

        self.vbox_filtercreator.addWidget(self.groupbox_attributes)

        # APPLY FILTER BUTTON
        self.groupbox_applybutton = Qtw.QGroupBox()
        apply_filter_button = Qtw.QPushButton('Apply Filter')
        apply_filter_button.clicked.connect(self.applyfilter)
        vbox_applybutton = Qtw.QVBoxLayout()
        self.groupbox_applybutton.setLayout(vbox_applybutton)
        vbox_applybutton.addWidget(apply_filter_button)
        self.vbox_filtercreator.addWidget(self.groupbox_applybutton)

        self.vbox_filtercreator.addStretch()

        ########################
        # APPLIED FILTERS FRAME
        frame_appliedfilters = Qtw.QFrame(self)
        frame_appliedfilters.setFrameShape(Qtw.QFrame.StyledPanel)
        self.vbox_appliedfilters = Qtw.QVBoxLayout()
        frame_appliedfilters.setLayout(self.vbox_appliedfilters)
        frame_appliedfilters.setSizePolicy(Qtw.QSizePolicy.Expanding,
                                           Qtw.QSizePolicy.Expanding)

        filterlabel = Qtw.QLabel('Applied filters')
        filterlabel.setStyleSheet('font: bold; font-size: 14pt')
        self.vbox_appliedfilters.addWidget(filterlabel)

        self.lwfilters = Qtw.QListWidget()
        self.lwfilters.setSizePolicy(Qtw.QSizePolicy.Expanding,
                                     Qtw.QSizePolicy.Expanding)
        self.vbox_appliedfilters.addWidget(self.lwfilters)

        self.pbremovefilter = Qtw.QPushButton('Remove filter')
        self.pbremovefilter.clicked.connect(self.removefilter)
        self.vbox_appliedfilters.addWidget(self.pbremovefilter)

        ###########################
        # TREE REPRESENTATION FRAME
        frame_treerepresentation = Qtw.QFrame(self)
        frame_treerepresentation.setFrameShape(Qtw.QFrame.StyledPanel)
        vbox_treerepresentation = Qtw.QVBoxLayout()
        frame_treerepresentation.setLayout(vbox_treerepresentation)
        frame_treerepresentation.setSizePolicy(Qtw.QSizePolicy.Expanding,
                                               Qtw.QSizePolicy.Expanding)

        self.odmltree = Qtw.QTreeWidget()
        self.odmltree.setColumnCount(2)
        self.odmltree.setHeaderLabels(self.odmltreeheaders)
        self.odmltree.setSelectionMode(3)
        self.odmltree.setMinimumWidth(500)
        self.odmltree.setSizePolicy(Qtw.QSizePolicy.Expanding,
                                    Qtw.QSizePolicy.Expanding)

        columnwidths = [50] * len(self.odmltreeheaders)
        columnwidths[0:3] = [250, 100, 100]
        [self.odmltree.setColumnWidth(i, w) for i, w in enumerate(columnwidths)]

        vbox_treerepresentation.addWidget(self.odmltree)

        splitterv = Qtw.QSplitter(Qt.Vertical)
        splitterv.addWidget(frame_filtercreator)
        splitterv.addWidget(frame_appliedfilters)

        splitter2 = Qtw.QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitterv)
        splitter2.addWidget(frame_treerepresentation)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.groupbox_attributes.setFixedHeight(100)

        self.grid_attributes.itemAtPosition(1, 0).widget().click()

    def initializePage(self):
        # self.update_attributes()

        self.default_filter_functions = [
            ('==\t[x==y]',
             'x==y'),
            ('endswith\t[hasattr(x,"endswith") and x.endswith(y)]',
             'hasattr(x,"endswith") and x.endswith(y)'),
            ('startswith\t[hasattr(x,"startswith") and x.startswith(y)]',
             'hasattr(x,"startswith") and x.startswith(y)'),
            ('is in list\t[x in y]',
             'x in y'),
            ('contains\t[type(x)==str and y in x]',
             'type(x)==str and y in x')]

        # self.filter_functions = copy.deepcopy(self.default_filter_functions)

        clearLayout(self.grid_filterfunction)

        self.filterfunctionnames = [f[0] for f in self.default_filter_functions]
        self.filterfunctions = [f[1] for f in self.default_filter_functions]

        self.settings.register('filterfunctionnames', self.filterfunctionnames)
        self.settings.register('filterfunctions', self.filterfunctions)

        self.view_filterfunctions()

        self.load_odml()

        self.settings.register('filters', self.filters)

        self.run_all_filters()

        self.lwfilters.clear()

        for filter in list(self.filters.values()):
            filter_name = self._get_filter_name(filter)
            self._show_applied_filter(filter, filter_name)

        self.odmltree.expandToDepth(0)

    def view_filterfunctions(self):
        clearLayout(self.grid_filterfunction)

        for f, filter in enumerate(
                zip(self.filterfunctionnames, self.filterfunctions)):
            filter_name = filter[0]
            filter_abbr = filter_name.split('[')[0].strip(' ').rstrip('\t')
            filter_func_str = filter[1]
            self.grid_filterfunction.addWidget(Qtw.QLabel(filter_abbr), f, 1)
            self.grid_filterfunction.addWidget(Qtw.QRadioButton(filter_func_str),
                                               f, 2)
            if f >= len(self.default_filter_functions):
                remove_button = Qtw.QPushButton('-')
                remove_button.setFixedWidth(30)
                remove_button.clicked.connect(self.removefilterfunction)
                self.grid_filterfunction.addWidget(remove_button, f, 0)

        self.grid_filterfunction.itemAtPosition(0, 2).widget().setChecked(True)

    def new_filter_func(self):

        if len(self.filterfunctions) >= len(self.default_filter_functions) + 5:
            Qtw.QMessageBox.warning(self, 'Too many functions',
                                    'You can only define up to 5 custom functions.')
            return

        fname = str(self.lineedit_filtername.text())
        fstr = str(self.lineedit_fxy.text())

        # consistency checks
        if not (fname and fstr):
            Qtw.QMessageBox.warning(self, 'No function defined',
                                    'You need to define your a function name and '
                                    'a function expression depending on the '
                                    'attribute (x) and the value (y).')
            return
        elif '[' in fname or '[' in fstr or ']' in fname or ']' in fstr:
            Qtw.QMessageBox.warning(self, 'Invalid expression',
                                    'You can not use square brackets to define '
                                    'your function. Please adapt your function '
                                    'accordingly.')
            return
        elif '%s\t[%s]' % (fname, fstr) in self.filterfunctionnames:
            Qtw.QMessageBox.warning(self, 'Function already exists',
                                    'You can not define a function with name %s, '
                                    'a function of this name already exists' % (
                                        fname))
            return

        self.filterfunctionnames.append('%s\t[%s]' % (fname, fstr))
        self.filterfunctions.append('%s' % fstr)
        self.view_filterfunctions()

        # set last radiobutton activated
        i = 0
        while self.grid_filterfunction.itemAtPosition(i, 2):
            i += 1
        self.grid_filterfunction.itemAtPosition(i - 1, 2).widget().setChecked(
            True)

    def update_attributes(self):
        sender = self.sender()
        nattributes = self._get_number_of_keys()
        idx = self.grid_attributes.indexOf(sender)
        location = self.grid_attributes.getItemPosition(idx)

        # in case of full line -> remove line
        if self.grid_attributes.itemAtPosition(location[0], location[1] + 1):
            # deleting row
            tbr = [self.grid_attributes.itemAtPosition(location[0], location[
                1] + i).widget() for i in list(range(3))]
            for widget in tbr:
                self.grid_attributes.removeWidget(widget)
                widget.deleteLater()

            # moving lower widgets upward
            for row_id in list(range(location[0] + 1, nattributes + 1)):
                for col_id in list(range(3)):
                    item = self.grid_attributes.itemAtPosition(row_id, col_id)
                    widget = item.widget() if hasattr(item, 'widget') else None
                    if widget:
                        widx = self.grid_attributes.indexOf(widget)
                        wloc = self.grid_attributes.getItemPosition(widx)

                        self.grid_attributes.removeWidget(widget)
                        self.grid_attributes.addWidget(widget, wloc[0] - 1, wloc[1])

            self.update_enabled_keys()

        # in case of an empty line -> add line
        else:
            # moving add button
            widx = self.grid_attributes.indexOf(sender)
            wloc = self.grid_attributes.getItemPosition(widx)
            if wloc[0] < len(self.odmltreeheaders) - 1:
                self.grid_attributes.removeWidget(sender)
                self.grid_attributes.addWidget(sender, wloc[0] + 1, wloc[1])

                # adding row
                removebutton = Qtw.QPushButton('-')
                removebutton.setFixedWidth(30)
                removebutton.clicked.connect(self.update_attributes)
                self.grid_attributes.addWidget(removebutton, *wloc)

                all_keys = self.odmltreeheaders[1:]
                # get previously selected ids
                selected_ids = []
                for combobox_id in list(range(1, self._get_number_of_keys())):
                    combobox = self.grid_attributes.itemAtPosition(combobox_id,
                                                                   1).widget()
                    selected_ids.append(combobox.currentIndex())

                keycb = Qtw.QComboBox()
                keycb.addItems(all_keys)
                keycb.currentIndexChanged.connect(self.update_enabled_keys)

                self.grid_attributes.addWidget(keycb, wloc[0], wloc[1] + 1)
                self.grid_attributes.addWidget(Qtw.QLineEdit(), wloc[0],
                                               wloc[1] + 2)

                # set to first non-selected id
                for id in list(range(len(self.odmltreeheaders))):
                    if id not in selected_ids:
                        keycb.setCurrentIndex(id)
                        break

            else:
                Qtw.QMessageBox.warning(self, 'Too many attributes',
                                        'You can not define more than %s '
                                        'attributes.' % (len(
                                            self.odmltreeheaders) - 1))

        self.layout().invalidate()

    def update_enabled_keys(self):
        # get selected item_ids
        selected_ids = []
        for combobox_id in list(range(1, self._get_number_of_keys())):
            combobox = self.grid_attributes.itemAtPosition(combobox_id,
                                                           1).widget()
            selected_ids.append(combobox.currentIndex())

        # set selected ids disabled in other comboboxes
        for combobox_id in list(range(1, self._get_number_of_keys())):
            combobox = self.grid_attributes.itemAtPosition(combobox_id,
                                                           1).widget()
            for item_id in list(range(combobox.count())):
                if item_id in selected_ids and \
                                combobox.currentIndex() != item_id:
                    combobox.model().item(item_id).setEnabled(False)
                else:
                    combobox.model().item(item_id).setEnabled(True)

    def _get_number_of_keys(self):
        i = 0
        while self.grid_attributes.itemAtPosition(i, 1):
            i += 1
        return i

    def applyfilter(self):

        # get selected filterfunction
        for id in list(range(self.grid_filterfunction.count())):
            widget = self.grid_filterfunction.itemAt(id).widget()
            if hasattr(widget, 'isChecked') and widget.isChecked():
                wloc = self.grid_filterfunction.getItemPosition(id)
                break

        filterfuncstr = self.filterfunctions[wloc[0]]

        # checking data consistency
        if filterfuncstr in ['hasattr(x,"endswith") and x.endswith(y)',
                             'hasattr(x,"startswith") and x.startswith(y)']:
            for i in list(range(1, self._get_number_of_keys())):
                value = str(self.grid_attributes.
                            itemAtPosition(i, 2).widget().text())
                try:
                    valuetype = type(eval(value))
                # if (value[0] not in ['"',"'"]) or (value[-1] not in ['"',
                # "'"]):
                except:
                    valuetype = None

                if valuetype not in [str, unicode]:
                    Qtw.QMessageBox.warning(self, 'String input required',
                                            'To be able to use the startswith or '
                                            'endswith '
                                            'filter function you need to provide '
                                            'a string '
                                            'to compare to. You can define a '
                                            'string by using '
                                            'quotation marks at the beginning and '
                                            'end of your '
                                            'text (eg. "my string")')
                    return

        elif filterfuncstr == 'x in y':
            for i in list(range(1, self._get_number_of_keys())):
                value = str(self.grid_attributes.
                            itemAtPosition(i, 2).widget().text())
                # if (value[0] !='[') or (value[-1] != ']'):
                try:
                    valuetype = type(eval(value))
                except:
                    valuetype = None

                if not hasattr(valuetype, '__iter__'):
                    Qtw.QMessageBox.warning(self, 'List input required',
                                            'To be able to use the "is in" filter function you '
                                            'need to provide a list to compare to. You can define '
                                            'a list by using square brackets at the beginning and '
                                            'end of your list (eg. ["option1","option2"] or '
                                            '[1,2,3,4])')
                    return

        filter = {}
        filter['mode'] = 'and' if self.rbAND.isChecked() else 'or'
        filter['invert'] = self.cbinvert.isChecked()
        filter['recursive'] = self.cbrecursive.isChecked()
        filter['compfuncstr'] = filterfuncstr
        try:
            compfunc = lambda x, y: \
                eval(filter['compfuncstr'])
        except SyntaxError:
            Qtw.QMessageBox.warning(self, 'Incorrect syntax',
                                    'Your filter function has an incorrect '
                                    'syntax. Please fix it and try again.')
            return
        filter['kwargs'] = {}
        for i in list(range(1, self._get_number_of_keys())):
            key = self.grid_attributes. \
                itemAtPosition(i, 1).widget().currentText()
            value = self.grid_attributes.itemAtPosition(i, 2).widget().text()
            filter['kwargs'][str(key)] = str(value)

        filter_name = self._get_filter_name(filter)

        if filter_name not in self.filters:
            self._show_applied_filter(filter, filter_name)

        else:
            Qtw.QMessageBox.warning(self, 'Filter already exists',
                                    'You can not apply the same filter twice.')

    def _get_filter_name(self, filter):
        filterfuncstr = filter['compfuncstr']

        filter_name = ''
        if filter['invert']:
            filter_name += 'invert; '
        if filter['recursive']:
            filter_name += 'recursive; '
        filter_name += (' ' + filter['mode'].upper() + ' ').join(
            ['(%s %s %s)' % (key,
                             filterfuncstr.split('[')[0].rstrip('\t'),
                             filter['kwargs'][key])
             for key in filter['kwargs']])

        return filter_name

    def _show_applied_filter(self, filter, filter_name):
        self.filters[filter_name] = filter

        try:
            self.run_single_filter(filter_name)
        except (ValueError, NameError) as e:
            self.filters.pop(filter_name)
            self.reset_filtersettings()
            return

        self.lwfilters.addItems([filter_name])

        self.reset_filtersettings()

    def reset_filtersettings(self):
        self.rbAND.setChecked(True)
        self.rbOR.setChecked(False)
        self.cbinvert.setChecked(False)
        self.cbrecursive.setChecked(False)

        self.grid_filterfunction.itemAtPosition(0, 2).widget().setChecked(True)

        self.lineedit_filtername.setText('')
        self.lineedit_fxy.setText('')

        w = self.grid_attributes.itemAtPosition(2, 0).widget()
        while str(w.text()) == '-':
            w.click()
            w = self.grid_attributes.itemAtPosition(2, 0).widget()

        self.grid_attributes.itemAtPosition(1, 1).widget().setCurrentIndex(0)
        self.grid_attributes.itemAtPosition(1, 2).widget().setText('')

    def removefilterfunction(self):
        sender = self.sender()

        idx = self.grid_filterfunction.indexOf(sender)
        location = self.grid_filterfunction.getItemPosition(idx)

        self.filterfunctionnames.pop(location[0])
        self.filterfunctions.pop(location[0])
        self.view_filterfunctions()

    def removefilter(self):
        i = self.lwfilters.currentRow()
        filter_name = str(self.lwfilters.currentItem().text())
        self.filters.pop(filter_name)
        self.lwfilters.takeItem(i)

        self.run_all_filters()

    def run_all_filters(self):
        # keeping filtered_table object and not substituting whole object to
        # be able to retrieve data from registered object
        self.filtered_table._odmldict = copy.deepcopy(self.table._odmldict)
        for filter_name, filter in iteritems(self.filters):
            #     self.filtered_table.filter(mode=filter['mode'],
            #                                invert=filter['invert'],
            #                                recursive=filter['recursive'],
            #                                comparison_func=lambda x,y:\
            #                                             eval(filter[
            # 'compfuncstr']),
            #                                **{key:eval(value) for key,value in
            #                                 iteritems(filter['kwargs'])})
            # self.update_tree(self.filtered_table)

            self.run_single_filter(filter_name)
        self.update_tree(self.filtered_table)

    def run_single_filter(self, filter_name):
        if self.filtered_table == None:
            self.filtered_table = copy.deepcopy(self.table)
        filter = self.filters[filter_name]

        try:
            [eval(value) for value in list(filter['kwargs'].values())]
        except:
            Qtw.QMessageBox.warning(self, 'Non-interpretable value',
                                'Can not interpret list of values "{}". There is a non-valid '
                                'python object contained. To generate a string put your '
                                'text into quotation marks. To define a list '
                                'use square brackets.'.format(str(filter['kwargs'].values())))
            raise ValueError('Can not interpret values "{}"'.format(str(filter['kwargs'].values())))

        try:
            self.filtered_table.filter(mode=filter['mode'],
                                       invert=filter['invert'],
                                       recursive=filter['recursive'],
                                       comparison_func=lambda x, y: \
                                           eval(filter['compfuncstr']),
                                       **{key: eval(value) for key, value in
                                          iteritems(filter['kwargs'])})
        except Exception as e:
            message = e.message if hasattr(e, 'message') else (str(e))
            Qtw.QMessageBox.warning(self, 'Filter Warning', message)
            raise e
        self.update_tree(self.filtered_table)

    # TODO: check if this can also be done via XPath + provide xpath
    # interface in gui (see http://lxml.de/xpathxslt.html)
    def load_odml(self):
        # loading odml file
        self.table = odml_table.OdmlTable()
        self.settings.get_object('inputfilename')

        # setting xls_table or csv_table headers if necessary
        title_translator = {v: k for k, v in
                            iteritems(self.table._header_titles)}
        if ((os.path.splitext(self.settings.get_object('inputfilename'))[1]
             in ['.xls', '.csv']) and
                (self.settings.get_object('CBcustominput').isChecked())):
            inputheaderlabels = [str(l.text()) for l in self.settings.get_object('headerlabels')]
            inputcustomheaders = [str(cb.currentText()) for cb in
                                  self.settings.get_object('customheaders')]
            inputcolumnnames = [title_translator[label] for label in inputcustomheaders]
            self.table.change_header_titles(**dict(zip(inputcolumnnames, inputheaderlabels)))

        # loading input file
        if os.path.splitext(self.settings.get_object('inputfilename'))[1] == '.xls':
            self.table.load_from_xls_table(self.settings.get_object('inputfilename'))
        elif os.path.splitext(self.settings.get_object('inputfilename'))[1] == '.csv':
            self.table.load_from_csv_table(self.settings.get_object('inputfilename'))
        elif os.path.splitext(self.settings.get_object('inputfilename'))[1] in ['.odml', '.xml']:
            self.table.load_from_file(self.settings.get_object('inputfilename'))
        else:
            raise ValueError('Unknown input file extension "%s"'
                             '' % os.path.splitext(self.settings.get_object('inputfilename'))[1])

        self.update_tree(self.table)

        self.filtered_table = copy.deepcopy(self.table)
        self.settings.register('filtered_table', self.filtered_table,  useconfig=False)

    def update_tree(self, table):
        self.odmltree.clear()
        self.create_sectiontree(self.odmltree, table)
        self.create_proptree(self.odmltree, table)

        self.odmltree.expandToDepth(0)

    def create_sectiontree(self, tree, table):
        sections = {prop['Path'].strip('/').split(':')[0]: ['', '', '', '', '', '',
                                               prop['Path'].split(':')[0].split('/')[-1],
                                               prop['SectionType'],
                                               prop['SectionDefinition']]
                    for prop in table._odmldict}

        self.replace_Nones(sections)
        for sec in sorted(sections):
            sec_names = sec.split('/')
            parent_sec = tree.invisibleRootItem()
            for i in list(range(len(sec_names))):
                child = self.find_child(parent_sec, sec_names[i])
                if child:
                    parent_sec = child
                else:
                    new_sec = Qtw.QTreeWidgetItem(parent_sec, [sec_names[i]] +
                                                  list(sections[sec]))
                    parent_sec = new_sec

    def create_proptree(self, tree, table):
        props = {prop['Path'].strip('/').replace(':', '/'):
                     [prop['Value'],
                      prop['DataUncertainty'],
                      prop['DataUnit'],
                      prop['odmlDatatype'],
                      prop['Path'].split(':')[-1],
                      prop['PropertyDefinition'], '', '', '']
                 for prop in table._odmldict}

        self.replace_Nones(props)
        for prop in props:
            prop_path = prop.split('/')
            parent_sec = tree.invisibleRootItem()
            for i in list(range(len(prop_path))):
                child = self.find_child(parent_sec, prop_path[i])
                if child:
                    parent_sec = child
                else:
                    values = copy.deepcopy(props[prop][0])
                    tmp_prop = props[prop]
                    prop_name = prop_path[i]
                    for val in values:
                        tmp_prop[0] = str(val)
                        Qtw.QTreeWidgetItem(parent_sec, [prop_name] + tmp_prop)
                        prop_name = ''
                        tmp_prop = [''] * len(tmp_prop)

    def replace_Nones(self, data_dict):
        for value_list in list(data_dict.values()):
            for i in list(range(len(value_list))):
                if value_list[i] == None:
                    value_list[i] = ''

    def find_child(self, tree_sec, child_name):
        i = 0
        result = None
        while i < tree_sec.childCount():
            if tree_sec.child(i).text(0) == child_name:
                result = tree_sec.child(i)
                break
            i += 1

        return result


class SaveFilePage(QIWizardPage):
    def __init__(self, parent=None):
        super(SaveFilePage, self).__init__(parent)

        self.setTitle("Save the result")
        self.setSubTitle("Select a location to save your file. You can save "
                         "the settings made during this generation with a "
                         "custom configuration name. This configuration can be "
                         "used in future runs of the gui.")

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
        self.buttonbrowse = Qtw.QPushButton("Browse")
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
        vbox.addWidget(Qtw.QLabel('You can save the configuration '
                                  'used in this run'))
        grid = Qtw.QGridLayout()
        self.configlist = Qtw.QListWidget()
        self.configlist.itemActivated.connect(self.newconfname)
        self.add_new_conf(self.configlist)
        grid.addWidget(self.configlist, 0, 0, 1, 2)
        grid.addWidget(self.buttonsaveconfig, 1, 0)
        grid.addWidget(self.buttondeleteconfig, 1, 1)
        vbox.addLayout(grid)

        self.outputfilename = ''
        self.settings.register('outputfilename', self, useconfig=False)
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        self.expected_extensions = ['.odml', '.xml']

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

        dlg.setDirectory(os.path.dirname(self.settings.get_object('inputfilename')))


        filternames = ["%s files (*%s)" % (ext.strip('.'), ext) for ext in
                       self.expected_extensions]
        filternames += ["all files (*)"]
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

        if ((os.path.splitext(self.outputfilename)[1] not in self.expected_extensions) and
                (os.path.splitext(self.outputfilename)[1] != '')):
            Qtw.QMessageBox.warning(self, 'Wrong file format',
                                    'The output file format is supposed to be "%s",'
                                    ' but you selected "%s"'
                                    '' % (' or '.join(self.expected_extensions),
                                          os.path.splitext(self.outputfilename)[1]))
            self.handlebuttonbrowse()

        elif self.outputfilename != '':
            filtered_table = self.settings.get_object('filtered_table')
            filtered_table.write2odml(self.settings.get_object('outputfilename'))

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

            # need to remove odmltables object as this can not be saved
            self.settings.remove_object('filtered_table')

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
