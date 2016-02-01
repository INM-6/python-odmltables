# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:49:47 2015

@author: pick
"""

from odmltables.odml_xls_table import OdmlXlsTable
import unittest
import os
from create_test_odmls import create_2samerows_test_odml
from create_test_odmls import create_datatype_test_odml

import xlrd


class TestOdmlXlsTableAttributes(unittest.TestCase):
    """
    test, if changes of the attributes can be made and if wrong input leads to
    the right exceptions
    """

    def setUp(self):
        self.test_xls_table = OdmlXlsTable()

    def test_change_pattern(self):
        self.test_xls_table.pattern = 'alternating'
        self.assertEquals(self.test_xls_table.pattern, 'alternating')
        self.test_xls_table.pattern = 'chessfield'
        self.assertEquals(self.test_xls_table.pattern, 'chessfield')
        self.test_xls_table.pattern = 'alternating'
        self.assertEquals(self.test_xls_table.pattern, 'alternating')
        with self.assertRaises(Exception):
            # TODO: exception??
            self.test_xls_table.pattern = 'something'

    def test_change_changingpoint(self):
        self.test_xls_table.changing_point = 'sections'
        self.assertEquals(self.test_xls_table.changing_point, 'sections')
        self.test_xls_table.changing_point = 'properties'
        self.assertEquals(self.test_xls_table.changing_point, 'properties')
        self.test_xls_table.changing_point = 'values'
        self.assertEquals(self.test_xls_table.changing_point, 'values')
        self.test_xls_table.changing_point = None
        self.assertEquals(self.test_xls_table.changing_point, None)
        with self.assertRaises(Exception):
            # TODO: exception??
            self.test_xls_table.changing_point = 'something'

    def test_mark_columns(self):
        self.test_xls_table.mark_columns('SectionName', 'Path', 'Value')
        self.assertItemsEqual(self.test_xls_table._marked_cols, ['SectionName',
                                                                 'Path',
                                                                 'Value'])
        self.test_xls_table.mark_columns('DataUnit')
        self.assertItemsEqual(self.test_xls_table._marked_cols, ['DataUnit'])

    def test_highlight_defaults(self):
        self.test_xls_table.highlight_defaults = True
        self.assertTrue(self.test_xls_table._highlight_defaults)
        self.assertTrue(self.test_xls_table.highlight_defaults)

        self.test_xls_table.highlight_defaults = False
        self.assertFalse(self.test_xls_table._highlight_defaults)
        self.assertFalse(self.test_xls_table.highlight_defaults)

        self.test_xls_table.highlight_defaults = 'True'
        self.assertTrue(self.test_xls_table._highlight_defaults)
        self.assertTrue(self.test_xls_table.highlight_defaults)


class TestOdmlXlsTable(unittest.TestCase):

    def setUp(self):
        self.test_xls_table = OdmlXlsTable()
        self.filename = 'test.xls'

    def tearDown(self):
        os.remove(self.filename)

    def test_xls_datatypes(self):
        """
        test for all datatypes, if the information in the table is right
        """

        expected = [['Document Information', 'author', '', 'date',
                     '', 'repository', '', 'version', '0.1'],
                    ['Path to Section', 'Property Name', 'Value',
                     'odML Data Type', '', '', '', '', ''],
                    ['/numbers', 'Integer', -10, 'int', '', '', '', '', ''],
                    ['/numbers', 'Integer', 0, 'int', '', '', '', '', ''],
                    ['/numbers', 'Integer', 10, 'int', '', '', '', '', ''],
                    ['/numbers', 'Float', -1.234, 'float', '', '', '', '', ''],
                    ['/numbers', 'Float', 0.0, 'float', '', '', '', '', ''],
                    ['/numbers', 'Float', 1.234, 'float', '', '', '', '', ''],
                    ['/other', 'Boolean', 'true', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 'false', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 'True', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 'False', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 't', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 'f', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 'T', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 'F', 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 1, 'boolean', '', '', '', '', ''],
                    ['/other', 'Boolean', 0, 'boolean', '', '', '', '', ''],
                    ['/texts/datetime', 'Datetime', (2014, 12, 11, 15, 2, 0),
                     'datetime', '', '', '', '', ''],
                    ['/texts/datetime', 'Date', (2014, 12, 11, 0, 0, 0),
                     'date', '', '', '', '', ''],
                    ['/texts/datetime', 'Time', (0, 0, 0, 15, 2, 0), 'time', '', '', '', '', ''],
                    ['/texts/string-like', 'String', 'this is a string',
                     'string', '', '', '', '', ''],
                    ['/texts/string-like', 'Text', 'this is a text. It is ' +
                     'longer than a string and contains punctuation marks!',
                     'text', '', '', '', '', ''],
                    ['/texts/string-like', 'Person', 'Jana Pick', 'person', '', '', '', '', '']]

        self.test_xls_table.load_from_function(create_datatype_test_odml)

        self.test_xls_table.show_all_sections = True
        self.test_xls_table.show_all_properties = True
        self.test_xls_table.show_all_valueInformation = True

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in range(worksheet.nrows):
                for col in range(worksheet.ncols):
                    cell = worksheet.cell(row, col)
                    value = cell.value
                    if cell.ctype == 3:
                        # if its a date,convert it to a tuple
                        value = xlrd.xldate_as_tuple(value, 0)
                    self.assertEquals(value, expected[row][col])

    def test_empty_rows(self):
        """
        test, if emtpy rows appear in the table
        """
        expected = [['Document Information', 'author', '', 'date',
                     '', 'repository', '', 'version', ''],
                    ['Path to Section', 'Section Name', 'Property Name','','','','','',''],
                    ['/section1', 'section1', 'property1','','','','','','',''],
                    ['/section2', 'section2', 'property1','','','','','','','']]

        self.test_xls_table.load_from_function(create_2samerows_test_odml)

        self.test_xls_table.change_header(Path=1, SectionName=2,
                                          PropertyName=3)

        self.test_xls_table.show_all_sections = False
        self.test_xls_table.show_all_properties = False

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in range(worksheet.nrows):
                for col in range(worksheet.ncols):
                    c_value = worksheet.cell(row, col).value
                    self.assertEquals(c_value, expected[row][col])

if __name__ == '__main__':
    unittest.main()
