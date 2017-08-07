# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:58:23 2016

@author: zehl
"""

import os
from PyQt4.QtGui import QApplication

from filterpages import (LoadFilePage, CustomInputHeaderPage, FilterPage,
                         SaveFilePage)
from wizutils import OdmltablesWizard

from settings import Settings


class FilterWizard(OdmltablesWizard):
    NUM_PAGES = 4

    (PageLoadFile, PageCustomInputHeader, PageFilter, PageSaveFile) = range(
            NUM_PAGES)

    def __init__(self, parent=None):
        super(FilterWizard, self).__init__('Filter Wizard', parent)
        settings = Settings(self.settingsfile)

        self.setPage(self.PageLoadFile, LoadFilePage(settings))
        self.setPage(self.PageCustomInputHeader,
                     CustomInputHeaderPage(settings))
        self.setPage(self.PageFilter, FilterPage(settings))
        self.setPage(self.PageSaveFile, SaveFilePage(settings))

        self.setStartId(0)

    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageLoadFile] = self.tr(
                "Select an input file using the browser"
                " and choose your output file format.")
        msgs[self.PageCustomInputHeader] = self.tr(
                "You need to assign the header "
                " titles used in the input file "
                " to valid odml column types.")

        # TODO: Add more help info
        msgs[self.NUM_PAGES + 1] = self.tr(
                "Sorry, for this page there is no help available.")
        return msgs


# main ========================================================================
def main():
    import sys

    app = QApplication(sys.argv)
    wiz = FilterWizard()
    wiz.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
