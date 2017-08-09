# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:57:16 2016

@author: zehl
"""

import argparse
from PyQt4 import QtGui
import sys
from mainwindow import MainWindow
from odmltables.gui.compsectionwiz import CompSectionWizard
from odmltables.gui.filterwiz import FilterWizard
from odmltables.gui.generatetemplatewiz import GenerateTemplateWizard
from odmltables.gui.mergewiz import MergeWizard
from odmltables.gui.converterwiz import ConversionWizard

wizards = {'compare': CompSectionWizard,
           'filter': FilterWizard,
           'template': GenerateTemplateWizard,
           'merge': MergeWizard,
           'convert': ConversionWizard}

def run(wizard=None, filenames=None):
    app = QtGui.QApplication(sys.argv)
    if wizard is None:
        w = MainWindow()
        sys.exit(app.exec_())
    else:
        wiz = wizards[wizard]
        w = wiz(filename=filenames)
        w.exec_()

#TODO: handle filenames in individual wizards


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wizard", type=str, choices=list(wizards),
                        help="select odmltables wizard")
    parser.add_argument("-f", "--file", type=str, nargs="+",
                        help="one or multiple files to load")

    args = parser.parse_args()
    if not args.wizard and args.file:
        parser.error('--file can only be set when --wizard is set.')
    run(wizard=args.wizard, filenames=args.file)
