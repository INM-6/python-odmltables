
from PyQt4.QtGui import QWizardPage

class QIWizardPage(QWizardPage):
    def __init__(self,settings,parent=None):
        super(QIWizardPage,self).__init__(parent)
        self.settings = settings