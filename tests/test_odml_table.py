# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:11:32 2015

@author: pick
"""

import odml
from odmlviz.odml_table import OdmlTable
from odmlviz.odml_csv_table import OdmlCsvTable
from odmlviz.odml_xls_table import OdmlXlsTable

import unittest
from create_test_odmls import create_small_test_odml
from create_test_odmls import create_showall_test_odml
import os


class TestLoadOdmlFromTable(unittest.TestCase):

    def setUp(self):
        self.test_table = OdmlTable()
        self.filename = 'testtable'
        self.filetype = ''

    def tearDown(self):
        pass

    def test_load_from_csv(self):
        self.filetype = 'csv'
        table = OdmlCsvTable()
        table.load_from_function(create_small_test_odml)
        dict_in = [{key: dic[key] if dic[key] is not None
                    else '' for key in dic} for dic in table._odmldict]
        table.change_header(Path=1, SectionName=2, SectionType=3,
                            SectionDefinition=4, PropertyName=5,
                            PropertyDefinition=6, Value=7, ValueDefinition=8,
                            DataUnit=9, DataUncertainty=10, odmlDatatype=11)
        table.write2file(self.filename + '.' + self.filetype)
        self.test_table.load_from_csv_table(self.filename + '.' +
                                            self.filetype)
        dict_out = self.test_table._odmldict
        self.assertEquals(dict_in, dict_out)

    def test_load_from_xls(self):
        self.filetype = 'xls'
        table = OdmlXlsTable()
        table.load_from_function(create_small_test_odml)
        dict_in = [{key: dic[key] if dic[key] is not None
                    else '' for key in dic} for dic in table._odmldict]
        table.change_header(Path=1, SectionName=2, SectionType=3,
                            SectionDefinition=4, PropertyName=5,
                            PropertyDefinition=6, Value=7, ValueDefinition=8,
                            DataUnit=9, DataUncertainty=10, odmlDatatype=11)
        table.write2file(self.filename + '.' + self.filetype)
        self.test_table.load_from_xls_table(self.filename + '.' +
                                            self.filetype)
        dict_out = self.test_table._odmldict
        self.assertEquals(dict_in, dict_out)


class TestLoadSaveOdml(unittest.TestCase):
    """
    class to test loading the odml
    """

    def setUp(self):
        self.test_table = OdmlTable()
        self.expected_odmldict = [{'PropertyDefinition': None,
                                   'SectionName': 'section1',
                                   'PropertyName': 'property1',
                                   'Value': 'bla',
                                   'odmlDatatype': 'text',
                                   'DataUnit': None,
                                   'SectionType': 'undefined',
                                   'ValueDefinition': None,
                                   'DataUncertainty': None,
                                   'SectionDefinition': None,
                                   'Path': '/section1'}]

    def test_load_from_file(self):
        """
        test loading the odml-dictionary from an odml-file
        """
        filename = 'tmp_testfile.odml'
        doc = create_small_test_odml()
        odml.tools.xmlparser.XMLWriter(doc).write_file(filename)
        self.test_table.load_from_file(filename)
        os.remove(filename)
        self.assertEqual(self.test_table._odmldict, self.expected_odmldict)

    def test_load_from_function(self):
        """
        test loading the odml-dictionary from a function that generates an
        odml-document in python
        """
        self.test_table.load_from_function(create_small_test_odml)
        self.assertEqual(self.test_table._odmldict, self.expected_odmldict)

    def test_load_from_odmldoc(self):
        """
        test loading the odml-dictionary from an odml-document in python
        """
        doc = create_small_test_odml()
        self.test_table.load_from_odmldoc(doc)
        self.assertEqual(self.test_table._odmldict, self.expected_odmldict)

    def test_write2odml(self):
        """
        test writing the odmldict back to an odml-file
        """
        file1 = 'test.odml'
        file2 = 'test2.odml'
        doc = create_showall_test_odml()
        self.test_table.load_from_odmldoc(doc)
        odml.tools.xmlparser.XMLWriter(doc).write_file(file1)

        self.test_table.change_header(Path=1, SectionName=2, SectionType=3,
                                      SectionDefinition=4, PropertyName=5,
                                      PropertyDefinition=6, Value=7,
                                      ValueDefinition=8, DataUnit=9,
                                      DataUncertainty=10, odmlDatatype=11)
        self.test_table.write2odml(file2)

        self.test_table.load_from_file(file1)
        expected = self.test_table._odmldict
        self.test_table.load_from_file(file2)
        self.assertEqual(expected, self.test_table._odmldict)

        os.remove(file1)
        os.remove(file2)


class TestChangeHeader(unittest.TestCase):

    def setUp(self):
        self.test_table = OdmlTable()

    def test_simple_change(self):
        """
        Tests simple changing of the header
        """
        self.test_table.change_header(Path=1, SectionType=2, Value=3)
        self.assertEqual(self.test_table._header, ["Path", "SectionType",
                                                   "Value"])

    def test_index_zero(self):
        """
        Test change_header with using the index 0
        """
        # TODO: change as exception is changed
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=0, SectionType=1, Value=2)

    def test_negative_index(self):
        """
        Test change_header with using a negative index
        """
        # TODO: change Exception
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=-1)

    def test_empty_cols_allowed(self):
        """
        Test change_header leaving empty columns, while it is allowed
        """
        self.test_table.allow_empty_columns = True
        self.test_table.change_header(Path=1, SectionType=3, Value=4)
        self.assertEqual(self.test_table._header, ["Path", None, "SectionType",
                                                   "Value"])

    def test_empty_cols_forbidden(self):
        """
        Test change_header leaving empty columns, while this is forbidden
        """
        self.test_table.allow_empty_columns = False
        # TODO: exception
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=1, SectionType=3, Value=4)

    def test_same_indizes(self):
        """
        Test change_header with two columns with same indizes
        """
        # TODO: Exception
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=1, SectionType=1, Value=2)

    def test_wrong_keyword(self):
        """
        Test using change_header with a wrong keyword
        """
        # TODO: Exception
        with self.assertRaises(Exception):
            self.test_table.change_header(Path=1, Sectionname=2, Value=3)


class TestOdmlTable(unittest.TestCase):
    """
    class to test the other functions of the OdmlTable-class
    """

    def setUp(self):
        self.test_table = OdmlTable()

    def test_change_titles(self):
        """
        changing the header_titles
        """
        expected = {"Path": "Pfad",
                    "SectionName": "Section Name",
                    "SectionType": "Section Type",
                    "SectionDefinition": "Section Definition",
                    "PropertyName": "Eigenschaft",
                    "PropertyDefinition": "Property Definition",
                    "Value": "Wert",
                    "ValueDefinition": "Value Definition",
                    "DataUnit": "Einheit",
                    "DataUncertainty": "Data Uncertainty",
                    "odmlDatatype": "Datentyp"}
        self.test_table.change_header_titles(Path="Pfad",
                                             PropertyName="Eigenschaft",
                                             Value="Wert", DataUnit="Einheit",
                                             odmlDatatype="Datentyp")
        self.assertEqual(self.test_table._header_titles, expected)

    def test_change_allow_free_cols(self):
        """
        set allow_free_columns
        """

        self.test_table.allow_empty_columns = True
        self.assertEqual(self.test_table._allow_empty_columns, True)
        self.test_table.allow_empty_columns = False
        self.assertEqual(self.test_table._allow_empty_columns, False)
        # TODO: Exception
        with self.assertRaises(Exception):
            self.test_table.allow_empty_columns = 4

    def test_forbid_free_cols(self):
        """
        test forbidding free columns while there are already free columns in
        the header
        """

        self.test_table.allow_empty_columns = True
        self.test_table.change_header(Path=1, PropertyDefinition=3, Value=4)
        # TODO: Exception aendern
        with self.assertRaises(Exception):
            self.test_table.allow_empty_columns = False


if __name__ == '__main__':
    unittest.main()
