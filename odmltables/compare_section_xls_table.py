# -*- coding: utf-8 -*-
__package__='odmltables'

import os.path
import datetime
import xlwt

from .compare_section_table import CompareSectionTable
from .xls_style import XlsStyle


class CompareSectionXlsTable(CompareSectionTable):
    """
    class to write a CompareSectionTable to a xls-file


    :param sheet_name: name of the excel-sheet, default is 'sheet1'
    :type sheet_name: string
    :param header_style: style used for the header
    :param first_style: style used for the values inside the table
    :param second_style: second style used for the values inside the table
    :param missing_value_style: if include_all is True, this style will be used
        if a property doesnt exist in the section, so they distinguish from
        properties with empty values
    :type header_style: XlsStyle
    :type first_style: XlsStyle
    :type second_style: XlsStyle
    :type missing_value_style: XlsStyle

    """

    def __init__(self):

        CompareSectionTable.__init__(self)

        self.sheet_name = "sheet1"
        self.header_style = XlsStyle(backcolor='gray80', fontcolor='white',
                                     fontstyle='bold 1')
        self.first_style = XlsStyle(backcolor='dark_blue', fontcolor='white',
                                    fontstyle='')
        self.second_style = XlsStyle(backcolor='green', fontcolor='white',
                                     fontstyle='')
        self.missing_value_style = XlsStyle(backcolor='red',
                                            fontcolor='black', fontstyle='', )

    def write2file(self, save_to):
        """
        writes the table to an xls-file
        """
        headerstyle = xlwt.easyxf(self.header_style.get_style_string())
        missing_val_style = xlwt.easyxf(
            self.missing_value_style.get_style_string())
        row_styles = [xlwt.easyxf(self.first_style.get_style_string()),
                      xlwt.easyxf(self.second_style.get_style_string())]

        properties, sections, table = self._build_table()

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(self.sheet_name)

        if os.path.splitext(save_to)[-1] == '':
            save_to += '.xls'

        max_col_len = []

        if (self.switch):

            for i, prop in enumerate([''] + properties):
                sheet.write(0, i, prop, headerstyle)
                max_col_len.append(len(str(prop)))

            for row_num, sec in enumerate(sections):
                sheet.write(row_num + 1, 0, sec, headerstyle)
                if len(str(sec)) > max_col_len[0]:
                    max_col_len[0] = len(str(sec))

            for row_num, row in enumerate(table):
                for col_num, elem in enumerate(row):

                    if elem is None:
                        style = missing_val_style
                        cell_content = ""
                    else:
                        style = row_styles[row_num % 2]
                        cell_content = elem

                        if isinstance(cell_content, datetime.datetime):
                            style.num_format_str = "DD-MM-YYYY HH:MM:SS"
                        elif isinstance(cell_content, datetime.date):
                            style.num_format_str = "DD-MM-YYYY"
                        elif isinstance(cell_content, datetime.time):
                            style.num_format_str = "HH:MM:SS"
                        else:
                            style.num_format_str = ""

                    sheet.write(row_num + 1, col_num + 1, cell_content, style)
                    if len(str(cell_content)) > max_col_len[col_num+1]:
                        max_col_len[col_num+1] = len(str(cell_content))

        else:

            for i, sec in enumerate([''] + sections):
                sheet.write(0, i, sec, headerstyle)
                max_col_len.append(len(str(sec)))

            for row_num, prop in enumerate(properties):
                sheet.write(row_num + 1, 0, prop, headerstyle)
                if len(str(prop)) > max_col_len[0]:
                    max_col_len[0] = len(str(prop))

            for col_num, col in enumerate(table):
                for row_num, elem in enumerate(col):

                    if elem is None:
                        style = missing_val_style
                        cell_content = ""
                    else:
                        style = row_styles[row_num % 2]
                        cell_content = elem

                        if isinstance(cell_content, datetime.datetime):
                            style.num_format_str = "DD-MM-YYYY HH:MM:SS"
                        elif isinstance(cell_content, datetime.date):
                            style.num_format_str = "DD-MM-YYYY"
                        elif isinstance(cell_content, datetime.time):
                            style.num_format_str = "HH:MM:SS"
                        else:
                            style.num_format_str = ""

                    sheet.write(row_num + 1, col_num + 1, cell_content, style)
                    if len(str(cell_content)) > max_col_len[col_num+1]:
                        max_col_len[col_num+1] = len(str(cell_content))

        # adjust width of he columns
        for col_id, col_len in enumerate(max_col_len):
            sheet.col(col_id).width = (256 * (col_len+1))

        workbook.save(save_to)
