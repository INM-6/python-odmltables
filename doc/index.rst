.. python-odmltables documentation master file, created by
   sphinx-quickstart on Mon Aug 17 13:22:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**************************************************************
odML-tables - Table-based editing of odML metadata collections
**************************************************************

Synopsis
=========

*odML-tables* is a tool to support working with metadata collections for electrophysiological data. 

The odML_ file format and library API provides a means to store hierarchical metadata collections for electrophysiological data. Such collections typically consist of a large number of key-value pairs organized by a hierarchy of sections (see `Grewe et al, 2011, Frontiers in Neuroinformatics 5, 16`_). However, for editing and viewing metadata the use of standard spreadsheet software offering a flat tabular representation of a selected subset of metadata is desireable. *odML-tables* provides a set of library functions as well as a graphical user interface that offers to swtich between hierarchical and flat representations of their metadata collection, and provides functions that assist in working with these files.

Currently, odML-tables supports:

- converting metadata collections between the hierarchical odML format and table-based representations (i.e., xls, csv)
- creating an empty template for starting a new metadata collection
- comparing sections within a metadata collections
- filtering metadata collections to extract a specific subcollection
- merging multiple metadata collections into one file


Contents:
=========

.. toctree::
    :maxdepth: 1

    introduction
    install
    tutorial
    documentation
    authors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _`odML`: http://www.g-node.org/projects/odml
.. _`Grewe et al, 2011, Frontiers in Neuroinformatics 5, 16`: http://dx.doi.org/10.3389/fninf.2011.00016

.. |date| date::
.. |time| date:: %H:%M
