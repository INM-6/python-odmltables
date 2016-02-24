# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 13:12:21 2016

@author: pick
"""


from PyQt4.QtGui import (QWizard, QWizardPage, QVBoxLayout, QHBoxLayout,
                         QLineEdit, QPushButton, QLabel, QGroupBox,
                         QGridLayout, QTreeWidget, QTreeWidgetItem,
                         QToolButton, QFileDialog)
from PyQt4.QtCore import Qt
import odml
import odmltables.compare_section_csv_table
from settings import Settings
from pageutils import QIWizardPage


class CompSectionWiz(QWizard):

    settings = {}
    settingsfile = 'odmlconverter.conf'

    NUM_PAGES = 3

    (PageChooseFile, PageChooseSections, PageSaveTable) = range(NUM_PAGES)


    def __init__(self):
        super(CompSectionWiz, self).__init__()

        settings = Settings(self.settingsfile)

        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)

        self.setPage(self.PageChooseFile, ChooseFilePage(settings))
        self.setPage(self.PageChooseSections, ChooseSectionsPage(settings))
        self.setPage(self.PageSaveTable, SaveTablePage(settings))

        self.setStartId(self.PageChooseFile)


class ChooseFilePage(QIWizardPage):
    """
    may be replaced by LoadFilePage
    """

    def __init__(self, parent=None):
        super(ChooseFilePage, self).__init__(parent)
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.buttonbrowse = QPushButton("Browse")
        self.buttonbrowse.clicked.connect(self.handlebuttonbrowse)
        self.inputfile = QLabel()

        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonbrowse)
        hbox.addWidget(self.inputfile)

        layout.addLayout(hbox)

        self.setLayout(layout)

    def handlebuttonbrowse(self):
        # only allow .odml-files
        filename = QFileDialog().getOpenFileName(filter="*.odml")
        self.inputpath = QLineEdit(filename)
        self.registerField('inputfile', self.inputpath)
        self.inputfile.setText(filename)




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
        sectionlistlayout = QHBoxLayout()


        # define layout for filter form
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
        mainlayout.addWidget(filterbox)

        self.setTitle("Select Sections")
        self.setLayout(mainlayout)
        self.adjustSize()

    def initializePage(self):

        # load sections and properties from the selected file
        odmldoc = odml.tools.xmlparser.load(self.field("inputfile"))
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


class ChoosePropertiesPage(QIWizardPage):

    def __init__(self, parent=None):
        super(ChoosePropertiesPage, self).__init__(parent)


class ChooseStylesPage(QWizardPage):

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

    def handlebuttonbrowse(self):
        # only allow .odml-files
        filename = QFileDialog().getSaveFileName()
        self.outputpath = QLineEdit(filename)
        self.registerField('outputfile', self.outputpath)
        self.outputfile.setText(filename)

    def validatePage(self):

        table = odmltables.compare_section_csv_table.CompareSectionCsvTable()
        table.load_from_file(self.field("inputfile"))
        selections = [s[0] for s in self.settings.get_object("selected_secs")]
        table.choose_sections(*selections)
        table.write2file(self.field("outputfile"))
        return 1



