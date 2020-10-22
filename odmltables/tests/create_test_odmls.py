# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:48:12 2015

@author: pick
"""
import odml
import datetime


def create_2samerows_test_odml():
    """
    creates an odml-document in which there is a property with two same values
    to create a table with two rows that are the same
    """

    doc = odml.Document()
    doc.append(odml.Section(name='section1'))
    doc.append(odml.Section(name='section2'))

    parent = doc['section1']
    parent.append(odml.Property(name='property1', values=[1, 2, 2]))

    parent = doc['section2']
    parent.append(odml.Property(name='property1', values=2))

    return doc


def create_showall_test_odml():
    """
    creates a test-odml-document specifically to test the 'showall'-attributes
    (showall_sections, showall_properties, showall_value_information) to test
    if the right cells are left free
    """
    doc = odml.Document()

    doc.append(odml.Section(name='section1', definition='sec1'))
    doc.append(odml.Section(name='section2', definition='sec2'))
    doc.append(odml.Section(name='section3', definition='sec3'))

    parent = doc['section1']
    parent.append(odml.Property(name='property1', definition='prop1',
                                values=['value1', 'value2', 'value3'],
                                dtype=odml.DType.string,
                                unit='g',
                                uncertainty=1))

    parent.append(odml.Property(name='property2', definition='prop2',
                                values='value1',
                                dtype=odml.DType.text,
                                unit='g',
                                uncertainty=1))
    parent.append(odml.Property(name='property3', definition='prop3',
                                values='value1',
                                dtype=odml.DType.text,
                                unit='g',
                                uncertainty=1))

    parent = doc['section2']
    parent.append(odml.Property(name='property1', definition='prop1',
                                values='value1',
                                dtype=odml.DType.string,
                                unit='g',
                                uncertainty=1))

    parent = doc['section3']
    parent.append(odml.Property(name='property1', definition='prop1',
                                values=['value1', 'value2'],
                                dtype=odml.DType.string,
                                unit='g',
                                uncertainty=1
                                ))

    return doc


def create_small_test_odml():
    """
    creates a small odml-document with only one section, property and value
    """

    doc = odml.Document()

    doc.append(odml.Section(name='section1'))

    parent = doc['section1']

    parent.append(odml.Property(name='property1',
                                values='bla',
                                dtype=odml.DType.text))

    return doc


def create_datatype_test_odml():
    """
    create an odml-document using every odml datatype at least once
    """

    # data that will be written in the odml-document
    int_values = [-10, 0, 10]

    float_values = [-1.234, 0.0, 1.234]

    bool_values = ['true', 'false', 'True', 'False', 't', 'f', 'T', 'F', 1, 0]

    text_value = "this is a text. It is longer than a string and contains " + \
                 "punctuation marks!"
    datetime_value = datetime.datetime(2014, 12, 11, 15, 2, 0)
    date_value = datetime.date(2014, 12, 11)
    time_value = datetime.time(15, 2, 0)

    # create a new odml document
    doc = odml.Document(version='0.1')

    # create sections
    doc.append(odml.Section(name='numbers'))
    doc.append(odml.Section(name='texts'))
    doc.append(odml.Section(name='other'))

    # add subsections and properties
    parent = doc['numbers']

    parent.append(odml.Property(name='Integer',
                                values=int_values,
                                definition='contains different int-values'))

    parent.append(odml.Property(name='Float',
                                values=float_values,
                                definition='contains different float-values'))

    parent = doc['texts']

    parent.append(odml.Section(name='datetime'))
    parent.append(odml.Section(name='string-like'))

    parent = doc['texts']['datetime']
    parent.append(odml.Property(name='Datetime',
                                values=datetime_value,
                                dtype=odml.DType.datetime))
    parent.append(odml.Property(name='Date',
                                values=date_value,
                                dtype=odml.DType.date))

    parent.append(odml.Property(name='Time',
                                values=time_value,
                                dtype=odml.DType.time))

    parent = doc['texts']['string-like']

    parent.append(odml.Property(name='String',
                                values='this is a string',
                                dtype=odml.DType.string))
    parent.append(odml.Property(name='Text',
                                values=text_value,
                                dtype=odml.DType.text))

    parent.append(odml.Property(name='Person',
                                values='Jana Pick',
                                dtype=odml.DType.person))

    parent = doc['other']

    parent.append(odml.Property(name='Boolean',
                                values=bool_values,
                                dtype=odml.DType.boolean))
    return doc


def create_compare_test(sections=3, properties=3, levels=1):
    """
    """

    doc = odml.Document()

    def append_children(sec, level):
        if level < levels:
            for i in list(range(sections)):
                sec.append(odml.Section(name='Section' + str(i + 1)))
                parent = sec['Section' + str(i + 1)]
                append_children(parent, level + 1)
                if (i != 2):
                    for j in list(range(properties)):
                        parent.append(odml.Property(name='Property' + str(j + 1),
                                                    values=[i + j]))
                else:
                    for j in list(range(properties - 2)):
                        parent.append(odml.Property(name='Property' + str(j + 1),
                                                    values=[i + j]))
                    parent.append(odml.Property(name='Property' + str(properties),
                                                values=[i + properties - 1]))

    append_children(doc, 0)

    doc.append(odml.Section(name='One more Section'))
    parent = doc['One more Section']
    parent.append(odml.Property(name='Property2', values=[11]))

    return doc


def create_complex_test_odml():
    doc = odml.Document(version='0.0.x')
    doc.author = 'FirstName LastName'
    doc.date = datetime.date.today()
    doc.version = '0.0.x'
    doc.repository = '/myserver/myrepo'

    # APPEND MAIN SECTIONS
    doc.append(odml.Section(name='MySection',
                            type='<Enter the type of data you this section is'
                                 ' associated with, e.g. hardware>',
                            definition='<Describe the purpose of sections '
                                       'in short statements in this '
                                       'column.>'))
    doc.append(odml.Section(name='OneMoreSection',
                            type='<Enter the type of data you this section is'
                                 ' associated with, e.g. software>',
                            definition='<Use only the first cell in this '
                                       'column to for the section '
                                       'description.>'))

    parent = doc['OneMoreSection']
    parent.append(odml.Section('MySubsection',
                               type='<Enter the type of data you this section'
                                    ' is associated with, e.g. settings>',
                               definition='<Describe the purpose of this '
                                          'section here (eg. everything '
                                          'concerning the amplifier '
                                          'used...)'))

    # ADDING PROPERTIES
    parent = doc['MySection']
    parent.append(odml.Property(name='MyFirstProperty',
                                values='MyFirstValue',
                                dtype='str',
                                definition='<Enter a short definition of '
                                           'the property and the associated '
                                           'value described here>'))
    parent.append(odml.Property(name='OneMoreProperty',
                                values=[2.001, 4],
                                dtype='float',
                                unit='mm',
                                uncertainty=0.02,
                                definition='A section can have more than '
                                           'one property attached and a '
                                           'value can be of different type '
                                           'than string.'))

    parent = doc['OneMoreSection']
    parent.append(odml.Property(name='MyEmptyProperty',
                                values=-1,
                                dtype='int',
                                definition='This property contains an '
                                           'empty/default value.'
                                           'The integer value still '
                                           'contains the default value '
                                           '"-1", which can be highlighted '
                                           'using odml-tables.'))

    parent = doc['OneMoreSection']['MySubsection']
    parent.append(odml.Property(name='MyLastProperty',
                                values=datetime.datetime.today().date(),
                                dtype='date',
                                definition='You can define the hierarchical'
                                           ' location of a section via the'
                                           ' "path to section" column.'
                                           'The value contains todays date.'))
    return doc
