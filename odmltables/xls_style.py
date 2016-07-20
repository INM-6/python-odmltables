# -*- coding: utf-8 -*-
"""

"""


class XlsStyle():
    """
    class to create a stylestring to use in xlwt.easyxf


    :param backcolor: color of the background of the cell
    :param fontcolor: color of the text inside the cell
    :param fontstyle: style of the text inside the cell ('bold 1' or '')
    :type backcolor: string
    :type fontcolor: string
    :type fontstyle: string

    """

    def __init__(self, backcolor='black', fontcolor='white', fontstyle='bold'):
        self.backcolor = backcolor
        self.fontcolor = fontcolor
        self.fontstyle = fontstyle

    def get_style_string(self):
        """
        returns a style_string that can be used to create a cell-style with
        xlwt.easyxf
        """
        s = ("font: {0} , color {1}; pattern: pattern solid," +
             " fore_colour {2};").format(self.fontstyle, self.fontcolor,
                                         self.backcolor)

        return s
