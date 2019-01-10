# -*- coding: utf-8 -*-
"""

"""

__package__='odmltables'

import datetime
import xlwt
import numpy as np

# Workaround Python 2 and 3 unicode handling.
try:
    unicode = unicode
except NameError:
    unicode = str

from .odml_table import OdmlTable
from .xls_style import XlsStyle


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
    :param pattern: can be 'alternating' or 'checkerboard'
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

    def __init__(self, load_from=None):
        super(OdmlXlsTable, self).__init__(load_from=load_from)
        self.sheetname = "sheet1"
        self._marked_cols = ["Value"]
        self.document_info_style = XlsStyle(backcolor='white',
                                            fontcolor='gray80',
                                            fontstyle='bold 1')
        self.header_style = XlsStyle(backcolor='gray80',
                                     fontcolor='white',
                                     fontstyle='bold 1')
        self.first_style = XlsStyle(backcolor='dark_blue',
                                    fontcolor='white',
                                    fontstyle='')
        self.second_style = XlsStyle(backcolor='green',
                                     fontcolor='white',
                                     fontstyle='')
        self.first_marked_style = XlsStyle(backcolor='light_blue',
                                           fontcolor='black',
                                           fontstyle='')
        self.second_marked_style = XlsStyle(backcolor='lime',
                                            fontcolor='black',
                                            fontstyle='')
        self.highlight_style = XlsStyle(backcolor='red',
                                        fontcolor='black',
                                        fontstyle='')
        self._highlight_defaults = False
        self._pattern = 'alternating'
        self._changing_point = 'sections'

    # TODO: python properties??

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
        if pat in ['alternating', 'checkerboard']:
            self._pattern = pat
        else:
            raise Exception("This pattern does not exist")

    @property
    def highlight_defaults(self):
        return self._highlight_defaults

    @highlight_defaults.setter
    def highlight_defaults(self, mode):
        if mode in [True, False]:
            self._highlight_defaults = mode
        else:
            try:
                self._highlight_defaults = bool(mode)
            except:
                raise TypeError('Mode "{}" can not be'
                                'converted to boolean.'
                                ''.format(str(mode)))

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
          - 'DataUnit'
          - 'DataUncertainty'
          - 'odmlDatatype'.

        """
        cols = []
        for arg in args:
            if arg in list(self._header_titles):
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

        self.consistency_check()

        valid_changing_points = ['sections', 'properties', 'values', None]
        if not self._changing_point in valid_changing_points:
            raise Exception("Invalid argument for changing_point: Your changing_point must"
                            " be one of {}".format(str(valid_changing_points)))

        styles = {"document_info": xlwt.easyxf(
            self.document_info_style.get_style_string()),
            "header": xlwt.easyxf(self.header_style.get_style_string()),
            "row0col0": xlwt.easyxf(self.first_style.get_style_string()),
            "row1col0":
                xlwt.easyxf(self.second_style.get_style_string()),
            "row0col1":
                xlwt.easyxf(self.first_marked_style.get_style_string()),
            "row1col1":
                xlwt.easyxf(self.second_marked_style.get_style_string()),
            "highlight":
                xlwt.easyxf(self.highlight_style.get_style_string())}


        def write_row(row_id, row_content, stylestrings):
            assert len(row_content) == len(stylestrings)
            xls_styles = [styles[rs] for rs in stylestrings]
            for col_id, cell_content in enumerate(row_content):
                style = xls_styles[col_id]
                if cell_content == None:
                    cell_content = ''
                if isinstance(cell_content, datetime.datetime):
                    style.num_format_str = "DD-MM-YYYY HH:MM:SS"
                elif isinstance(cell_content, datetime.date):
                    style.num_format_str = "DD-MM-YYYY"
                elif isinstance(cell_content, datetime.time):
                    style.num_format_str = "HH:MM:SS"
                else:
                    style.num_format_str = ""

                sheet.write(row_id, col_id, cell_content, style)

                # finding longest string in the column
                if len(unicode(cell_content)) > max_col_len[col_id]:
                    max_col_len[col_id] = len(unicode(cell_content))

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(self.sheetname)

        oldpath = ""
        row_id = 0

        doclen = len(self._docdict) if self._docdict else 0

        max_col_len = [1] * max(len(self._header), 2 * doclen + 1)
        for i, h in enumerate(self._header):
            if h != None:
                max_col_len[i] = len(self._header_titles[h])

        if self._docdict:
            row_content = ['Document Information']
            for k, v in sorted(self._docdict.items()):
                row_content.extend([k,v])
            row_styles = ['document_info'] * len(row_content)
            write_row(0, row_content, row_styles)

            row_id += 1

        # write the header
        for col_id, h in enumerate(self._header):
            sheet.write(row_id, col_id, self._header_titles[h] if h in self._header_titles else "",
                        styles['header'])

        row_id += 1

        # set default styles as bool values for simplicity
        if self._pattern is "checkerboard":
            row_style_default = np.array([0, 1] * (len(self._header)), dtype=bool)
            row_style_default = row_style_default[:len(self._header)]
        elif self._pattern is "alternating":
            row_style_default = np.array([0] * len(self._header), dtype=bool)
        else:
            raise Exception("{} is not a valid pattern".format(self._pattern))
        column_style_default = np.array([1 if h in self._marked_cols else 0 for h in self._header],
                                        dtype=bool)

        self.row_style = row_style_default
        self.column_style = column_style_default



        def _switch_row_style():
            self.row_style = np.invert(self.row_style)

        if self._odmldict != None:
            # write the rest of the rows
            for dic in self._odmldict:

                # make a copy of the actual dic
                row_dic = dic.copy()

                # inflate row_dic
                row_dic['Path'], row_dic['PropertyName'] = row_dic['Path'].split(':')
                row_dic['SectionName'] = row_dic['Path'].split('/')[-1]
                row_dic_complete = row_dic.copy()

                # removing unnecessary entries
                if row_dic["Path"] == oldpath:
                    if not self.show_all_sections:
                        for h in self._SECTION_INF + ['SectionName']:
                            row_dic[h] = ""
                        row_dic['Path'] = ""

                # if dic["Path"].split(':')[-1] == oldprop:
                #     if not self.show_all_properties:
                #         for h in self._PROPERTY_INF:
                #             row_dic[h] = ""

                # handling row styles
                if self._changing_point is 'properties':
                    _switch_row_style()
                elif self._changing_point is 'sections' and (row_dic["Path"] != oldpath):
                    _switch_row_style()

                # row_content: only those elements of row_dic, that will be visible in the table
                row_content = [row_dic[h] if h != None else '' for h in self._header]

                # generating row even when no value entry is present
                if not row_dic['Value']:
                    row_dic['Value'] = ['']

                for v in row_dic['Value']:
                    stylestring = ["row{:d}col{:d}".format(r, c)
                                   for r, c in zip(self.row_style, self.column_style)]
                    # highlight empty values
                    if self._highlight_defaults and (row_dic['Value'] == []
                                                     or row_dic['Value'] == ['']):
                        stylestring[self._header.index('Value')] = 'highlight'

                    # update value entry and write line
                    if 'Value' in self._header:
                        # explicitely replacing 0-1 representation by string representation
                        if isinstance(v, bool):
                            v = 'True' if v else 'False'
                        row_content[self._header.index('Value')] = v
                    write_row(row_id, row_content, stylestring)
                    row_id += 1

                    # continue with next property if values are not exported
                    if 'Value' not in self._header:
                        break

                    if self._changing_point is 'values':
                        _switch_row_style()

                    # adjust section and property entries for next value
                    for h in self._header:
                        if (not self.show_all_properties
                                and h in self._PROPERTY_INF + ['PropertyName']):
                            row_content[self._header.index(h)] = ''
                        elif (not self.show_all_sections
                              and h in self._SECTION_INF + ['SectionName', 'Path']):
                            row_content[self._header.index(h)] = ''

                oldpath = row_dic_complete["Path"]

        # adjust the size of the columns due to the max length of the content,
        # but no more than max_allowed_col_len characters
        max_allowed_col_len = 80
        for i, l in enumerate(max_col_len):
            sheet.col(i).width = 256 * (min(l, max_allowed_col_len) + 1)

        workbook.save(save_to)
