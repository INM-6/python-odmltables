# -*- coding: utf-8 -*-

import os, sys
from PyQt5.QtWidgets import (QWizard, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt

try:
    import odmltables

    have_odmltables = True
except:
    have_odmltables = False

from .settings import Settings


class OdmltablesWizard(QWizard):
    def __init__(self, wizname, parent=None):
        super(OdmltablesWizard, self).__init__(parent)

        self.wizname = wizname
        self.settingsfile = os.path.join(os.path.expanduser("~"),
                                         '.odmltables',
                                         wizname.replace(' ', '').lower() + '.conf')

        # initialize settings
        self.settings = Settings(self.settingsfile)

        # setting starting page of wizard
        # self.setStartId(0)

        self.setOption(self.IndependentPages, False)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        logo_filename = "odMLtables_100x100.png"
        logo_dirs = [os.path.join(os.path.dirname(__file__), '..', '..', 'logo'),
                     os.path.join(sys.prefix, 'share/pixmaps')]
        for logo_dir in logo_dirs:
            filepath = os.path.join(logo_dir, logo_filename)
            if os.path.exists(filepath):
                self.setPixmap(QWizard.LogoPixmap, QPixmap(filepath))

        # set up help messages
        self._lastHelpMsg = ''
        self._helpMsgs = self._createHelpMsgs()
        self.helpRequested.connect(self._showHelp)

        self.setWindowTitle(self.tr(wizname))

    def _createHelpMsgs(self):
        raise NotImplementedError()

    @pyqtSlot()
    def _showHelp(self):
        # get the help message for the current page
        msg = self._helpMsgs[self.currentId()]
        # # if same as last message, display alternate message
        # if msg == self._lastHelpMsg:
        #     msg = self._helpMsgs[self.NUM_PAGES + 1]

        doc_link = "<p>For detailed information about odMLtables refer to the " \
                   "<a href='http://pythonhosted.org/python-odmltables'>odMLtables " \
                   "documentation</a>.</p>"

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Help")
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setText(msg + doc_link)
        msgBox.exec_()

        # QMessageBox.information(self,
        #                         self.tr(self.wizname),
        #                         msg)
        # self._lastHelpMsg = msg


def get_graphic_path():
    if have_odmltables:
        data_path = os.path.join(os.path.dirname(odmltables.__file__),
                                 'gui',
                                 'graphics')
    return data_path
