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
    parent.append(odml.Property(name='property1', value=[1, 2, 2]))

    parent = doc['section2']
    parent.append(odml.Property(name='property1', value=2))

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
    parent.append(odml.Property(name='property1', definition='prop1', value=
                                [odml.Value(data='value1',
                                            dtype=odml.DType.string,
                                            unit='g',
                                            uncertainty=1),
                                 odml.Value(data='value2',
                                            dtype=odml.DType.string,
                                            unit='g',
                                            uncertainty=1),
                                 odml.Value(data='value3',
                                            dtype=odml.DType.text,
                                            unit='g',
                                            uncertainty=1)]))

    parent.append(odml.Property(name='property2', definition='prop2', value=
                  odml.Value(data='value1',
                             dtype=odml.DType.text,
                             unit='g',
                             uncertainty=1)))
    parent.append(odml.Property(name='property3', definition='prop3', value=
                  odml.Value(data='value1',
                             dtype=odml.DType.text,
                             unit='g',
                             uncertainty=1)))

    parent = doc['section2']
    parent.append(odml.Property(name='property1', definition='prop1', value=
                  odml.Value(data='value1',
                             dtype=odml.DType.string,
                             unit='g',
                             uncertainty=1)))

    parent = doc['section3']
    parent.append(odml.Property(name='property1', definition='prop1', value=
                  [odml.Value(data='value1',
                              dtype=odml.DType.string,
                              unit='g',
                              uncertainty=1),
                   odml.Value(data='value2',
                              dtype=odml.DType.string,
                              unit='g',
                              uncertainty=2)]))

    return doc


def create_small_test_odml():
    """
    creates a small odml-document with only one section, property and value
    """

    doc = odml.Document()

    doc.append(odml.Section(name='section1'))

    parent = doc['section1']

    parent.append(odml.Property(name='property1',
                                value=odml.Value(data='bla',
                                                 dtype=odml.DType.text)))

    return doc


def create_datatype_test_odml():
    """
    create an odml-document using every odml-datatype at least once
    """

    # data that will be written in the odml-document
    int_values = [odml.Value(data=-10,
                             dtype=odml.DType.int,
                             definition='a negative test int'),
                  odml.Value(data=0,
                             dtype=odml.DType.int,
                             definition='test int null'),
                  odml.Value(data=10,
                             dtype=odml.DType.int,
                             definition='a positive test int')]

    float_values = [odml.Value(data=-1.234,
                               dtype=odml.DType.float,
                               definition='a negative test float'),
                    odml.Value(data=0.0,
                               dtype=odml.DType.float,
                               definition='test float null'),
                    odml.Value(data=1.234,
                               dtype=odml.DType.float,
                               definition='a positive test float')]

    bool_values = ['true', 'false', 'True', 'False', 't', 'f', 'T', 'F', 1, 0]

    text_value = "this is a text. It is longer than a string and contains " +\
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
                                value=int_values,
                                definition='contains different int-values'))

    parent.append(odml.Property(name='Float',
                                value=float_values,
                                definition='contains different float-values'))

    parent = doc['texts']

    parent.append(odml.Section(name='datetime'))
    parent.append(odml.Section(name='string-like'))

    parent = doc['texts']['datetime']
    parent.append(odml.Property(name='Datetime',
                                value=odml.Value(data=datetime_value,
                                                 dtype=odml.DType.datetime)))
    parent.append(odml.Property(name='Date',
                                value=odml.Value(data=date_value,
                                                 dtype=odml.DType.date)))

    parent.append(odml.Property(name='Time',
                                value=odml.Value(data=time_value,
                                                 dtype=odml.DType.time)))

    parent = doc['texts']['string-like']

    parent.append(odml.Property(name='String',
                                value=odml.Value(data='this is a string',
                                                 dtype=odml.DType.string)))
    parent.append(odml.Property(name='Text',
                                value=odml.Value(data=text_value,
                                                 dtype=odml.DType.text)))

    parent.append(odml.Property(name='Person',
                                value=odml.Value(data='Jana Pick',
                                                 dtype=odml.DType.person)))

    parent = doc['other']

    parent.append(odml.Property(name='Boolean',
                                value=[odml.Value(data=data,
                                                  dtype=odml.DType.boolean)
                                       for data in bool_values]))
    return doc


def create_compare_test(sections=3, properties=3,levels=1):
    """
    """

    doc = odml.Document()

    def append_children(sec,level):
        if level < levels:
            for i in range(sections):
                sec.append(odml.Section(name='Section' + str(i+1)))
                parent = sec['Section' + str(i+1)]
                append_children(parent,level+1)
                if(i != 2):
                    for j in range(properties):
                        parent.append(odml.Property(name='Property' + str(j+1), value= i+j))
                else:
                    for j in range(properties-2):
                        parent.append(odml.Property(name='Property' + str(j+1), value= i+j))
                    parent.append(odml.Property(name='Property' + str(properties), value= i+properties-1))

    # sec = doc
    # for l in range(levels):
    #     for i in range(sections):
    #         doc.append(odml.Section(name='Section' + str(i+1)))
    #         parent = doc['Section' + str(i+1)]
    #         if(i != 2):
    #             for j in range(properties):
    #                 parent.append(odml.Property(name='Property' + str(j+1), value= i+j))
    #         else:
    #             for j in range(properties-2):
    #                 parent.append(odml.Property(name='Property' + str(j+1), value= i+j))
    #             parent.append(odml.Property(name='Property' + str(properties), value= i+properties-1))


    append_children(doc,0)

    doc.append(odml.Section(name='One more Section'))
    parent = doc['One more Section']
    parent.append(odml.Property(name='Property2', value=11))

    return doc





