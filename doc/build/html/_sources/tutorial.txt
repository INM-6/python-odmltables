odMLtables Tutorial
===================

:Authors:
	Jana Pick and Lyuba Zehl
:Release:
	0.1
:License:
	Creative Commons Attribution-ShareAlike 4.0 International 
	`License <http://creativecommons.org/licenses/by-sa/4.0/>`_

In general there are two different kinds of tables you can create yet: a table with an overview of your whole odML or a table comparing different sections of the odML due to their properties. How they exactly look like will be shown later. But you should know, that only the first table can be converted back to an odML-file.

odML-table
***********

This table is basically just a flat version of the odML-file. Every row of the table represents a value of the odML (as you will see later, that does not mean you have to print every value) and gives all available information about this value. Those are:

* **Path** The Path to the Section next to the Value. Every Value belongs to exactly one Property, and every Property to exactly one Section. So, by giving the Path to the Section you automatically get the Path to the Value by adding the Name of the Property and the Value. This must be in the table, if you want to convert it back to an odML-file, otherwise it will be impossible to recreate the hierarchic structure of the odML.
* **SectionName** The Name of the Section next to the Value. This one is optional, as the name of the Section is already given in the Path.
* **SectionDefinition** The Definition of the Section next to the Value. This is an optional attribute in odML, so it is also optional in the table.
* **SectionType** The type of the Section.
* **PropertyName** The Name of the Property the Value belongs to. This one is not optional, if you want to convert the table back to an odML.
* **PropertyDefinition** The Definition of the Property. 
* **Value** The metadata-Value itself. A Property without Values cannot exist, so this has to be in the table to create an odML from it.
* **ValueDefinition** The definition of the Value (optional).
* **DataUnit** The Unit of the Value (optional).
* **DataUncertainty** The uncertainty of the Value (optional).
* **odmlDatatype** The odML data Type of the Value. This is important, because it might be different from the datatype in Python or Excel. This one must be given in the table if you want to convert it back to odML.

Those are many options, and in most cases you dont need all those information. The default columns of an odML-Table are 'Path', 'Property Name', 'Value' and 'odML Data Type', as those are the information needed to create an odML from the information in the table.



csv
+++

As already mentioned in the introduction there are different formats you can save your files to; at the moment those are csv or xls. Since xls provides much more possibilities concerning the appearance of the table we will start with the easier csv-format.


create the first table
----------------------

To create a csv table from an odML-file you have to import the class :class:`odml_csv_table.OdmlCsvTable`::

    from odml_csv_table import OdmlCsvTable

    myFirstTable = OdmlCsvTable()


Then you can load your odML-file::

    myFirstTable.load_from_file('testfile.odml')

Now you can already write it to a csv-file by using the following command::

    myFirstTable.write2file('testtable.csv')

You will get a table with the four columns; 'Path', 'Property Name', 'Value' and 'odML Data Type'.



load the odML
-------------

You can not only, as shown in the example above, load the odML from an odML-file. There are several other possibilities:

1. load from an :class:`odml.Document` (class of the odML-Python-library)::
    
    import odml    

    doc = odml.Document()
    # now append some sections, properties and values to the document    

    myTable = OdmlCsvTable()
    myTable.load_from_odmldoc(doc)

2. load from a python function that creates an :class:`odml.Document`::

    import odml

    def function1():
        doc = odml.Document()
        # now append some sections, properties and values to the document 
        
        return doc

    myTable = odmlCsvTable()
    myTable.load_from_function(function1)
        

3. load from a table (this option will be explained later)

changing the header
-------------------

Next step is to change the header in favor of your plans for the table. You can choose, which of the possible columns given above will be in the table and also what their name is. 

.. warning::
   If you miss out one of the columns 'Path', 'Property Name', 'Value' and 'odML Data Type' in your table, it cannot be converted back to an odML-file. Also, if you change the names of the columns you will have to use the same settings to convert it back. 

By using the function :func:`odml_table.OdmlTable.change_header_titles` you can choose an own title for every column::

    myFirstTable.change_header_titles(Path='my path', 
                                      PropertyName='my property', 
                                      Value='my value', 
                                      odmlDatatype='my datatype')

The table should now look exactly as the old one, with the only difference that the names of the columns have changed. If you want to print some more information, you can adjust this by using the function :func:`odml_table.OdmlTable.change_header`::

    myFirstTable.change_header(Path=1, 
                               SectionName=2, 
                               SectionDefinition=3, 
                               PropertyName=4, 
                               Value=5)

As you can see, in this function you can not only decide the columns but also their order, by giving them numbers from 1 on. If, for some reason, you want to have an empty column inside your table, you will have to set the option ``odml_table.OdmlTable.allow_empty_columns`` to True ::

    myFirstTable.allow_empty_columns = True

After this command, a code as the following should work fine::

    myFirstTable.change_header(Path=1, 
                               PropertyName=3, 
                               Value=4, 
                               SectionDefinition=7, 
                               DataUncertainty=8)

avoiding unnessaccery entries
-----------------------------

You might already have notized, that not every cell of the tables is filled. To make a table better humanreadable, some information about the Section (Path, SectionName and SectionDefinition) or the Property (PropertyName, PropertyDefinition) wont be printed in the table if they dont change. To change this behaviour use the options ``showall_sections`` and ``showall_properties``::

    myFirstTable.showall_sections = True
    myFirstTable.showall_properties = True

Now everything should be there.


xls
+++

All those functions already shown for the csv-table also work with xls. But there are some additional features concerning the Style of cells. First you need import the modul and create a new table::
    
    from odml_xls_table import OdmlXlsTable
    myXlsTable = OdmlXlsTable()



choosing styles
---------------

There are some styles you can easily change in the table. First, there is the style of the header. You can choose the backcolor and fontcolor and the style of the font::

    myXlsTable.header_style.backcolor = 'blue'
    myXlsTable.header_style.fontcolor = ''
    myXlsTable.header_style.fontstyle = 'bold 1'

The same way you can adapt the styles ``first_style`` and ``second_style``. Those are the styles used for the normal rows of the table. For a better overview there are those two styles, which are used alternating (for more information see section about `changing pattern`_.

You can find a table with all possible colors and their names :download:`here <colors.xls>`. 

marking columns
---------------

Sometimes there might be columns you want to lay a special focus on. So, to mark columns that they differ from the other, there is the option ``mark_columns``::

    myXlsTable.mark_columns('Path', 'Value')

Those marked columns will have a different style, which is determined by the attributes ``first_marked_style`` and ``second_marked_style`` (those can also be changed). 


changing pattern
----------------

By default the two different styles for the rows will alternate when a new section starts. But you can also change this behavior to a new property or a new value and, if you dont want different colors at all, just turn it off. This works by setting ``changing_point`` to either 'sections', 'properties', 'values' or None::

    myXlsTable.changing_point = 'values'

Also, for a better distinctness between the columns , you can choose a 'chessfield'- pattern, so the styles will switch with every row.::

    myXlsTable.pattern = 'chessfield'



table to compare sections
*************************

It might happen, that you have several sections with similar properties, for example TODO: example . To create a table, in which you can easily compare different sections of an odml, you can use this classes.

csv
+++

The easiest format here is, again, csv. So for the beginning, here is how you create a table to compare sections due to their properties in csv.

the beginning
----------------

to create a csv-file with the table, import the class::

    from compare_section_csv_table import CompareSectionCsvTable
    myCompareTable = CompareSectionCsvTable()

Now you can load the table::
    
    myCompareTable.load_from_file('somefile.odml')

choosing sections
-----------------

Next you have to decide, which sections of the table you want to compare. You can either just choose all sections out of a list of sectionnames or you can select all sections with a specific beginning::

    myCompareTable.choose_sections('s1', 's2', 's3') 
   
    # or

    myCompareTable.choose_sections_startwith('s')

You can already write this table to a file::

    myCompareTable.write2file('compare.csv')



switch the table
----------------

Now the section names should be in the header and the property names in the first column. This can be inverted by using the command ``switch``::

    myCompareTable.switch = True

This time the property names should be in the header and the names of the sections in the first column. For example if you have many sections to compare you might get a better overview by switching the table this way.


include all
-----------

If the sections you compare dont have exactly the same structure there might be properties appearing in one section but not in another. If you only want to compare those properties that are present in all of your chosen sections, use the option include_all::

    myCompareTable.include_all = False



xls
+++

In this part you will find the additional options for an xls-table.


first table
-----------

to create a new table use the command::

    from compare_section_xls_table import CompareSectionXlsTable()
    xlsCompareTable = CompareSectionXlsTable()


changing styles
---------------

there are different styles you can adjust in this table:

1. **headerstyle** The style used for the captions of rows and columns
2. **first_style** The style used for the values inside the table
3. **second_style** The second style used for the values inside the table
4. **missing_value_style** If ``include_all`` is True, this style will be used if a property doesnt exist in the section, so they distinguish from properties with empty values

You can, as already shown for the odml-table (`choosing styles`_), adjust backcolor, fontcolor and fontstyle for each of the styles. 














