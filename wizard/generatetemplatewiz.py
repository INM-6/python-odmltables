# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import (QApplication, QWizard, QPixmap, QMessageBox)
from PyQt4.QtCore import (pyqtSlot)

from generatetemplatepages import HeaderOrderPage,SaveFilePage
from settings import Settings
class GenerateTemplateWizard(QWizard):
    NUM_PAGES = 2

    (PageHeaderOrder,PageSaveFile) = range(NUM_PAGES)

    settings = {}

    settingsfile = 'generatetemplate.conf'

    def __init__(self, parent=None):
        super(GenerateTemplateWizard, self).__init__(parent)
        settings = Settings(self.settingsfile)

        self.setPage(self.PageHeaderOrder, HeaderOrderPage(settings))
        self.setPage(self.PageSaveFile, SaveFilePage(settings))

        # setting starting page of wizard
        self.setStartId(self.PageHeaderOrder)


        self.setOption(self.IndependentPages, False)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        self.setPixmap(QWizard.LogoPixmap, QPixmap("../logos/odML-tables.png"))

        # set up help messages
        self._lastHelpMsg = ''
        self._helpMsgs = self._createHelpMsgs()
        self.helpRequested.connect(self._showHelp)

        self.setWindowTitle(self.tr("generate template wizard"))


    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageHeaderOrder] = self.tr("Select the headers you want be"
                                             " present in the output table. "
                                             " You need to select at least "
                                             " 'Path to Section', 'Property Name',"
                                             " 'Value' and 'odML Data Type' to be"
                                             " able to convert the table back into "
                                             " an odml file.")
        msgs[self.PageSaveFile] = self.tr("Select a location to save you file by "
                                          "clicking on the browse button.")
        msgs[self.NUM_PAGES + 1] = self.tr("Sorry, for this page there is no help available.")
        return msgs

    @pyqtSlot()
    def _showHelp(self):
        # get the help message for the current page
        msg = self._helpMsgs[self.currentId()]

        # if same as last message, display alternate message
        if msg == self._lastHelpMsg:
            msg = self._helpMsgs[self.NUM_PAGES + 1]

        QMessageBox.information(self,
                                self.tr("Conversion Wizard Help"),
                                msg)
        self._lastHelpMsg = msg

# main ========================================================================
def main():
    import sys

    app = QApplication(sys.argv)
    wiz = GenerateTemplateWizard()
    wiz.show()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

