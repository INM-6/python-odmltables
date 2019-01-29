# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:57:46 2016

@author: zehl
"""

import datetime
import os
import sys
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui

# import wizards
from .compsectionwiz import CompSectionWizard
from .converterwiz import ConversionWizard
from .filterwiz import FilterWizard
from .generatetemplatewiz import GenerateTemplateWizard
from .mergewiz import MergeWizard
from .wizutils import get_graphic_path

from odmltables import VERSION


def handle_exception(exc_type, exc_value, exc_traceback):
    """ handle all exceptions """

    error_logfile = os.path.join(os.path.expanduser("~"),
                                 '.odmltables',
                                 'error.log')

    ## KeyboardInterrupt is a special case.
    ## We don't raise the error dialog when it occurs.
    if issubclass(exc_type, KeyboardInterrupt):
        if QtWidgets.qApp:
            QtWidgets.qApp.quit()
        return

    filename, lineid, func, line = traceback.extract_tb(exc_traceback).pop()
    filename = os.path.basename(filename)
    error = "%s: %s" % (exc_type.__name__, exc_value)
    complete_error = "".join(traceback.format_exception(exc_type,
                                                        exc_value,
                                                        exc_traceback))

    msg_text = ("<html><b>%s</b><br><br>"
                "Please check your odMLtables settings and inputfiles for "
                "consistency. In case you found a bug in odMLtables please "
                "contact the odMLtables team "
                "<i>https://github.com/INM-6/python-odmltables/issues</i>."
                "<br><br>"
                "For a detailed error report see log file at <i>%s</i>"
                "</html>" % (
                    error.replace('<', '').replace('>', ''), error_logfile))

    QtWidgets.QMessageBox.critical(None,
                               "Unexpected Error in odMLtables",
                               msg_text)

    print("An error occurred. This is the full error report:")
    print()
    print(complete_error)

    now = str(datetime.datetime.now())
    errorpath = os.path.dirname(error_logfile)
    if not os.path.exists(errorpath):
        os.makedirs(errorpath)
    with open(error_logfile, "a+") as myfile:
        myfile.writelines(['################### %s ###################\n' % now,
                           complete_error, '\n'])

        # sys.exit(1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

        # install handler for exceptions
        sys.excepthook = handle_exception

    def initUI(self):

        centralWidget = QtWidgets.QWidget()
        w, h = 450, 450
        self.setFixedSize(w, h)
        self.setCentralWidget(centralWidget)

        # background color
        centralWidget.setAutoFillBackground(True)
        p = centralWidget.palette()
        gradient = QtGui.QRadialGradient(w / 2, h / 3, h / 1, w / 2, h)
        # gradient = QtGui.QRadialGradient(w / 2, h / 2, h / 1, w / 2, h)
        gradient.setColorAt(0.0, QtGui.QColor(240, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(0, 76, 153))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        # p.setColor(centralWidget.backgroundRole(),QtGui.QColor(153,204,255))
        # (255,128,0) # for button background
        centralWidget.setPalette(p)

        vbox = QtWidgets.QVBoxLayout()

        titlebox = QtWidgets.QHBoxLayout()
        vbox.addLayout(titlebox)

        subtitlebox = QtWidgets.QVBoxLayout()
        titlebox.addLayout(subtitlebox)
        subtitlebox.addSpacing(8)

        title_font = QtGui.QFont()
        # title_font.setFamily("Verdana")
        title_font.setBold(True)
        title_font.setPointSize(14)
        label = QtWidgets.QLabel("odMLtables version {}".format(VERSION))
        label.setFont(title_font)
        pal = QtGui.QPalette(label.palette())
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(QtCore.Qt.black))
        label.setPalette(pal)
        subtitlebox.addWidget(label)

        subtitlebox.addSpacing(5)

        subtitle = QtWidgets.QLabel('Select one of the actions below')
        subtitle.setPalette(pal)
        subtitlebox.addWidget(subtitle)
        # subtitlebox.addSpacing(10)

        grid = QtWidgets.QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        vbox.addLayout(grid)

        self.convertbutton = self.generate_button('Convert between odml\nand '
                                                  'table format',
                                                  "convertodml.svg")
        self.comparebutton = self.generate_button('Compare entries within\nan '
                                                  'odml',
                                                  "comparetable.svg")
        self.generatebutton = self.generate_button('Generate new table',
                                                   "createtemplate.svg")
        self.filterbutton = self.generate_button('Filter content of odml\n',
                                                 "filterodml.svg")
        self.mergebutton = self.generate_button('Merge contents of odmls\n',
                                                "mergeodml.svg")

        icon = QtWidgets.QLabel()
        # icon.setGeometry(10, 10, 4, 100)
        logo_filename = "odMLtables_100x100.png"
        logo_dirs = [os.path.join(os.path.dirname(__file__), '..', '..', 'logo'),
                     os.path.join(sys.prefix, 'share/pixmaps')]
        for logo_dir in logo_dirs:
            filepath = os.path.join(logo_dir, logo_filename)
            if os.path.exists(filepath):
                icon.setPixmap(QtGui.QPixmap(filepath))


        grid.addWidget(self.convertbutton, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.comparebutton, 1, 1)
        grid.addWidget(self.generatebutton, 1, 0)
        grid.addWidget(self.filterbutton, 2, 1)
        grid.addWidget(self.mergebutton, 2, 0)
        titlebox.addWidget(icon)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('odMLtables')
        centralWidget.setLayout(vbox)
        self.show()

    def generate_button(self, text, graphic_name):
        graphic_path = get_graphic_path()
        button = QtWidgets.QToolButton()
        button.setText(self.tr(text))
        button.setIcon(QtGui.QIcon(os.path.join(graphic_path, graphic_name)))
        button.setIconSize(QtCore.QSize(120, 60))
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        button.setFixedWidth(200)
        button.setFixedHeight(100)
        button.clicked.connect(self.startWizard)

        button.setStyleSheet(
            'QToolButton {'
            'background-color:#FF9955;'
            'border: 2px solid #404040;'
            'border-radius: 5px;'
            'color: black};'  # 'FF7F2A'

            'QToolButton:hover{'
            'background-color:red};'
        )
        return button

    def startWizard(self):
        sender = self.sender()

        if sender == self.convertbutton:
            wizard = ConversionWizard()
        elif sender == self.comparebutton:
            wizard = CompSectionWizard()
        elif sender == self.generatebutton:
            wizard = GenerateTemplateWizard()
        elif sender == self.filterbutton:
            wizard = FilterWizard()
        elif sender == self.mergebutton:
            wizard = MergeWizard()
        else:
            raise EnvironmentError('Unknown sender')

        wizard.exec_()
