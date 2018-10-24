import os.path

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION.txt')) as version_file:
    VERSION = version_file.read().strip()


# -*- coding: utf-8 -*-
"""
:mod:`odmltables` provides classes for manipulation and conversion of odML files.

Classes:
.. autoclass:: odmltables.odml_table.OdmlTable
.. autoclass:: odmltables.odml_csv_table.OdmlCsvTable
.. autoclass:: odmltables.odml_xls_table.OdmlXlsTable
.. autoclass:: odmltables.compare_section_csv_table.CompareSectionCsvTable
"""


from odmltables.odml_table import OdmlTable
from odmltables.odml_csv_table import OdmlCsvTable
from odmltables.odml_xls_table import OdmlXlsTable
from odmltables.compare_section_csv_table import CompareSectionCsvTable
from odmltables.compare_section_xls_table import CompareSectionXlsTable
