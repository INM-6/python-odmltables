# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:54:02 2015

@author: pick
"""

from odmltables.compare_section_table import CompareSectionTable
from odmltables.compare_section_csv_table import CompareSectionCsvTable
from odmltables.compare_section_xls_table import CompareSectionXlsTable
import odml
from .create_test_odmls import create_compare_test
import os
import csv
import unittest


class TestCompareSectionTable(unittest.TestCase):
    def setUp(self):
        self.test_table = CompareSectionTable()
        self.doc = create_compare_test()
        odml.tools.xmlparser.XMLWriter(self.doc).write_file('comparetest.odml')

    def tearDown(self):
        os.remove('comparetest.odml')

    def test_loadfromfile(self):
        self.test_table.load_from_file('comparetest.odml')
        self.assertEqual(self.doc, self.test_table._odmldoc)

    def test_choose(self):
        self.test_table.choose_sections(
            'Section3', 'Section1', 'One more Section')
        expected = [section.name for section in
                    self.doc.itersections(filter_func=lambda x:
                    x.name in ['Section1', 'Section3', 'One more Section'])]
        result = [section.name for section in
                  self.doc.itersections(filter_func=self.test_table._sel_fun)]
        self.assertListEqual(expected, result)

    def test_choose_start(self):
        self.test_table.choose_sections_startwith('Section')
        expected = [section.name for section in
                    self.doc.itersections(filter_func=lambda x:
                    x.name.startswith('Section'))]
        result = [section.name for section in
                  self.doc.itersections(filter_func=self.test_table._sel_fun)]
        self.assertListEqual(expected, result)


include_true_expected = [['', 'Section1', 'Section2', 'Section3', 'One more Section'],
                         ['Property1', '0', '1', '2', ''],
                         ['Property2', '1', '2', '', '11'],
                         ['Property3', '2', '3', '4', '']]

include_false_expected = [['', 'Section1', 'Section2', 'Section3'],
                          ['Property1', '0', '1', '2'],
                          ['Property3', '2', '3', '4']]

switch_expected = [['', 'Property1', 'Property2', 'Property3'],
                   ['Section1', '0', '1', '2'],
                   ['Section2', '1', '2', '3'],
                   ['Section3', '2', '', '4'],
                   ['One more Section', '', '11', '']]


class TestCompareCsv(unittest.TestCase):
    def setUp(self):

        self.test_table = CompareSectionCsvTable()
        self.doc = create_compare_test()
        odml.tools.xmlparser.XMLWriter(self.doc).write_file('comparetest.odml')
        self.test_table.load_from_file('comparetest.odml')
        self.test_table.choose_sections_startwith('')

    def tearDown(self):
        os.remove('comparetest.odml')
        os.remove('test.csv')

    def test_includeall_true(self):
        self.test_table.include_all = True
        self.test_table.switch = False
        self.test_table.write2file('test.csv')
        with open('test.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                self.assertEqual(row, include_true_expected[row_num])
                row_num += 1

    def test_includeall_false(self):
        self.test_table.include_all = False
        self.test_table.switch = False
        self.test_table.choose_sections_startwith('S')
        self.test_table.write2file('test.csv')
        with open('test.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                self.assertEqual(row, include_false_expected[row_num])
                row_num += 1

    def test_switch(self):
        self.test_table.switch = True
        self.test_table.include_all = True
        self.test_table.write2file('test.csv')
        with open('test.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            row_num = 0
            for row in csvreader:
                self.assertEqual(row, switch_expected[row_num])
                row_num += 1


class TestCompareXls(unittest.TestCase):
    def setUp(self):
        self.test_table = CompareSectionXlsTable()

    def tearDown(self):
        pass

    def test_includeall_true(self):
        self.test_table.include_all = True
        self.test_table.switch = False

    def test_includeall_false(self):
        self.test_table.include_all = False
        self.test_table.switch = False

    def test_switch(self):
        self.test_table.switch = True


if __name__ == "__main__":
    unittest.main()
