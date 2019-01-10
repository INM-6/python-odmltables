# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QApplication)

from .generatetemplatepages import HeaderOrderPage, SaveFilePage
from .wizutils import OdmltablesWizard


class GenerateTemplateWizard(OdmltablesWizard):
    NUM_PAGES = 2

    (PageHeaderOrder, PageSaveFile) = list(range(NUM_PAGES))

    def __init__(self, parent=None, filename=None):
        super(GenerateTemplateWizard, self).__init__('Generate Template Wizard',
                                                     parent)

        self.setPage(self.PageHeaderOrder, HeaderOrderPage(self.settings))
        self.setPage(self.PageSaveFile, SaveFilePage(self.settings))

    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageHeaderOrder] = self.tr("Select the headers you want be"
                                             " present in the output table. "
                                             " You need to select at least "
                                             " 'Path to Section', 'Property "
                                             "Name',"
                                             " 'Value' and 'odML Data Type' "
                                             "to be"
                                             " able to convert the table back "
                                             "into "
                                             " an odml file.")
        msgs[self.PageSaveFile] = self.tr(
            "Select a location to save you file by "
            "clicking on the browse button.")
        msgs[self.NUM_PAGES + 1] = self.tr(
            "Sorry, for this page there is no help available.")
        return msgs


# main ========================================================================
def main():
    import sys

    app = QApplication(sys.argv)
    wiz = GenerateTemplateWizard()
    wiz.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
