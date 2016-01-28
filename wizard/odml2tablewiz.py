# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:58:23 2016

@author: zehl
"""


from PyQt4.QtGui import (QApplication, QWizard, QPixmap, QMessageBox)
from PyQt4.QtCore import (pyqtSlot)
from wizard.pages import (IntroPage,EvaluatePage,RegisterPage,DetailsPage,
                         ConclusionPage)

class odml2tableWizard(QWizard):
    NUM_PAGES = 5

    (PageIntro, PageEvaluate, PageRegister, PageDetails,
        PageConclusion) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(odml2tableWizard, self).__init__(parent)

        self.setPage(self.PageIntro, IntroPage(self))
        self.setPage(self.PageEvaluate, EvaluatePage())
        self.setPage(self.PageRegister, RegisterPage())
        self.setPage(self.PageDetails, DetailsPage())
        self.setPage(self.PageConclusion, ConclusionPage())

        self.setStartId(self.PageIntro)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/logo.png"))

        # set up help messages
        self._lastHelpMsg = ''
        self._helpMsgs = self._createHelpMsgs()
        self.helpRequested.connect(self._showHelp)

        self.setWindowTitle(self.tr("License Wizard"))

    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageIntro] = self.tr(
            "The decision you make here will affect which page you "
            "get to see next.")
        msgs[self.PageEvaluate] = self.tr(
            "Make sure to provide a valid email address, such as "
            "toni.buddenbrook@example.de.")
        msgs[self.PageRegister] = self.tr(
            "If you don't provide an upgrade key, you will be "
            "asked to fill in your details.")
        msgs[self.PageDetails] = self.tr(
            "Make sure to provide a valid email address, such as "
            "thomas.gradgrind@example.co.uk.")
        msgs[self.PageConclusion] = self.tr(
            "You must accept the terms and conditions of the "
            "license to proceed.")
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
                                self.tr("License Wizard Help"),
                                msg)
        self._lastHelpMsg = msg

    def convert(self):
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

