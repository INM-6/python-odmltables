# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:11:32 2015

@author: pick
"""

import copy
import os
import datetime

import odml
from odmltables.odml_table import OdmlTable
from odmltables.odml_table import OdmlDtypes
from odmltables.odml_csv_table import OdmlCsvTable
from odmltables.odml_xls_table import OdmlXlsTable

from .create_test_odmls import (create_small_test_odml, create_showall_test_odml,
                                create_compare_test)

import unittest


class TestLoadOdmlFromTable(unittest.TestCase):
    def setUp(self):
        self.test_table = OdmlTable()
        self.filename = 'testtable'
        self.filetype = ''

    def tearDown(self):
        for ext in ['.xls', '.odml', '.csv']:
            if os.path.exists(self.filename + ext):
                os.remove(self.filename + ext)

    def test_load_from_csv(self):
        self.filetype = 'csv'
        table = OdmlCsvTable()
        table.load_from_function(create_small_test_odml)
        dict_in = table._odmldict
        table.change_header(Path=1, SectionName=2, SectionType=3,
                            SectionDefinition=4, PropertyName=5,
                            PropertyDefinition=6, Value=7,
                            DataUnit=9, DataUncertainty=10, odmlDatatype=11)
        table.write2file(self.filename + '.' + self.filetype)
        self.test_table.load_from_csv_table(self.filename + '.' + self.filetype)
        dict_out = self.test_table._odmldict
        self.assertEqual(dict_in, dict_out)

    def test_load_from_xls(self):
        self.filetype = 'xls'
        table = OdmlXlsTable()
        table.load_from_function(create_small_test_odml)
        dict_in = table._odmldict
        table.change_header(Path=1, SectionName=2, SectionType=3,
                            SectionDefinition=4, PropertyName=5,
                            PropertyDefinition=6, Value=7,
                            DataUnit=8, DataUncertainty=9, odmlDatatype=10)
        table.write2file(self.filename + '.' + self.filetype)
        self.test_table.load_from_xls_table(self.filename + '.' + self.filetype)
        dict_out = self.test_table._odmldict
        self.assertEqual(dict_in, dict_out)

    def test_load_from_file(self):
        self.filetype = 'odml'
        table = OdmlTable()
        table.load_from_function(create_small_test_odml)
        dict_in = copy.deepcopy(table._odmldict)
        table.write2odml(self.filename + '.' + self.filetype)
        new_test_table = OdmlTable(self.filename + '.' + self.filetype)
        dict_out = new_test_table._odmldict

        self.assertEqual(dict_in, dict_out)

    def test_load_from_during_init(self):

        def generate_doc():
            doc = odml.Document()
            doc.append(odml.Section('mysection'))
            doc[0].append(odml.Property('myproperty', values=17))
            return doc

        # test loading from odml doc and odml doc generator
        OdmlTable(generate_doc())
        OdmlTable(generate_doc)

        # saving to test load_from with filepath
        # generate odml
        table = OdmlTable(generate_doc)
        table.write2odml(save_to=self.filename + '.odml')
        # generate xls
        table = OdmlXlsTable(generate_doc)
        table.write2file(save_to=self.filename + '.xls')
        # generate csv
        table = OdmlCsvTable(generate_doc)
        table.write2file(save_to=self.filename + '.csv')

        # loading from files
        OdmlTable(self.filename + '.odml')
        OdmlTable(self.filename + '.xls')
        OdmlTable(self.filename + '.csv')


class TestLoadSaveOdml(unittest.TestCase):
    """
    class to test loading the odml
    """

    def setUp(self):
        self.test_table = OdmlTable()
        self.expected_odmldict = [{'PropertyDefinition': None,
                                   'Value': ['bla'],
                                   'odmlDatatype': 'text',
                                   'DataUnit': None,
                                   'SectionType': 'n.s.',
                                   'DataUncertainty': None,
                                   'SectionDefinition': None,
                                   'Path': '/section1:property1'}]

    def test_load_from_file(self):
        """
        test loading the odml-dictionary from an odml-file
        """
        filename = 'tmp_testfile.odml'
        doc = create_small_test_odml()
        odml.tools.xmlparser.XMLWriter(doc).write_file(filename)
        self.test_table.load_from_file(filename)
        os.remove(filename)
        self.assertDictEqual(self.test_table._odmldict[0], self.expected_odmldict[0])

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
                                      PropertyDefinition=6, Value=7, DataUnit=9,
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
        self.assertListEqual(self.test_table._header, ["Path", "SectionType", "Value"])

    def test_shortcut_change(self):
        self.test_table.change_header('full')
        expected_entries = ['Path', 'SectionName', 'SectionType', 'SectionDefinition', 'PropertyName',
                          'PropertyDefinition', 'Value', 'DataUnit', 'DataUncertainty',
                          'odmlDatatype']
        self.assertEqual(len(self.test_table._header), len(expected_entries))
        for entry in expected_entries:
            self.assertIn(entry, self.test_table._header)


        self.test_table.change_header('minimal')
        self.assertListEqual(self.test_table._header, ['Path', 'PropertyName', 'Value',
                                                       'odmlDatatype'])

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
                    "DataUnit": "Einheit",
                    "DataUncertainty": "Data Uncertainty",
                    "odmlDatatype": "Datentyp"}
        self.test_table.change_header_titles(Path="Pfad",
                                             PropertyName="Eigenschaft",
                                             Value="Wert", DataUnit="Einheit",
                                             odmlDatatype="Datentyp")
        self.assertEqual(self.test_table._header_titles, expected)

    def test_merge_sections(self):
        # set up 2 odmls with partially overlapping sections
        doc1 = odml.Document(author='Me')
        doc2 = odml.Document(author='You')

        doc1.extend([odml.Section('MySection'), odml.Section('OurSection')])
        doc2.extend([odml.Section('YourSection'), odml.Section('OurSection')])

        # adding properties to sections, because odml is omitting sections without properties
        for sec in doc1.sections + doc2.sections:
            sec.append(odml.Property('prop'))

        table1 = OdmlTable(load_from=doc1)
        table2 = OdmlTable(load_from=doc2)

        table1.merge(table2, strict=False)

        result = table1.convert2odml()

        expected = ['MySection', 'OurSection', 'YourSection']
        self.assertListEqual([s.name for s in result.sections], expected)

    def test_merge_append_identical_value(self):
        doc1 = odml.Document()
        doc1.append(odml.Section('first sec'))
        doc1.sections[0].append(odml.Property('first prop', values=['value 1', 'value 2']))

        doc2 = odml.Document()
        doc2.append(odml.Section('first sec'))
        doc2.sections[0].append(odml.Property('first prop', values=['value 2', 'value 3']))

        self.test_table.load_from_odmldoc(doc1)
        self.test_table.merge(doc2, overwrite_values=False)

        self.assertEqual(len(self.test_table._odmldict[0]['Value']), 3)
        expected = doc1.sections[0].properties[0].values + doc2.sections[0].properties[0].values
        expected = list(set(expected))
        # comparing as set to disregard item order
        self.assertEqual(set(self.test_table._odmldict[0]['Value']), set(expected))


    def test_merge_overwrite_values_false(self):
        doc1 = odml.Document()
        doc1.append(odml.Section('first sec'))
        doc1.sections[0].append(odml.Property('first prop', values='first value'))

        doc2 = odml.Document()
        doc2.append(odml.Section('first sec'))
        doc2.sections[0].append(odml.Property('first prop', values='second value'))

        self.test_table.load_from_odmldoc(doc1)
        self.test_table.merge(doc2, overwrite_values=False)

        self.assertEqual(len(self.test_table._odmldict[0]['Value']), 2)
        self.assertEqual(self.test_table._odmldict[0]['Value'],
                         doc1.sections[0].properties[0].values + doc2.sections[0].properties[0].values)

    def test_merge_overwrite_values_true(self):
        doc1 = odml.Document()
        doc1.append(odml.Section('first sec'))
        doc1.sections[0].append(odml.Property('first prop', values='first value'))

        doc2 = odml.Document()
        doc2.append(odml.Section('first sec'))
        doc2.sections[0].append(odml.Property('first prop', values='second value'))

        self.test_table.load_from_odmldoc(doc1)
        self.test_table.merge(doc2, overwrite_values=True)

        self.assertEqual(len(self.test_table._odmldict[0]['Value']), 1)
        self.assertEqual(self.test_table._odmldict[0]['Value'][0],
                         doc2.sections[0].properties[0].values[0])


    def test_merge_update_docprops(self):
        doc1 = odml.Document(author='me', repository='somewhere', version=1.1,
                             date=None)
        doc2 = odml.Document(author='', repository='anywhere', version=1.1,
                             date=datetime.date.today())
        self.test_table.load_from_odmldoc(doc1)
        self.test_table.merge(doc2)

        self.assertEqual(self.test_table._docdict['author'], doc1.author)
        self.assertEqual(self.test_table._docdict['repository'], doc1.repository)
        self.assertEqual(self.test_table._docdict['version'], doc1.version)
        self.assertEqual(self.test_table._docdict['date'], doc2.date)


class TestFilter(unittest.TestCase):
    """
    class to test the other functions of the OdmlTable-class
    """

    def setUp(self):
        self.test_table = OdmlTable()
        self.test_table.load_from_odmldoc(create_compare_test(levels=2))

    def test_filter_errors(self):
        """
        test filter function for exceptions
        """

        with self.assertRaises(ValueError):
            self.test_table.filter()

        with self.assertRaises(ValueError):
            self.test_table.filter(mode='wrongmode', Property='Property')

    def test_filter_mode_and(self):
        """
        testing mode='and' setting of filter function
        """

        self.test_table.filter(mode='and', invert=False, SectionName='Section2',
                               PropertyName='Property2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(4, num_props_new)

    def test_filter_mode_or(self):
        """
        testing mode='or' setting of filter function
        """

        self.test_table.filter(mode='or', invert=False, SectionName='Section2',
                               PropertyName='Property2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(17, num_props_new)

    def test_filter_invert(self):
        """
        testing invert setting of filter function
        """

        num_props_original = len(self.test_table._odmldict)
        self.test_table.filter(mode='or', invert=True, SectionName='Section2',
                               PropertyName='Property2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(num_props_original - 17, num_props_new)

    def test_filter_recursive(self):
        """
        testing recursive setting of filter function
        """

        # total_number of properties
        doc = self.test_table.convert2odml()
        tot_props = len(list(doc.iterproperties()))
        sec2s = list(doc.itersections(filter_func=lambda x: x.name == 'Section2'))
        sec2_props = sum([len(list(sec.properties)) for sec in sec2s])

        # removing all sections with name 'Section2' independent of location in odml tree
        self.test_table.filter(mode='and', recursive=True, invert=True, SectionName='Section2')
        num_props_new = len(self.test_table._odmldict)

        self.assertEqual(tot_props - sec2_props, num_props_new)

    def test_filter_comparison_func_false(self):
        """
        keeping/removing all properties by providing True/False as comparison function
        """

        num_props_original = len(self.test_table._odmldict)
        self.test_table.filter(comparison_func=lambda x, y: True, PropertyName='')
        self.assertEqual(len(self.test_table._odmldict), num_props_original)

        self.test_table.filter(comparison_func=lambda x, y: False, PropertyName='')
        self.assertEqual(len(self.test_table._odmldict), 0)


class TestOdmlDtypes(unittest.TestCase):
    """
    class to test the other functions of the OdmlDtype-class
    """

    def setUp(self):
        self.test_dtypes = OdmlDtypes()

    def test_defaults(self):
        expected_basedtypes = list(self.test_dtypes.default_basedtypes)
        self.assertListEqual(sorted(expected_basedtypes), sorted(self.test_dtypes.basedtypes))

        expected_synonyms = self.test_dtypes.default_synonyms
        self.assertEqual(expected_synonyms, self.test_dtypes.synonyms)

    def test_valid_dtypes(self):
        expected_dtypes = (list(self.test_dtypes.default_basedtypes) +
                           list(self.test_dtypes.default_synonyms))
        self.assertListEqual(sorted(expected_dtypes), sorted(self.test_dtypes.valid_dtypes))

    def test_synonym_adder(self):
        basedtype, synonym = ('int', 'testsyn1')
        self.test_dtypes.add_synonym(basedtype, synonym)

        expected_synonyms = self.test_dtypes.default_synonyms.copy()
        expected_synonyms.update({synonym: basedtype})
        self.assertEqual(self.test_dtypes.synonyms, expected_synonyms)


if __name__ == '__main__':
    unittest.main()
