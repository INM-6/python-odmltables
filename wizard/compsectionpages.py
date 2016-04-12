# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 09:31:26 2016

@author: pick
"""

from pageutils import QIWizardPage, shorten_path
from PyQt4.QtGui import (QVBoxLayout, QHBoxLayout, QMessageBox,
                         QLineEdit, QPushButton, QLabel, QGroupBox,
                         QGridLayout, QTreeWidget, QTreeWidgetItem,
                         QToolButton, QFileDialog, QCheckBox, QComboBox,
                         QFrame, QSizePolicy, QRadioButton)

from PyQt4.QtCore import Qt
import odml
import odmltables.compare_section_csv_table
import odmltables.compare_section_xls_table

class ChooseFilePage(QIWizardPage):
    """
    """

    def __init__(self, parent=None):
        super(ChooseFilePage, self).__init__(parent)
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
        self.inputfilename = ''
        self.inputfile = QLabel(self.inputfilename)
        self.inputfile.setWordWrap(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.buttonbrowse)
        hbox1.addWidget(self.inputfile)
        hbox1.addStretch()
        vbox.addLayout(hbox1)

        # adding configuration selection
        configlabel = QLabel('Load a configuration from a previous run')
        vbox.addWidget(configlabel)
        self.configselection = QComboBox()
        self.configselection.addItems(self.settings.get_all_config_names())
        self.configselection.insertItem(0,'-- No configuration --')
        self.configselection.setCurrentIndex(0)
        self.configselection.activated.connect(self.selectconfig)
        vbox.addWidget(self.configselection)

        # adding separator
        horizontalLine = QFrame()
        horizontalLine.setFrameStyle(QFrame.HLine)
        horizontalLine.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        vbox.addSpacing(10)
        vbox.addWidget(horizontalLine)
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
        self.setSubTitle("Select the file you want to convert and specify the output format you want to generate")

        self.settings.register('RBoutputxls', self.rbuttonxls)
        self.settings.register('RBoutputcsv', self.rbuttoncsv)

    def handlebuttonbrowse(self):
        # only allow .odml-files
        filename = QFileDialog().getOpenFileName(filter="*.odml")
        self.inputpath = QLineEdit(filename)
        self.settings.register('inputfile', self.inputpath)
        self.inputfile.setText(shorten_path(filename))

    def selectconfig(self):
        if self.configselection.currentIndex() != 0:
            self.settings.load_config(str(self.configselection.currentText()))

            # loading output format choice
            self.settings.register('RBoutputxls', self.rbuttonxls)
            self.settings.register('RBoutputcsv', self.rbuttoncsv)
            self.settings.register('CBcustominput', self.cbcustominput)
            self.settings.register('inputfilename', self, useconfig=False)
            short_filename = shorten_path(self.settings.get_object('inputfilename'))
            self.inputfile.setText(short_filename)
            # self.settings.get_object('RBoutputxls')

    def validatePage(self):
        if not any((self.settings.get_object('RBoutputxls').isChecked(),
                    self.settings.get_object('RBoutputcsv').isChecked())):
            QMessageBox.warning(self,'Select a format','You need to select a table format to continue.')
            return 0

        if not self.settings.is_registered('inputfile'):
            QMessageBox.warning(self,'Select an input file','You need to select an input file to continue.')
            return 0
        elif not self.settings.get_object('inputfile').text():
                QMessageBox.warning(self,'Select an input file','You need to select an input file to continue.')
                return 0

        return 1


class ChooseSectionsPage(QIWizardPage):
    """
    page to choose the sections that should be compared in the table
    """

    def __init__(self, parent=None):
        super(ChooseSectionsPage, self).__init__(parent)
        self.selected_sections = []   # sections in the right tree
        self.sections = []            # all sections without the selected
        self.filtered_sections = []   # filtered sections without the selected
        self.initUI()

    def initUI(self):

        mainlayout = QVBoxLayout()

        # layout containing the treewidgets
        sectionlistlayout = QHBoxLayout()

        # layout for filter form
        filterbox = QGroupBox("Filter")

        secname = QLineEdit()
        sectype = QLineEdit()
        propname = QLineEdit()

        filterlayout = QGridLayout()
        filterlayout.addWidget(QLabel("Section Name"), 1, 0)
        filterlayout.addWidget(QLabel("Section Type"), 2, 0)
        filterlayout.addWidget(QLabel("Property Name"), 3, 0)
        filterlayout.addWidget(secname, 1, 1)
        filterlayout.addWidget(sectype, 2, 1)
        filterlayout.addWidget(propname, 3, 1)
        filterbox.setLayout(filterlayout)

        secname.textChanged.connect(self.filterSections)
        sectype.textChanged.connect(self.filterSections)
        propname.textChanged.connect(self.filterSections)

        self.registerField("secname", secname)
        self.registerField("sectype", sectype)
        self.registerField("propname", propname)

        # define layout for the trre-widgets containing the sections
        self.section_tree = QTreeWidget()
        self.section_tree.setColumnCount(2)
        self.section_tree.setHeaderLabels(["Name", "Path"])

        self.selection_tree = QTreeWidget()
        self.selection_tree.setColumnCount(2)
        self.selection_tree.setHeaderLabels(["Name", "Path"])

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
        self.selectallcb = QCheckBox('select all')
        self.selectallcb.stateChanged.connect(self.selectall)
        mainlayout.addWidget(self.selectallcb)
        mainlayout.addWidget(filterbox)

        self.setTitle("Select Sections")
        self.setLayout(mainlayout)
        self.adjustSize()

    def initializePage(self):

        # load sections and properties from the selected file
        odmldoc = odml.tools.xmlparser.load(self.settings.get_object("inputfile").text())
        for section in odmldoc.itersections():
            self.sections.append([section.name,
                                  section.get_path(),
                                  [p.name for p in section.properties],
                                  section.type])

        # fill tree widget with sections and properties
        for line in self.sections:
            parent = QTreeWidgetItem([line[0], line[1]])
            for p in line[2]:
                QTreeWidgetItem(parent, [p])
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
            self.selection_tree.addTopLevelItem(self.section_tree.takeTopLevelItem(row))
            self.selected_sections.append(self.sections.pop(self.sections.index(self.filtered_sections[row])))
            self.filtered_sections.pop(row)

    def toleft(self):
        """
        function to shift items from the right TreeWidget to the left
        """

        rows = self._get_selected_rows(self.selection_tree)
        for row in rows:
            self.section_tree.addTopLevelItem(self.selection_tree.takeTopLevelItem(row))
            item = self.selected_sections.pop(row)
            self.sections.append(item)
            self.filtered_sections.append(item)

    def filterSections(self):

        # find sections that match the filter
        self.filtered_sections = [s for s in self.sections
                                  if self.field("secname") in s[0]
                                  and self.field("sectype") in s[3]
                                  and any([self.field("propname")
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
            self.section_tree.selectAll();
        else:
            self.section_tree.clearSelection();

    def validatePage(self):
        if not self.settings.get_object("selected_secs"):
            QMessageBox.warning(self,'No Sections chosen','You should choose at least two sections to be compared in the table.')
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
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.buttonbrowse = QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.outputfile = QLabel()

        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonbrowse)
        hbox.addWidget(self.outputfile)

        layout.addLayout(hbox)

        self.setLayout(layout)

    def initializePage(self):
        self.setTitle("Save Table")
        self.setSubTitle("Choose a location to save your table")


    def handlebuttonbrowse(self):
        # only allow .odml-files
        filename = QFileDialog().getSaveFileName()
        self.outputpath = QLineEdit(filename)
        self.settings.register('outputfile', self.outputpath)
        self.outputfile.setText(filename)

    def _saveXlsTable(self):
        table = odmltables.compare_section_xls_table.CompareSectionXlsTable()
        table.load_from_file(self.settings.get_object("inputfile").text())
        selections = [s[0] for s in self.settings.get_object("selected_secs")]
        table.choose_sections(*selections)
        table.write2file(self.settings.get_object("outputfile").text())

    def _saveCsvTable(self):
        table = odmltables.compare_section_csv_table.CompareSectionCsvTable()
        table.load_from_file(self.settings.get_object("inputfile").text())
        selections = [s[0] for s in self.settings.get_object("selected_secs")]
        table.choose_sections(*selections)
        table.write2file(self.settings.get_object("outputfile").text())

    def validatePage(self):

        if not self.settings.get_object('outputfile').text():
            QMessageBox.warning(self,'Select an outputfile','You need to select a outputfile to continue.')
            return 0

        if self.settings.get_object('RBoutputxls').isChecked():
            self._saveXlsTable()
        elif self.settings.get_object('RBoutputcsv').isChecked():
            self._saveCsvTable()
        else:
            return 0

        return 1

#
