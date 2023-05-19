# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:58:23 2016

@author: zehl
"""

import argparse
import sys

from PyQt5.QtWidgets import QApplication

from .filterpages import (LoadFilePage, CustomInputHeaderPage, FilterPage,
                          SaveFilePage)
from .settings import Settings
from .wizutils import OdmltablesWizard


class FilterWizard(OdmltablesWizard):
    NUM_PAGES = 4

    (PageLoadFile, PageCustomInputHeader, PageFilter, PageSaveFile) = list(range(NUM_PAGES))

    def __init__(self, parent=None, filename=None):
        super(FilterWizard, self).__init__('Filter Wizard', parent)
        settings = Settings(self.settingsfile)

        if isinstance(filename, list):
            filename = filename[0]
        self.setPage(self.PageLoadFile, LoadFilePage(settings, filename))
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, nargs=1,
                        help="odml file to load")
    args = parser.parse_args()
    app = QApplication(sys.argv)
    wiz = FilterWizard(filename=args.file)
    wiz.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
