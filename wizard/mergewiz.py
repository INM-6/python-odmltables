# -*- coding: utf-8 -*-


from PyQt4.QtGui import QApplication

from mergepages import (LoadFilePage, SaveFilePage)
from wizutils import OdmltablesWizard

from settings import Settings
class MergeWizard(OdmltablesWizard):
    NUM_PAGES = 2

    (PageLoadFile, PageSaveFile) = range(NUM_PAGES)


    def __init__(self, parent=None):
        super(MergeWizard, self).__init__('Merge Wizard',parent)
        settings = Settings(self.settingsfile)

        self.setPage(self.PageLoadFile, LoadFilePage(settings))
        self.setPage(self.PageSaveFile, SaveFilePage(settings))


    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageLoadFile] = self.tr("Select two input files using the "
                                          "browser and choose your output "
                                          "file format.")
        msgs[self.PageSaveFile] = self.tr("Select a location to save your "
                                          "file by clicking on the browse "
                                          "button.")
        msgs[self.NUM_PAGES + 1] = self.tr("Sorry, for this page there is no "
                                           "help available.")
        return msgs

# main ========================================================================
def main():
    import sys

    app = QApplication(sys.argv)
    wiz = MergeWizard()
    wiz.show()


    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

