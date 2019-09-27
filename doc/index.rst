.. python-odmltables documentation master file, created by
   sphinx-quickstart on Mon Aug 17 13:22:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**************************************************************
odMLtables - Table-based editing of odML metadata collections
**************************************************************

Synopsis
=========

*odMLtables* is a tool to support working with metadata collections for electrophysiological data and is described in detail in `Sprenger et al. (2019) odMLtables: A User-Friendly Approach for Managing Metadata of Neurophysiological Experiments`_.

The odML_ file format and library API provides a means to store hierarchical metadata collections for electrophysiological data. Such collections typically consist of a large number of key-value pairs organized by a hierarchy of sections (see `Grewe et al. (2011) Frontiers in Neuroinformatics 5:16`_). However, for editing and viewing metadata the use of standard spreadsheet software offering a flat tabular representation of a selected subset of metadata is desireable (cf., `Zehl et al. (2016) Frontiers in Neuroinformatics 10:26`_). *odMLtables* provides a set of library functions as well as a graphical user interface that offers to swtich between hierarchical and flat representations of their metadata collection, and provides functions that assist in working with these files.

Currently, odMLtables supports:

- converting metadata collections between the hierarchical odML format and table-based representations (i.e., xls, csv)
- creating a new table for starting a metadata collection
- comparing sections within a metadata collections
- filtering metadata collections to extract a specific subcollection
- merging multiple metadata collections into one file


Contents:
=========

.. toctree::
    :maxdepth: 1

    install
    tutorial
    modules
    whatisnew
    authors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Citation
========
If you are using *odMLtables* for your project please consider citing

`Sprenger J, Zehl L, Pick J, Sonntag M, Grewe J, Wachtler T, Grün S and Denker M (2019) odMLtables: A User-Friendly Approach for Managing Metadata of Neurophysiological Experiments. Front. Neuroinform. 13:62. doi: 10.3389/fninf.2019.00062`_

.. _`Sprenger et al. (2019) odMLtables: A User-Friendly Approach for Managing Metadata of Neurophysiological Experiments`: https://doi.org/10.3389/fninf.2019.00062
.. _`Sprenger J, Zehl L, Pick J, Sonntag M, Grewe J, Wachtler T, Grün S and Denker M (2019) odMLtables: A User-Friendly Approach for Managing Metadata of Neurophysiological Experiments. Front. Neuroinform. 13:62. doi: 10.3389/fninf.2019.00062`: https://doi.org/10.3389/fninf.2019.00062
.. _`odML`: http://www.g-node.org/projects/odml
.. _`Grewe et al. (2011) Frontiers in Neuroinformatics 5:16`: http://dx.doi.org/10.3389/fninf.2011.00016
.. _`Zehl et al. (2016) Frontiers in Neuroinformatics 10:26`: http://dx.doi.org/10.3389/fninf.2016.00026

.. |date| date::
.. |time| date:: %H:%M
