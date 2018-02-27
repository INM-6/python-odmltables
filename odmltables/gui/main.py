# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:57:16 2016

@author: zehl
"""

import argparse
import sys

from PyQt5 import QtWidgets

from odmltables import VERSION
from .mainwindow import MainWindow
from .compsectionwiz import CompSectionWizard
from .converterwiz import ConversionWizard
from .filterwiz import FilterWizard
from .generatetemplatewiz import GenerateTemplateWizard
from .mergewiz import MergeWizard

wizards = {'compare': CompSectionWizard,
           'filter': FilterWizard,
           'template': GenerateTemplateWizard,
           'merge': MergeWizard,
           'convert': ConversionWizard}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wizard", type=str, choices=list(wizards),
                        help="select odmltables wizard")
    parser.add_argument("-f", "--file", type=str, nargs="+",
                        help="one or multiple files to load")
    parser.add_argument("--version", action="version",
                        version=("odMLTables %s" % VERSION), help="odMLTables version")

    args = parser.parse_args()
    if not args.wizard and args.file:
        parser.error('--file can only be set when --wizard is set.')
    run(wizard=args.wizard, filenames=args.file)


def run(wizard=None, filenames=None):
    app = QtWidgets.QApplication(sys.argv)
    if wizard is None:
        w = MainWindow()
        sys.exit(app.exec_())
    else:
        wiz = wizards[wizard]
        w = wiz(filename=filenames)
        w.exec_()


if __name__ == '__main__':
    parse_args()
