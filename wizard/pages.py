# -*- coding: utf-8 -*-
"""
pages
=====

Classes to create dialog pages for the wizard interface of python-odmltables.

Classes
-------

WelcomePage        - Class generating the first dialog page, where the user has
                     to decide which odmltable operation he/she wants to
                     perform

LoadodMLPage       - Class generating a dialog page, where the user has to
                     specify the odML file he/she wants to transform into a
                     table and define the corresponding table format

LoadTablePage      - Class generating a dialog page, where the user has to
                     specify the table file he/she wants to transform into an
                     odML file and state if the item names of the table header
                     were modified

HeaderOrderPage    - Class generating a dialog page, where the user has to
                     choose which table header items should be used, can change
                     in which order the table header items are displayed, and
                     state if the item names should be modified

HeaderDefNamesPage - Class generating a dialog page, where the user can modify
                     the names for all chosen header items for the wanted table

HeaderModNamesPage - Class generating a dialog page, where the user has to
                     match the default names of the odML header items to all
                     modified header item names of the loaded table

RedundancyPage     - Class generating a dialog page, where the user can state
                     if and which redundant information should be displayed in
                     the wanted table

MarkColumnPage     - Class generating a dialog page, where the user can decide
                     if and which column of the wanted table should be
                     emphasized compared to the remaining columns

BackPatternPage    - Class generating a dialog page, where the user can decide
                     if and which background pattern type should be used for
                     the wanted table

StylePage          - Class generating a dialog page, where the user can see the
                     style (background color, font style) of the chosen pattern
                     and can decide to change the style for the pattern fields,
                     individually

StyleModPage       - Class generating a dialog page, where the user can change
                     the background colors, the font colors, and the font style
                     for a selected pattern field of the wanted table

SavePage           - Class generating a dialog page, where the user defines the
                     location, and filename of the file that he wants to save


@author: zehl
"""


from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
                         QRadioButton, QVBoxLayout, QLineEdit, QGridLayout,
                         QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
                         QMessageBox)
from PyQt4.QtCore import (pyqtSlot, QRegExp)


class WelcomePage(QWizardPage):
    def __init__(self,parent=None):
        super(WelcomePage,self).__init__(parent)

        self.setTitle(self.tr("Create your table"))
        self.setPixmap(QWizard.WatermarkPixmap,QPixmap(":/graphics/icon.svg"))
        topLable = QLabel(self.tr('Select an output format:'))





class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr("Introduction"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("This Wizard will help you register your copy of "
                                  "<i>Super Product One</i> or start "
                                  "evaluating the product."))
        topLabel.setWordWrap(True)

        regRBtn = QRadioButton(self.tr("&Register your copy"))
        self.evalRBtn = QRadioButton(self.tr("&Evaluate the product for 30 days"))
        regRBtn.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(regRBtn)
        layout.addWidget(self.evalRBtn)
        self.setLayout(layout)

        self.registerField('regRBtn',regRBtn)


    # def nextId(self):
    #     # if self.evalRBtn.isChecked():
    #     #     print 'Current ID %s'%(self.currentId())
    #     return self.currentId() + 1
    #     # else:
    #     #     return 2



class EvaluatePage(QWizardPage):
    def __init__(self, parent=None):
        super(EvaluatePage, self).__init__(parent)

        self.setTitle(self.tr("Evaluate <i>Super Product One</i>"))
        self.setSubTitle(self.tr("Please fill both fields. \nMake sure to provide "
                                 "a valid email address (e.g. john.smith@example.com)"))
        nameLabel = QLabel("Name: ")
        nameEdit = QLineEdit()
        nameLabel.setBuddy(nameEdit)

        emailLabel = QLabel(self.tr("&Email address: "))
        emailEdit = QLineEdit()
        emailEdit.setValidator(QRegExpValidator(
                QRegExp(".*@.*"), self))
        emailLabel.setBuddy(emailEdit)

        self.registerField("evaluate.name*", nameEdit)
        self.registerField("evaluate.email*", emailEdit)

        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(nameEdit, 0, 1)
        grid.addWidget(emailLabel, 1, 0)
        grid.addWidget(emailEdit, 1, 1)
        self.setLayout(grid)

    # def nextId(self):
    #     return odml2tableWizard.PageConclusion

    def validatePage(self):
        print 'validation'
        pass

class RegisterPage(QWizardPage):
    def __init__(self, parent=None):
        super(RegisterPage, self).__init__(parent)

        self.setTitle(self.tr("Register Your Copy of <i>Super Product One</i>"))
        self.setSubTitle(self.tr("If you have an upgrade key, please fill in "
                                 "the appropriate field."))
        nameLabel = QLabel(self.tr("N&ame"))
        nameEdit = QLineEdit()
        nameLabel.setBuddy(nameEdit)

        upgradeKeyLabel = QLabel(self.tr("&Upgrade key"))
        self.upgradeKeyEdit = QLineEdit()
        upgradeKeyLabel.setBuddy(self.upgradeKeyEdit)

        self.registerField("register.name*", nameEdit)
        self.registerField("register.upgradeKey", self.upgradeKeyEdit)

        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(nameEdit, 0, 1)
        grid.addWidget(upgradeKeyLabel, 1, 0)
        grid.addWidget(self.upgradeKeyEdit, 1, 1)

        self.setLayout(grid)

    # def nextId(self):
    #     if len(self.upgradeKeyEdit.text()) > 0 :
    #         return odml2tableWizard.PageConclusion
    #     else:
    #         return odml2tableWizard.PageDetails


class DetailsPage(QWizardPage):
    def __init__(self, parent=None):
        super(DetailsPage, self).__init__(parent)

        self.setTitle(self.tr("Fill in Your Details"))
        self.setSubTitle(self.tr("Please fill all three fields. /n"
                                 "Make sure to provide a valid "
                                 "email address (e.g., tanaka.aya@example.com)."))
        coLabel = QLabel(self.tr("&Company name: "))
        coEdit = QLineEdit()
        coLabel.setBuddy(coEdit)

        emailLabel = QLabel(self.tr("&Email address: "))
        emailEdit = QLineEdit()
        emailEdit.setValidator(QRegExpValidator(QRegExp(".*@.*"), self))
        emailLabel.setBuddy(emailEdit)

        postLabel = QLabel(self.tr("&Postal address: "))
        postEdit = QLineEdit()
        postLabel.setBuddy(postEdit)

        self.registerField("details.company*", coEdit)
        self.registerField("details.email*", emailEdit)
        self.registerField("details.postal*", postEdit)

        grid = QGridLayout()
        grid.addWidget(coLabel, 0, 0)
        grid.addWidget(coEdit, 0, 1)
        grid.addWidget(emailLabel, 1, 0)
        grid.addWidget(emailEdit, 1, 1)
        grid.addWidget(postLabel, 2, 0)
        grid.addWidget(postEdit, 2, 1)
        self.setLayout(grid)

    # def nextId(self):
    #     return odml2tableWizard.PageConclusion

class ConclusionPage(QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle(self.tr("Complete Your Registration"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))

        self.bottomLabel = QLabel()
        self.bottomLabel.setWordWrap(True)

        agreeBox = QCheckBox(self.tr("I agree to the terms of the license."))

        self.registerField("conclusion.agree*", agreeBox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.bottomLabel)
        vbox.addWidget(agreeBox)
        self.setLayout(vbox)

    # def nextId(self):
    #     return -1

    def initializePage(self):
        licenseText = ''

        # if self.wizard().hasVisitedPage(odml2tableWizard.PageEvaluate):
        #     licenseText = self.tr("<u>Evaluation License Agreement:</u> "
        #                   "You can use this software for 30 days and make one "
        #                   "backup, but you are not allowed to distribute it.")
        # elif self.wizard().hasVisitedPage(odml2tableWizard.PageDetails):
        #     licenseText = self.tr("<u>First-Time License Agreement:</u> "
        #                   "You can use this software subject to the license "
        #                   "you will receive by email.")
        # else:
        #     licenseText = self.tr("<u>Upgrade License Agreement:</u> "
        #                   "This software is licensed under the terms of your "
        #                   "current license.")

        licenseText = 'Put License Text here.'

        self.bottomLabel.setText(licenseText)

    def setVisible(self, visible):
        # only show the 'Print' button on the last page
        QWizardPage.setVisible(self, visible)

        if visible:
            self.wizard().setButtonText(QWizard.CustomButton1, self.tr("&Print"))
            self.wizard().setOption(QWizard.HaveCustomButton1, True)
            self.wizard().customButtonClicked.connect(self._printButtonClicked)
            self._configWizBtns(True)
        else:
            # only disconnect if button has been assigned and connected
            btn = self.wizard().button(QWizard.CustomButton1)
            if len(btn.text()) > 0:
                self.wizard().customButtonClicked.disconnect(self._printButtonClicked)

            self.wizard().setOption(QWizard.HaveCustomButton1, False)
            self._configWizBtns(False)

    def _configWizBtns(self, state):
        # position the Print button (CustomButton1) before the Finish button
        if state:
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.CustomButton1, QWizard.FinishButton,
                       QWizard.CancelButton, QWizard.HelpButton]
            self.wizard().setButtonLayout(btnList)
        else:
            # remove it if it's not visible
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.FinishButton,
                       QWizard.CancelButton, QWizard.HelpButton]
            self.wizard().setButtonLayout(btnList)

    @pyqtSlot()
    def _printButtonClicked(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_():
            QMessageBox.warning(self,
                                self.tr("Print License"),
                                self.tr("As an environment friendly measure, the "
                                        "license text will not actually be printed."))