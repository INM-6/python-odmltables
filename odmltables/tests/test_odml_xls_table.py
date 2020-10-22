# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:49:47 2015

@author: pick
"""

import copy
import odml
from odmltables.odml_xls_table import OdmlXlsTable, OdmlTable
import unittest
import os
from odmltables.tests.create_test_odmls import (create_2samerows_test_odml,
                                                create_datatype_test_odml,
                                                create_complex_test_odml, create_showall_test_odml)

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
        self.assertEqual(self.test_xls_table.pattern, 'alternating')
        self.test_xls_table.pattern = 'checkerboard'
        self.assertEqual(self.test_xls_table.pattern, 'checkerboard')
        self.test_xls_table.pattern = 'alternating'
        self.assertEqual(self.test_xls_table.pattern, 'alternating')
        with self.assertRaises(Exception):
            # TODO: exception??
            self.test_xls_table.pattern = 'something'

    def test_change_changingpoint(self):
        self.test_xls_table.changing_point = 'sections'
        self.assertEqual(self.test_xls_table.changing_point, 'sections')
        self.test_xls_table.changing_point = 'properties'
        self.assertEqual(self.test_xls_table.changing_point, 'properties')
        self.test_xls_table.changing_point = 'values'
        self.assertEqual(self.test_xls_table.changing_point, 'values')
        self.test_xls_table.changing_point = None
        self.assertEqual(self.test_xls_table.changing_point, None)
        with self.assertRaises(Exception):
            # TODO: exception??
            self.test_xls_table.changing_point = 'something'

    def test_mark_columns(self):
        self.test_xls_table.mark_columns('SectionName', 'Path', 'Value')
        self.assertListEqual(self.test_xls_table._marked_cols, ['SectionName',
                                                                'Path',
                                                                'Value'])
        self.test_xls_table.mark_columns('DataUnit')
        self.assertListEqual(self.test_xls_table._marked_cols, ['DataUnit'])

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
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_xls_datatypes(self):
        """
        test for all datatypes, if the information in the table is right
        """

        # input = [['Document Information', 'author', '', 'date', '', 'repository', '','version', '0.1'],
        #             ['Path to Section', 'Property Name', 'Value', 'odML Data Type', '', '', '','', ''],
        #             ['/numbers', 'Float', -1.234, 'float', '', '', '', '', ''],
        #             ['/numbers', 'Float', 0.0, 'float', '', '', '', '', ''],
        #             ['/numbers', 'Float', 1.234, 'float', '', '', '', '', ''],
        #             ['/numbers', 'Integer', -10.0, 'int', '', '', '', '', ''],
        #             ['/numbers', 'Integer', 0.0, 'int', '', '', '', '', ''],
        #             ['/numbers', 'Integer', 10.0, 'int', '', '', '', '', ''],
        #             ['/other', 'Boolean', 'true', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 'false', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 'True', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 'False', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 't', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 'f', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 'T', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 'F', 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 1.0, 'boolean', '', '', '', '', ''],
        #             ['/other', 'Boolean', 0.0, 'boolean', '', '', '', '', ''],
        #             ['/texts/datetime', 'Date', (2014, 12, 11, 0, 0, 0), 'date', '', '', '', '', ''],
        #             ['/texts/datetime', 'Datetime', (2014, 12, 11, 15, 2, 0), 'datetime', '', '', '','', ''],
        #             ['/texts/datetime', 'Time', (0, 0, 0, 15, 2, 0), 'time', '', '', '', '', ''],
        #             ['/texts/string-like', 'Person', 'Jana Pick', 'person', '', '', '', '', ''],
        #             ['/texts/string-like', 'String', 'this is a string', 'string', '', '','', '',''],
        #             ['/texts/string-like', 'Text', 'this is a text. It is longer than a string and contains punctuation marks!', 'text', '', '', '', '', '']]

        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version',
             '0.1'],
            ['Path to Section', 'Property Name', 'Value', 'odML Data Type', '', '', '', '', ''],
            ['/numbers', 'Float', -1.234, 'float', '', '', '', '', ''],
            ['/numbers', 'Float', 0.0, 'float', '', '', '', '', ''],
            ['/numbers', 'Float', 1.234, 'float', '', '', '', '', ''],
            ['/numbers', 'Integer', -10.0, 'int', '', '', '', '', ''],
            ['/numbers', 'Integer', 0.0, 'int', '', '', '', '', ''],
            ['/numbers', 'Integer', 10.0, 'int', '', '', '', '', ''],
            ['/other', 'Boolean', 'True', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'False', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'True', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'False', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'True', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'False', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'True', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'False', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'True', 'boolean', '', '', '', '', ''],
            ['/other', 'Boolean', 'False', 'boolean', '', '', '', '', ''],
            ['/texts/datetime', 'Date', (2014, 12, 11, 0, 0, 0), 'date', '', '', '', '', ''],
            ['/texts/datetime', 'Datetime', (2014, 12, 11, 15, 2, 0), 'datetime', '', '', '', '',
             ''],
            ['/texts/datetime', 'Time', (0, 0, 0, 15, 2, 0), 'time', '', '', '', '', ''],
            ['/texts/string-like', 'Person', 'Jana Pick', 'person', '', '', '', '', ''],
            ['/texts/string-like', 'String', 'this is a string', 'string', '', '', '', '', ''],
            ['/texts/string-like', 'Text',
             'this is a text. It is longer than a string and contains punctuation marks!', 'text',
             '', '', '', '', '']]

        self.test_xls_table.load_from_function(create_datatype_test_odml)

        self.test_xls_table.show_all_sections = True
        self.test_xls_table.show_all_properties = True

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in list(range(worksheet.nrows)):
                for col in list(range(worksheet.ncols)):
                    if expected[row][col] is None:  # skip undefined entries
                        continue
                    cell = worksheet.cell(row, col)
                    value = cell.value
                    if cell.ctype == 3:
                        # if its a date, convert it to a tuple
                        value = xlrd.xldate_as_tuple(value, 0)
                    self.assertEqual(value, expected[row][col])

    def test_empty_rows(self):
        """
        test, if emtpy rows appear in the table
        """
        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Property Name', '', '', '', '', '', ''],
            ['/section1', 'section1', 'property1', '', '', '', '', '', '', ''],
            ['/section2', 'section2', 'property1', '', '', '', '', '', '', '']]

        self.test_xls_table.load_from_function(create_2samerows_test_odml)

        self.test_xls_table.change_header(Path=1, SectionName=2,
                                          PropertyName=3)

        self.test_xls_table.show_all_sections = False
        self.test_xls_table.show_all_properties = False

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in list(range(worksheet.nrows)):
                for col in list(range(worksheet.ncols)):
                    if expected[row][col] is None:  # skip undefined entries
                        continue
                    c_value = worksheet.cell(row, col).value
                    self.assertEqual(c_value, expected[row][col])

    def test_write_read(self):
        self.test_xls_table.load_from_function(create_complex_test_odml)

        self.test_xls_table.show_all_sections = True
        self.test_xls_table.show_all_properties = True

        old_dict = copy.deepcopy(self.test_xls_table._odmldict)

        # including all columns available
        self.test_xls_table.change_header(Path=1, SectionName=2, PropertyName=3, SectionType=4,
                                          SectionDefinition=5, PropertyDefinition=6, Value=7,
                                          DataUnit=8, DataUncertainty=9, odmlDatatype=10)

        self.test_xls_table.write2file(self.filename)
        self.test_xls_table.load_from_xls_table(self.filename)

        new_dict = self.test_xls_table._odmldict

        self.assertListEqual(old_dict, new_dict)

    def test_saveload_empty_value(self):
        doc = odml.Document()
        doc.append(odml.Section('sec'))
        doc[0].append(odml.Property('prop', values=[]))

        table = OdmlXlsTable()
        table.load_from_odmldoc(doc)
        table.change_header('full')
        table.write2file(self.filename)

        table2 = OdmlTable()
        table2.load_from_xls_table(self.filename)

        # comparing values which are written to xls by default
        self.assertEqual(len(table._odmldict), len(table2._odmldict))
        self.assertEqual(len(table._odmldict), 1)
        self.assertDictEqual(table._odmldict[0], table2._odmldict[0])


class TestShowallOdmlXlsTable(unittest.TestCase):
    """
    test possible combinations of the attributes showall_sections,
    showall_properties and showall_valueinformation to see wether the same
    values are not printed again, unless it is the start of a new section or
    property
    """

    def setUp(self):
        self.test_xls_table = OdmlXlsTable()
        self.test_xls_table.load_from_function(create_showall_test_odml)
        self.test_xls_table.change_header(Path=1,
                                          SectionName=2,
                                          SectionDefinition=3,
                                          PropertyName=4,
                                          PropertyDefinition=5,
                                          Value=6,
                                          DataUnit=7,
                                          DataUncertainty=8,
                                          odmlDatatype=9)
        self.filename = 'testfile.xls'

    def tearDown(self):
        os.remove(self.filename)

    def test_tt(self):
        """
        showall_sections=True
        showall_properties=True
        """

        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Section Definition', 'Property Name',
             'Property Definition', 'Value', 'Data Unit', 'Data Uncertainty', 'odML Data Type'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value2', 'g', 1, 'string'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value3', 'g', 1, 'string'],
            ['/section1', 'section1', 'sec1', 'property2', 'prop2', 'value1', 'g', 1, 'text'],
            ['/section1', 'section1', 'sec1', 'property3', 'prop3', 'value1', 'g', 1, 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value2', 'g', 1, 'string']]

        self.test_xls_table.show_all_sections = True
        self.test_xls_table.show_all_properties = True

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in list(range(worksheet.nrows)):
                for col in list(range(worksheet.ncols)):
                    if expected[row][col] is None:  # skipping unspecified cells
                        continue
                    cell = worksheet.cell(row, col)
                    value = cell.value
                    if cell.ctype == 3:
                        # if its a date, convert it to a tuple
                        value = xlrd.xldate_as_tuple(value, 0)
                    self.assertEqual(value, expected[row][col])

        # with open(self.filename, 'r') as xlsfile:
        #     xlsreader = xls.reader(xlsfile)
        #     row_num = 0
        #     for row in xlsreader:
        #         self.assertEqual(row, expected[row_num])
        #         row_num += 1

    def test_ff(self):
        """
        showall_sections=False
        showall_properties=False
        """
        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Section Definition', 'Property Name',
             'Property Definition', 'Value', 'Data Unit', 'Data Uncertainty', 'odML Data Type'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['', '', '', '', '', 'value2', '', '', ''],
            ['', '', '', '', '', 'value3', '', '', ''],
            ['', '', '', 'property2', 'prop2', 'value1', 'g', 1, 'text'],
            ['', '', '', 'property3', 'prop3', 'value1', 'g', 1, 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['', '', '', '', '', 'value2', '', '', '']]

        self.test_xls_table.show_all_sections = False
        self.test_xls_table.show_all_properties = False

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in list(range(worksheet.nrows)):
                for col in list(range(worksheet.ncols)):
                    if expected[row][col] is None:  # skipping unspecified cells
                        continue
                    cell = worksheet.cell(row, col)
                    value = cell.value
                    if cell.ctype == 3:
                        # if its a date, convert it to a tuple
                        value = xlrd.xldate_as_tuple(value, 0)
                    self.assertEqual(value, expected[row][col])

    def test_ft(self):
        """
        showall_sections=False
        showall_properties=True
        """
        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Section Definition', 'Property Name',
             'Property Definition', 'Value', 'Data Unit', 'Data Uncertainty', 'odML Data Type'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['', '', '', 'property1', 'prop1', 'value2', 'g', 1, 'string'],
            ['', '', '', 'property1', 'prop1', 'value3', 'g', 1, 'string'],
            ['', '', '', 'property2', 'prop2', 'value1', 'g', 1, 'text'],
            ['', '', '', 'property3', 'prop3', 'value1', 'g', 1, 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['', '', '', 'property1', 'prop1', 'value2', 'g', 1, 'string']]

        self.test_xls_table.show_all_sections = False
        self.test_xls_table.show_all_properties = True

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in list(range(worksheet.nrows)):
                for col in list(range(worksheet.ncols)):
                    if expected[row][col] is None:  # skipping unspecified cells
                        continue
                    cell = worksheet.cell(row, col)
                    value = cell.value
                    if cell.ctype == 3:
                        # if its a date, convert it to a tuple
                        value = xlrd.xldate_as_tuple(value, 0)
                    self.assertEqual(value, expected[row][col])

    def test_tf(self):
        """
        showall_sections=True
        showall_properties=False
        """
        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Section Definition', 'Property Name',
             'Property Definition', 'Value', 'Data Unit', 'Data Uncertainty', 'odML Data Type'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section1', 'section1', 'sec1', '', '', 'value2', '', '', ''],
            ['/section1', 'section1', 'sec1', '', '', 'value3', '', '', ''],
            ['/section1', 'section1', 'sec1', 'property2', 'prop2', 'value1', 'g', 1, 'text'],
            ['/section1', 'section1', 'sec1', 'property3', 'prop3', 'value1', 'g', 1, 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', 1, 'string'],
            ['/section3', 'section3', 'sec3', '', '', 'value2', '', '', '']]

        self.test_xls_table.show_all_sections = True
        self.test_xls_table.show_all_properties = False

        self.test_xls_table.write2file(self.filename)

        workbook = xlrd.open_workbook(self.filename)
        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            for row in list(range(worksheet.nrows)):
                for col in list(range(worksheet.ncols)):
                    if expected[row][col] is None:  # skipping unspecified cells
                        continue
                    cell = worksheet.cell(row, col)
                    value = cell.value
                    if cell.ctype == 3:
                        # if its a date, convert it to a tuple
                        value = xlrd.xldate_as_tuple(value, 0)
                    self.assertEqual(value, expected[row][col])


if __name__ == '__main__':
    unittest.main()
