# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:01:13 2015

@author: pick
"""

import odml
from odmltables.odml_csv_table import OdmlCsvTable, OdmlTable
from .create_test_odmls import (create_showall_test_odml, create_2samerows_test_odml)
import os
import csv

import unittest


class TestOdmlCsvTable(unittest.TestCase):
    """
    """

    def setUp(self):
        self.test_csv_table = OdmlCsvTable()
        self.filename = 'test.csv'

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_empty_rows(self):
        """
        test if a row that would be empty will appear in the table
        """

        expected = [['Document Information', 'author', '', 'date', None, 'repository', '',
                     'version', ''],
                    ['Path to Section', 'Section Name', 'Property Name', '', '', '', '', '', ''],
                    ['/section1', 'section1', 'property1', '', '', '', '', '', ''],
                    ['/section2', 'section2', 'property1', '', '', '', '', '', '']]

        self.test_csv_table.load_from_function(create_2samerows_test_odml)

        self.test_csv_table.change_header(Path=1, SectionName=2, PropertyName=3, )

        self.test_csv_table.show_all_sections = False
        self.test_csv_table.show_all_properties = False

        self.test_csv_table.write2file(self.filename)

        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                if None in expected[row_num]:
                    for id in range(len(expected[row_num])):
                        if expected[row_num][id] is not None:
                            self.assertEqual(row[id], expected[row_num][id])
                else:
                    self.assertEqual(row, expected[row_num])
                row_num += 1

    def test_saveload_empty_value(self):
        doc = odml.Document()
        doc.append(odml.Section('sec'))
        doc[0].append(odml.Property('prop', values=[]))

        table = OdmlCsvTable()
        table.load_from_odmldoc(doc)
        table.change_header('full')
        table.write2file(self.filename)

        table2 = OdmlTable()
        table2.load_from_csv_table(self.filename)

        # comparing values which are written to xls by default
        self.assertEqual(len(table._odmldict), len(table2._odmldict))
        self.assertEqual(len(table._odmldict), 1)
        self.assertDictEqual(table._odmldict[0], table2._odmldict[0])


class TestShowallOdmlCsvTable(unittest.TestCase):
    """
    test possible combinations of the attributes showall_sections,
    showall_properties and showall_valueinformation to see wether the same
    values are not printed again, unless it is the start of a new section or
    property
    """

    def setUp(self):
        self.test_csv_table = OdmlCsvTable()
        self.test_csv_table.load_from_function(create_showall_test_odml)
        self.test_csv_table.change_header(Path=1,
                                          SectionName=2,
                                          SectionDefinition=3,
                                          PropertyName=4,
                                          PropertyDefinition=5,
                                          Value=6,
                                          DataUnit=7,
                                          DataUncertainty=8,
                                          odmlDatatype=9)
        self.filename = 'testfile.csv'

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
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value2', 'g', '1', 'string'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value3', 'g', '1', 'string'],
            ['/section1', 'section1', 'sec1', 'property2', 'prop2', 'value1', 'g', '1', 'text'],
            ['/section1', 'section1', 'sec1', 'property3', 'prop3', 'value1', 'g', '1', 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value2', 'g', '1', 'string']]

        self.test_csv_table.show_all_sections = True
        self.test_csv_table.show_all_properties = True

        self.test_csv_table.write2file(self.filename)

        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                if None in expected[row_num]:
                    for id in range(len(expected[row_num])):
                        if expected[row_num][id] is not None:
                            self.assertEqual(row[id], expected[row_num][id])
                else:
                    self.assertEqual(row, expected[row_num])
                row_num += 1

    def test_ff(self):
        """
        showall_sections=False
        showall_properties=False
        """
        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Section Definition', 'Property Name',
             'Property Definition', 'Value', 'Data Unit', 'Data Uncertainty', 'odML Data Type'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['', '', '', '', '', 'value2', '', '', ''],
            ['', '', '', '', '', 'value3', '', '', ''],
            ['', '', '', 'property2', 'prop2', 'value1', 'g', '1', 'text'],
            ['', '', '', 'property3', 'prop3', 'value1', 'g', '1', 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['', '', '', '', '', 'value2', '', '', '']]

        self.test_csv_table.show_all_sections = False
        self.test_csv_table.show_all_properties = False

        self.test_csv_table.write2file(self.filename)

        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                if None in expected[row_num]:
                    for id in range(len(expected[row_num])):
                        if expected[row_num][id] is not None:
                            self.assertEqual(row[id], expected[row_num][id])
                else:
                    self.assertEqual(row, expected[row_num])
                row_num += 1

    def test_ft(self):
        """
        showall_sections=False
        showall_properties=True
        """
        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Section Definition', 'Property Name',
             'Property Definition', 'Value', 'Data Unit', 'Data Uncertainty', 'odML Data Type'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['', '', '', 'property1', 'prop1', 'value2', 'g', '1', 'string'],
            ['', '', '', 'property1', 'prop1', 'value3', 'g', '1', 'string'],
            ['', '', '', 'property2', 'prop2', 'value1', 'g', '1', 'text'],
            ['', '', '', 'property3', 'prop3', 'value1', 'g', '1', 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['', '', '', 'property1', 'prop1', 'value2', 'g', '1', 'string']]

        self.test_csv_table.show_all_sections = False
        self.test_csv_table.show_all_properties = True

        self.test_csv_table.write2file(self.filename)

        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                if None in expected[row_num]:
                    for id in range(len(expected[row_num])):
                        if expected[row_num][id] is not None:
                            self.assertEqual(row[id], expected[row_num][id])
                else:
                    self.assertEqual(row, expected[row_num])
                row_num += 1

    def test_tf(self):
        """
        showall_sections=True
        showall_properties=False
        """
        expected = [
            ['Document Information', 'author', '', 'date', None, 'repository', '', 'version', ''],
            ['Path to Section', 'Section Name', 'Section Definition', 'Property Name',
             'Property Definition', 'Value', 'Data Unit', 'Data Uncertainty', 'odML Data Type'],
            ['/section1', 'section1', 'sec1', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section1', 'section1', 'sec1', '', '', 'value2', '', '', ''],
            ['/section1', 'section1', 'sec1', '', '', 'value3', '', '', ''],
            ['/section1', 'section1', 'sec1', 'property2', 'prop2', 'value1', 'g', '1', 'text'],
            ['/section1', 'section1', 'sec1', 'property3', 'prop3', 'value1', 'g', '1', 'text'],
            ['/section2', 'section2', 'sec2', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section3', 'section3', 'sec3', 'property1', 'prop1', 'value1', 'g', '1', 'string'],
            ['/section3', 'section3', 'sec3', '', '', 'value2', '', '', '']]

        self.test_csv_table.show_all_sections = True
        self.test_csv_table.show_all_properties = False

        self.test_csv_table.write2file(self.filename)

        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                if None in expected[row_num]:
                    for id in range(len(expected[row_num])):
                        if expected[row_num][id] is not None:
                            self.assertEqual(row[id], expected[row_num][id])
                else:
                    self.assertEqual(row, expected[row_num])
                row_num += 1


if __name__ == '__main__':
    unittest.main()
