# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import (QWizard, QPixmap, QMessageBox)
from PyQt4.QtCore import (pyqtSlot)

try:
    import odmltables

    have_odmltables = True
except:
    have_odmltables = False

from settings import Settings


class OdmltablesWizard(QWizard):
    def __init__(self, wizname, parent=None):
        super(OdmltablesWizard, self).__init__(parent)

        self.wizname = wizname
        self.settingsfile = wizname.replace(' ', '').lower() + '.conf'

        # initialize settings
        self.settings = Settings(self.settingsfile)

        # setting starting page of wizard
        # self.setStartId(0)

        self.setOption(self.IndependentPages, False)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        self.setPixmap(QWizard.LogoPixmap,
                       QPixmap(os.path.join('..', '..', 'logo',
                                            "odML-tables_100x100.png")))
        # self.setPixmap(QWizard.WatermarkPixmap, QPixmap(os.path.join('..',
        # 'logo',"odML-tables_100x100.png")))

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

        QMessageBox.information(self,
                                self.tr(self.wizname),
                                msg)
        self._lastHelpMsg = msg


def get_graphic_path():
    if have_odmltables:
        data_path = os.path.join(os.path.dirname(odmltables.__file__),
                                 'wizard',
                                 'graphics')
    return data_path

