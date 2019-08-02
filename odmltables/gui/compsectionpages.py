# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 09:31:26 2016

@author: pick
"""
import os
import sys
import subprocess

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QMessageBox,
                         QLineEdit, QPushButton, QLabel, QGroupBox,
                         QGridLayout, QTreeWidget, QTreeWidgetItem,
                         QToolButton, QFileDialog, QCheckBox, QComboBox,
                         QFrame, QSizePolicy, QRadioButton)

from PyQt5.QtCore import Qt

from .pageutils import QIWizardPage, clearLayout, shorten_path
import odml
import odmltables.compare_section_csv_table
import odmltables.compare_section_xls_table


class ChooseFilePage(QIWizardPage):
    """
    """

    def __init__(self, parent=None, filename=None):
        super(ChooseFilePage, self).__init__(parent)

        if filename is None:
            self.inputfilename = ''
        else:
            self.inputfilename = filename
        self.settings.register('inputfilename', self, useconfig=False)

        self.initUI()

    def initUI(self):

        # Adding input part
        vbox = QVBoxLayout()
        topLabel = QLabel(self.tr("Choose a file to load"))
        topLabel.setWordWrap(True)
        vbox.addWidget(topLabel)
        vbox.addSpacing(20)

        # Add first horizontal box
        self.buttonbrowse = QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.inputfile = QLabel(self.inputfilename)
        self.inputfile.setWordWrap(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.buttonbrowse)
        hbox1.addWidget(self.inputfile)
        hbox1.addStretch()
        vbox.addLayout(hbox1)

        vbox.addSpacing(10)

        # Adding output part
        bottomLabel = QLabel(self.tr("Select an output format"))
        bottomLabel.setWordWrap(True)
        vbox.addWidget(bottomLabel)
        vbox.addWidget(bottomLabel)

        # Add second horizontal box
        self.rbuttonxls = QRadioButton(self.tr("xls"))
        self.rbuttoncsv = QRadioButton(self.tr("csv"))
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.rbuttonxls)
        hbox2.addSpacing(50)
        hbox2.addWidget(self.rbuttoncsv)
        hbox2.addStretch()
        vbox.addLayout(hbox2)
        vbox.addStretch()

        self.setLayout(vbox)

    def initializePage(self):

        self.setTitle("Select an input file")
        self.setSubTitle("Select the file you want to convert and specify the "
                         "output format you want to generate")

        self.settings.register('RBoutputxls', self.rbuttonxls)
        self.settings.register('RBoutputcsv', self.rbuttoncsv)

        self.rbuttonxls.setChecked(True)

    def handlebuttonbrowse(self):
        dlg = QFileDialog()
        dlg.setNameFilters(["%s files (*%s)" % ('odml', '.odml'),
                            "%s files (*%s)" % ('xml', '.xml')])
        fn = self.settings.get_object('inputfilename')
        if fn:
            dlg.selectFile(fn)

        if dlg.exec_():
            self.inputfilename = str(dlg.selectedFiles()[0])

        self.settings.register('inputfilename', self, useconfig=False)
        self.inputfile.setText(shorten_path(self.inputfilename))

    def validatePage(self):
        if not any((self.settings.get_object('RBoutputxls').isChecked(),
                    self.settings.get_object('RBoutputcsv').isChecked())):
            QMessageBox.warning(self, 'Select a format',
                                'You need to select a table format to '
                                'continue.')
            return 0

        if ((not self.settings.is_registered('inputfilename')) or
                (not self.settings.get_object('inputfilename'))):
            QMessageBox.warning(self, 'Select an input file',
                                'You need to select an input file to continue.')
            return 0

        return 1


class ChooseSectionsPage(QIWizardPage):
    """
    page to choose the sections that should be compared in the table
    """

    def __init__(self, parent=None):
        super(ChooseSectionsPage, self).__init__(parent)
        self.selected_sections = []  # sections in the right tree
        self.sections = []  # all sections without the selected
        self.filtered_sections = []  # filtered sections without the selected
        self.initUI()

    def initUI(self):

        mainlayout = QVBoxLayout()

        # layout containing the treewidgets
        sectionlistlayout = QHBoxLayout()

        # layout for filter form
        filterbox = QGroupBox("Filter")

        self.LEsecname = QLineEdit()
        self.LEsectype = QLineEdit()
        self.LEpropname = QLineEdit()

        filterlayout = QGridLayout()
        filterlayout.addWidget(QLabel("Section Name"), 1, 0)
        filterlayout.addWidget(QLabel("Section Type"), 2, 0)
        filterlayout.addWidget(QLabel("Property Name"), 3, 0)
        filterlayout.addWidget(self.LEsecname, 1, 1)
        filterlayout.addWidget(self.LEsectype, 2, 1)
        filterlayout.addWidget(self.LEpropname, 3, 1)
        filterbox.setLayout(filterlayout)

        self.LEsecname.textChanged.connect(self.filterSections)
        self.LEsectype.textChanged.connect(self.filterSections)
        self.LEpropname.textChanged.connect(self.filterSections)

        # define layout for the trre-widgets containing the sections
        self.section_tree = QTreeWidget()
        self.section_tree.setColumnCount(2)
        self.section_tree.setHeaderLabels(["Name", "Path"])
        self.section_tree.itemDoubleClicked.connect(self.toright)

        self.selection_tree = QTreeWidget()
        self.selection_tree.setColumnCount(2)
        self.selection_tree.setHeaderLabels(["Name", "Path"])
        self.selection_tree.itemDoubleClicked.connect(self.toleft)

        self.selection_tree.setSelectionMode(3)
        self.section_tree.setSelectionMode(3)

        self.settings.register("selected_secs", self.selected_sections)

        # buttons to move items of the tree-widgets
        movebuttonlayout = QVBoxLayout()
        btn_right = QToolButton()
        btn_right.setArrowType(Qt.RightArrow)
        btn_right.clicked.connect(self.toright)
        btn_left = QToolButton()
        btn_left.setArrowType(Qt.LeftArrow)
        btn_left.clicked.connect(self.toleft)

        movebuttonlayout.addStretch(1)
        movebuttonlayout.addWidget(btn_right)
        movebuttonlayout.addSpacing(1)
        movebuttonlayout.addWidget(btn_left)
        movebuttonlayout.addStretch(1)

        sectionlistlayout.addWidget(self.section_tree)
        sectionlistlayout.addSpacing(1)
        sectionlistlayout.addLayout(movebuttonlayout)
        sectionlistlayout.addSpacing(1)
        sectionlistlayout.addWidget(self.selection_tree)

        mainlayout.addLayout(sectionlistlayout)
        self.selectallcb = QCheckBox('select all (Ctrl+A)')
        self.selectallcb.stateChanged.connect(self.selectall)
        mainlayout.addWidget(self.selectallcb)
        mainlayout.addWidget(filterbox)

        self.setTitle("Select Sections")
        self.setLayout(mainlayout)
        self.adjustSize()

    def initializePage(self):

        # load sections and properties from the selected file
        odmldoc = odml.load(self.settings.get_object("inputfilename"))
        # resolve links and includes
        odmldoc.finalize()
        for section in odmldoc.itersections():
            self.sections.append([section.name,
                                  section.get_path(),
                                  [p.name for p in section.properties],
                                  section.type])

        # fill tree widget with sections and properties
        for line in self.sections:
            parent = QTreeWidgetItem([line[0], line[1]])
            for p in line[2]:
                QTreeWidgetItem(parent, [str(p)])
            self.section_tree.addTopLevelItem(parent)

        self.filtered_sections = list(self.sections)
        self.setTitle("Choose Sections")
        self.setSubTitle("Choose the sections you want to compare")

    def _get_selected_rows(self, tree):
        """
        function to determine the selected rows in a specified QTreeWidget
        """

        rows = []
        for index in tree.selectedIndexes():
            if index.parent().row() is -1:
                rows.append(index.row())
            else:
                # if a property is selected, the whole section containing this
                # property shall be moved
                rows.append(index.parent().row())

        # sort rownumbers in descending order to prevent shifting when moving
        # the items
        return sorted(list(set(rows)), reverse=True)

    def toright(self):
        """
        function to shift items from the left TreeWidget to the right
        """

        rows = self._get_selected_rows(self.section_tree)
        for row in rows:
            self.selection_tree.addTopLevelItem(
                self.section_tree.takeTopLevelItem(row))
            self.selected_sections.append(self.sections.pop(
                self.sections.index(self.filtered_sections[row])))
            self.filtered_sections.pop(row)

    def toleft(self):
        """
        function to shift items from the right TreeWidget to the left
        """

        rows = self._get_selected_rows(self.selection_tree)
        for row in rows:
            self.section_tree.addTopLevelItem(
                self.selection_tree.takeTopLevelItem(row))
            item = self.selected_sections.pop(row)
            self.sections.append(item)
            self.filtered_sections.append(item)

    def filterSections(self):

        # find sections that match the filter
        self.filtered_sections = [s for s in self.sections
                                  if str(self.LEsecname.text()) in s[0]
                                  and str(self.LEsectype.text()) in s[3]
                                  and any([str(self.LEpropname.text())
                                           in p for p in s[2]])]
        # clear left treewidget
        self.section_tree.clear()

        # fill left treewidget with the filtered sections
        for line in self.filtered_sections:
            parent = QTreeWidgetItem([line[0], line[1]])
            for p in line[2]:
                QTreeWidgetItem(parent, [p])
            self.section_tree.addTopLevelItem(parent)

    def selectall(self):
        if self.selectallcb.isChecked():
            self.section_tree.selectAll()
        else:
            self.section_tree.clearSelection()

    def validatePage(self):
        if not self.settings.get_object("selected_secs"):
            QMessageBox.warning(self, 'No sections chosen',
                                'You should choose at least two sections to be '
                                'compared in the table.')
            return 0
        return 1


class ChoosePropertiesPage(QIWizardPage):
    # idea: page to choose the properties that should be compared.
    # not useful yet, because odmltables doesnt provide this option

    def __init__(self, parent=None):
        super(ChoosePropertiesPage, self).__init__(parent)


class ChooseStylesPage(QIWizardPage):
    def __init__(self, parent=None):
        super(ChooseStylesPage, self).__init__(parent)


class SaveTablePage(QIWizardPage):
    """
    may be replaced by SaveFilePage
    """

    def __init__(self, parent=None):
        super(SaveTablePage, self).__init__(parent)

        self.setTitle("Save the result")
        self.setSubTitle("Select a location to save your file.")

        # Set up layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

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
        self.buttonbrowse = QPushButton("Save file")
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
        # vbox.addSpacing(10)
        vbox.addWidget(self.buttonshow)
        vbox.addStretch()

        self.settings.register('outputfilename', self, useconfig=False)
        short_filename = shorten_path(self.outputfilename)
        self.outputfile.setText(short_filename)

        if self.settings.get_object('RBoutputxls').isChecked():
            self.expected_extension = '.xls'
        elif self.settings.get_object('RBoutputcsv').isChecked():
            self.expected_extension = '.csv'
        else:
            raise ValueError('Can not save file without selection of '
                             'output format.')

        self.topLabel.setText("Where do you want to save your "
                              "%s file?" % self.expected_extension.strip('.'))
        self.issaved = False

    def handlebuttonbrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setLabelText(QFileDialog.Accept, "Save comparison")
        dlg.setDefaultSuffix(self.expected_extension.strip('.'))

        inputfilename = self.settings.get_object('inputfilename')
        dirname = os.path.dirname(inputfilename)
        suggested_filename = os.path.splitext(os.path.basename(
            inputfilename))[0] + self.expected_extension
        dlg.setDirectory(dirname)
        dlg.selectFile(suggested_filename)

        filternames = ["%s files (*%s)" % (ext.strip('.'), ext) for ext in
                       [self.expected_extension]]
        filternames += ["all files (*)"]
        dlg.setNameFilters(filternames)

        if dlg.exec_():
            self.outputfilename = str(dlg.selectedFiles()[0])
        self.settings.register('outputfilename', self)
        self.outputfile.setText(shorten_path(self.outputfilename))

        if self.outputfilename:
            self.compare()
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

    def _saveXlsTable(self):
        table = odmltables.compare_section_xls_table.CompareSectionXlsTable()
        table.load_from_file(self.settings.get_object("inputfilename"))
        selections = [s[0] for s in self.settings.get_object("selected_secs")]
        table.choose_sections(*selections)
        table.write2file(self.settings.get_object("outputfilename"))

    def _saveCsvTable(self):
        table = odmltables.compare_section_csv_table.CompareSectionCsvTable()
        table.load_from_file(self.settings.get_object("inputfilename"))
        selections = [s[0] for s in self.settings.get_object("selected_secs")]
        table.choose_sections(*selections)
        table.write2file(self.settings.get_object("outputfilename"))

    def compare(self):
        if not (self.settings.is_registered('outputfilename') and
                    self.settings.get_object('outputfilename')):
            QMessageBox.warning(self, 'Select an outputfile',
                                'You need to select an outputfile to continue.')
            return 0

        if self.settings.get_object('RBoutputxls').isChecked():
            self._saveXlsTable()
        elif self.settings.get_object('RBoutputcsv').isChecked():
            self._saveCsvTable()
        else:
            raise ValueError('No output format was selected.')

    def validatePage(self):
        if self.issaved == False:
            quit_msg = "Are you sure you want to exit the program without " \
                       "saving your file?"
            reply = QMessageBox.question(self, 'Message',
                                         quit_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                return 0
        return 1
