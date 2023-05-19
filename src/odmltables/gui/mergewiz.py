# -*- coding: utf-8 -*-

import argparse
import sys

from PyQt5.QtWidgets import QApplication

from .mergepages import (LoadFilePage)
from .settings import Settings
from .wizutils import OdmltablesWizard


class MergeWizard(OdmltablesWizard):
    NUM_PAGES = 1

    (PageLoadFile) = 1

    def __init__(self, parent=None, filename=None):
        super(MergeWizard, self).__init__('Merge Wizard', parent)
        settings = Settings(self.settingsfile)

        if isinstance(filename, str):
            filenames = [filename]
        else:
            filenames = filename
        self.setPage(self.PageLoadFile, LoadFilePage(settings, filenames))

    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageLoadFile] = self.tr("Select two input files using the "
                                          "browser and choose your output "
                                          "file format.")
        msgs[self.NUM_PAGES + 1] = self.tr("Sorry, for this page there is no "
                                           "help available.")
        return msgs


# main ========================================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", type=str, nargs='+',
                        help="odml files to load")
    args = parser.parse_args()
    app = QApplication(sys.argv)
    wiz = MergeWizard(filenames=args.files)
    wiz.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
