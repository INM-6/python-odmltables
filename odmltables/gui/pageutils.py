# -*- coding: utf-8 -*-

import os
import re
import xlwt

from PyQt5.QtWidgets import QWizardPage, QWidgetItem, QSpacerItem, QComboBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class QIWizardPage(QWizardPage):
    def __init__(self, settings, parent=None):
        super(QIWizardPage, self).__init__(parent)
        self.settings = settings


def clearLayout(layout):
    for i in reversed(list(range(layout.count()))):
        item = layout.itemAt(i)

        if isinstance(item, QWidgetItem):
            # print("widget" + str(item))
            item.widget().close()
            # or
            # item.widget().setParent(None)
        elif isinstance(item, QSpacerItem):
            pass
            # print("spacer " + str(item))
            # no need to do extra stuff
        else:
            # print("layout " + str(item))
            clearLayout(item.layout())

        # remove the item from layout
        layout.removeItem(item)


class ColorListWidget(QComboBox):
    _xlwt_rgbcolors = [
        (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (0, 0, 0), (255, 255, 255), (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0),
        (0, 128, 0),
        (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
        (192, 192, 192),
        (128, 128, 128), (153, 153, 255), (153, 51, 102), (255, 255, 204),
        (204, 255, 255), (102, 0, 102), (255, 128, 128), (0, 102, 204),
        (204, 204, 255),
        (0, 0, 128), (255, 0, 255), (255, 255, 0), (0, 255, 255), (128, 0, 128),
        (128, 0, 0), (0, 128, 128), (0, 0, 255), (0, 204, 255), (204, 255, 255),
        (204, 255, 204), (255, 255, 153), (153, 204, 255), (255, 153, 204),
        (204, 153, 255), (255, 204, 153), (51, 102, 255), (51, 204, 204),
        (153, 204, 0),
        (255, 204, 0), (255, 153, 0), (255, 102, 0), (102, 102, 153),
        (150, 150, 150),
        (0, 51, 102), (51, 153, 102), (0, 51, 0), (51, 51, 0), (153, 51, 0),
        (153, 51, 102),
        (51, 51, 153), (51, 51, 51)
    ]

    def __init__(self):
        super(ColorListWidget, self).__init__()
        cmap = xlwt.Style.colour_map
        self.xlwt_colornames = []
        self.xlwt_color_index = []
        self.xlwt_rgbcolors = []
        # self._xlwt_colorlabels = []
        for i in list(range(64)):
            cnames = [name for (name, index) in list(cmap.items()) if index == i]
            # self._xlwt_colorlabels.append(cnames[0] if len(cnames)>0 else '')
            if cnames != []:
                self.xlwt_colornames.append(', '.join(cnames))
                self.xlwt_color_index.append(i)
                self.xlwt_rgbcolors.append(self._xlwt_rgbcolors[i])

        for i, xlwtcolor in enumerate(self.xlwt_colornames):
            self.insertItem(i, xlwtcolor)
            self.setItemData(i, QColor(*self.xlwt_rgbcolors[i]),
                             Qt.DecorationRole)

    def get_current_rgb(self):
        return self.xlwt_rgbcolors[self.currentIndex()]


#######################################################
# Supplementory functions

def shorten_path(path):
    sep = os.path.sep
    if path.count(sep) > 2:
        id = path.rfind(sep)
        id = path.rfind(sep, 0, id)
    else:
        id = 0
    if path == '':
        return path
    else:
        return "...%s" % (path[id:])


def get_property(style, property):
    styles = [str(s) for s in style.split(';')]
    for s in styles:
        if s.strip(' ').startswith(property + ':'):
            return s.replace(property + ':', '')

    return ''


def get_rgb(style_string):
    rgbregex = re.compile(
        " *rgb\( {0,2}(?P<r>\d{1,3}), {0,2}(?P<g>\d{1,3}), {0,2}(?P<b>\d{"
        "1,3})\) *")
    match = rgbregex.match(style_string)
    if match:
        groups = match.groupdict()
        return tuple([int(groups['r']), int(groups['g']), int(groups['b'])])
    else:
        raise ValueError(
            'No rgb identification possible from "%s"' % style_string)
