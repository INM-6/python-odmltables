# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:58:23 2016

@author: zehl
"""

import os
from PyQt4.QtGui import (QApplication, QWizard, QPixmap, QMessageBox)
from PyQt4.QtCore import (pyqtSlot)

from wizard.pages import (LoadFilePage,CustomInputHeaderPage,HeaderOrderPage,CustomColumnNamesPage,
                          ColorPatternPage,ChangeStyleOverviewPage,SaveFilePage)
from wizard.pages import Settings
class odml2tableWizard(QWizard):
    NUM_PAGES = 7

    (PageLoadFile, PageCustomInputHeader,PageHeaderOrder, PageCustomColumNames,
     PageColorPattern,PageChangeStyleOverview,PageSaveFile) = range(NUM_PAGES)

    settings = {}

    settingsfile = 'odmlconverter.conf'

    def __init__(self, parent=None):
        super(odml2tableWizard, self).__init__(parent)
        settings = Settings(self.settingsfile)

        self.setPage(self.PageLoadFile, LoadFilePage(settings))
        self.setPage(self.PageCustomInputHeader, CustomInputHeaderPage(settings))
        self.setPage(self.PageHeaderOrder, HeaderOrderPage(settings))
        self.setPage(self.PageCustomColumNames, CustomColumnNamesPage(settings))
        # self.setPage(self.PageColumnMarking, ColumnMarkingPage(settings))
        self.setPage(self.PageColorPattern, ColorPatternPage(settings))
        self.setPage(self.PageChangeStyleOverview, ChangeStyleOverviewPage(settings))
        self.setPage(self.PageSaveFile, SaveFilePage(settings))

        # # initialize settings
        # for pageid in self.pageIds():
        #     page = self.page(pageid)
        #     self.settings[page.__class__.split('.')[-1]] = {}
        #
        # # Saving settings
        # self.settings = dict(zip(range(self.NUM_PAGES),[{}]*self.NUM_PAGES))

        self.setStartId(self.PageLoadFile)
        # self.setStartId(self.PageChangeStyleOverview)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        self.setPixmap(QWizard.LogoPixmap, QPixmap("/images/logo.png"))

        # set up help messages
        self._lastHelpMsg = ''
        self._helpMsgs = self._createHelpMsgs()
        self.helpRequested.connect(self._showHelp)

        self.setWindowTitle(self.tr("conversion wizard"))


    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageLoadFile] = self.tr("Select an input file using the browser"
                                          " and choose your output file format.")
        msgs[self.PageCustomInputHeader] = self.tr("You need to assign the header "
                                                   " titles used in the input file "
                                                   " to valid odml column types.")
        msgs[self.PageHeaderOrder] = self.tr("Select the headers you want be"
                                             " present in the output table. "
                                             " You need to select at least "
                                             " 'Path to Section', 'Property Name',"
                                             " 'Value' and 'odML Data Type' to be"
                                             " able to convert the table back into "
                                             " an odml file.")
        # msgs[self.PageIntro] = self.tr(
        #     "The decision you make here will affect which page you "
        #     "get to see next.")
        # msgs[self.PageEvaluate] = self.tr(
        #     "Make sure to provide a valid email address, such as "
        #     "toni.buddenbrook@example.de.")
        # msgs[self.PageRegister] = self.tr(
        #     "If you don't provide an upgrade key, you will be "
        #     "asked to fill in your details.")
        # msgs[self.PageDetails] = self.tr(
        #     "Make sure to provide a valid email address, such as "
        #     "thomas.gradgrind@example.co.uk.")
        # msgs[self.PageConclusion] = self.tr(
        #     "You must accept the terms and conditions of the "
        #     "license to proceed.")
        msgs[self.NUM_PAGES + 1] = self.tr("Sorry, I already gave what help I could. "
                          "\nMaybe you should try asking a human?")
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

    def convert(self): #TODO: Actual odml<=> tables conversion depending on user settings
        params = get_wizard_parameters(self)
        convertodml2table(**params)


def get_wizard_parameters(wiz):
    raise NotImplementedError()
    return params

def convertodml2table(input_file,output_file,**kwargs):
    raise NotImplementedError()



# main ========================================================================
def main():
    import sys

    app = QApplication(sys.argv)
    wiz = odml2tableWizard()
    wiz.show()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

