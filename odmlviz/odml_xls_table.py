# -*- coding: utf-8 -*-
"""
Created on Mon May  4 08:39:42 2015

@author: pick
"""

from odml_table import OdmlTable
import xlwt
from xls_style import XlsStyle
import datetime


class OdmlXlsTable(OdmlTable):
    """
    Class to create a csv-file from an odml-file


    :param sheetname: name of the excel sheet; default is 'sheet1'
    :param header_style: style used for the header of the table
    :param first_style: default style used for the rows
    :param second_style: used to switch styles of the rows if changing_point
        is not None
    :param first_marked_style: default style used in marked columns
    :param second_marked_style: used to switch styles of the rows in marked
        columns if changing_point is not None
    :param pattern: can be 'alternating' or 'chessfield'
    :param changing_point: select the point for changing styles. this can be
        when a new section, property or value starts ('sections', 'properties',
        'values' or None)
    :type sheetname: string
    :type header_style: XlsStyle
    :type first_style: XlsStyle
    :type second_style: XlsStyle
    :type first_marked_style: XlsStyle
    :type second_marked_style: XlsStyle
    :type pattern: string
    :type changing_point: string


    """

    def __init__(self):
        OdmlTable.__init__(self)
        self.sheetname = "sheet1"
        self._marked_cols = ["Value"]
        self.header_style = XlsStyle(backcolor='gray80', fontcolor='white',
                                     fontstyle='bold 1')
        self.first_style = XlsStyle(backcolor='dark_blue', fontcolor='white',
                                    fontstyle='')
        self.second_style = XlsStyle(backcolor='green', fontcolor='white',
                                     fontstyle='')
        self.first_marked_style = XlsStyle(backcolor='light_blue',
                                           fontcolor='black', fontstyle='',)
        self.second_marked_style = XlsStyle(backcolor='lime',
                                            fontcolor='black', fontstyle='',)
        self._pattern = 'alternating'
        self._changing_point = 'sections'

    #TODO: python properties??

    @property
    def changing_point(self):
        return self._changing_point

    @changing_point.setter
    def changing_point(self, point):
        if point in ["sections", "properties", "values", None]:
            self._changing_point = point
        else:
            raise Exception("Your changing point must be 'sections', " +
                            "'properties', 'values' or None")
        # TODO: exceptions

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pat):
        if pat in ['alternating', 'chessfield']:
            self._pattern = pat
        else:
            raise Exception("This pattern does not exist")

    def mark_columns(self, *args):
        """
        choose the columns of the table you want to highlight by giving them
        another style (for example a different color).
        Possible Arguments are:

          - 'Path'
          - 'SectionName'
          - 'SectionType'
          - 'SectionDefinition'
          - 'PropertyName'
          - 'PropertyDefinition'
          - 'Value'
          - 'ValueDefinition'
          - 'DataUnit'
          - 'DataUncertainty'
          - 'odmlDatatype'.

        """
        cols = []
        for arg in args:
            if arg in self._header_titles.keys():
                cols.append(arg)
            else:
                raise Exception("wrong argument")
                # TODO: exception...
        self._marked_cols = cols

    def write2file(self, save_to):
        """
        writes the data from the odml-file to a xls-file

        :param save_to: name of the xls-file
        :type save_to: string
        """

        styles = {"header": xlwt.easyxf(self.header_style.get_style_string()),
                  "row0col0": xlwt.easyxf(self.first_style.get_style_string()),
                  "row1col0":
                  xlwt.easyxf(self.second_style.get_style_string()),
                  "row0col1":
                  xlwt.easyxf(self.first_marked_style.get_style_string()),
                  "row1col1":
                  xlwt.easyxf(self.second_marked_style.get_style_string())
                  }
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(self.sheetname)

        oldpath = ""
        oldprop = ""
        oldrow = []
        row = 1

        max_col_len = [len(self._header_titles[h]) for h in self._header]
        col_style = 0
        row_style = 0

        # write the header
        for col, h in enumerate(self._header):
            sheet.write(0, col, self._header_titles[h] if h in
                        self._header_titles else "", styles['header'])

        # write the rows
        for dic in self._odmldict:

            # make a copy of the actual dic
            row_dic = dic.copy()

            # removing unneccessary entries
            if dic["Path"] == oldpath:
                if not self.show_all_sections:
                    for h in self._SECTION_INF:
                        row_dic[h] = ""
            else:
                # start of a new section
                if self._changing_point is 'sections':
                    row_style = (row_style + 1) % 2     # switch row-color
                oldpath = dic["Path"]
                oldprop = ""

            if dic["PropertyName"] == oldprop:
                if not self.show_all_properties:
                    for h in self._PROPERTY_INF:
                        row_dic[h] = ""
            else:
                # start of a new property
                if self._changing_point is 'properties':
                    row_style = (row_style + 1) % 2     # switch row-color
                oldprop = dic["PropertyName"]

            # check the changing point
            if self._changing_point is 'values':
                row_style = (row_style + 1) % 2
            elif self._changing_point is None:
                pass
            elif not self._changing_point in ['sections', 'properties']:
                raise Exception("Invalid argument for changing_point: Your " +
                                "changing_point must be 'sections', " +
                                "'properties', 'values' or None")
                # TODO: change exception

            # row_content: only those elements of row_dic, that will be
            # visible in the table
            row_content = [row_dic[h] for h in self._header]

            # check, if row would be empty or same as the row before;
            # if so, skip the row
            if ((row_content == oldrow) or
                    (row_content == ['' for h in self._header])):
                continue
            else:
                oldrow = list(row_content)

            for col, h in enumerate(self._header):

                if self._pattern is "chessfield":
                    row_style = (row_style + 1) % 2
                elif self._pattern is "alternating":
                    row_style = row_style
                else:
                    raise Exception("this is not a valid argument")
                    # TODO: better exception

                # adjust column style
                if h in self._marked_cols:
                    col_style = 1
                else:
                    col_style = 0

                stylestring = "row" + str(row_style) + "col" + str(col_style)

                style = styles[stylestring]
                cell_content = row_dic[h]

                #special style for datetime-objects

                if isinstance(cell_content, datetime.datetime):
                    style.num_format_str = "DD-MM-YYYY HH:MM:SS"
                elif isinstance(cell_content, datetime.date):
                    style.num_format_str = "DD-MM-YYYY"
                elif isinstance(cell_content, datetime.time):
                    style.num_format_str = "HH:MM:SS"
                else:
                    style.num_format_str = ""

                # finding longest string in the column
                if len(str(cell_content)) > max_col_len[col]:
                    max_col_len[col] = len(str(cell_content))

                sheet.write(row, col, cell_content, style)

            row += 1

        # adjust the size of the columns due to the max length of the content
        for i, l in enumerate(max_col_len):
            sheet.col(i).width = 256 * (l+1)

        workbook.save(save_to)
