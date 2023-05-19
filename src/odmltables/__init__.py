import importlib.metadata
# this need to be at the begining because some sub module will need the version
__version__ = importlib.metadata.version("odmltables")
VERSION = __version__

# -*- coding: utf-8 -*-
"""
:mod:`odmltables` provides classes for manipulation and conversion of odML files.

Classes:
.. autoclass:: odmltables.odml_table.OdmlTable
.. autoclass:: odmltables.odml_csv_table.OdmlCsvTable
.. autoclass:: odmltables.odml_xls_table.OdmlXlsTable
.. autoclass:: odmltables.compare_section_csv_table.CompareSectionCsvTable
"""

from odmltables.odml_csv_table import OdmlCsvTable
