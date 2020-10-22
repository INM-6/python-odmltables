# -*- coding: utf-8 -*-
"""

"""

import odml
import datetime
from .odml_csv_table import OdmlCsvTable
from .odml_xls_table import OdmlXlsTable
from .odml_table import OdmlTable
from .compare_section_table import CompareSectionTable
from .compare_section_csv_table import CompareSectionCsvTable
from .compare_section_xls_table import CompareSectionXlsTable


def create_odmltable_example():
    """

    """

    species = ''
    gender = ''
    weight = 0.0
    start_date = datetime.date(1, 2, 3)
    end_date = datetime.date(1, 2, 3)
    duration = 1

    doc = odml.Document()
    doc.append(odml.Section(name='Subject',
                            definition='Information on the investigated '
                                       'experimental subject (animal or '
                                       'person)'))
    parent = doc['Subject']

    parent.append(odml.Section(name='Training',
                               definition='Information on the training given '
                                          'to subject'))

    parent.append(odml.Property(name='Species',
                                definition='Binomial species name',
                                values=species,
                                dtype=odml.DType.string))

    parent.append(odml.Property(name='Gender',
                                definition='Gender (male or female)',
                                values=gender,
                                dtype=odml.DType.string))

    parent.append(odml.Property(name='Weight',
                                values=weight,
                                dtype=odml.DType.float,
                                unit='kg',
                                uncertainty=5))

    parent = doc['Subject']['Training']
    parent.append(odml.Property(name='PeriodStart',
                                definition='start date of training',
                                values=start_date,
                                dtype=odml.DType.date))

    parent.append(odml.Property(name='PeriodEnd',
                                definition='end date of training',
                                values=end_date,
                                dtype=odml.DType.date))

    parent.append(odml.Property(name='Duration',
                                definition='Duration of the training',
                                values=duration,
                                dtype=odml.DType.int,
                                unit='work days'))
    return doc


def create_electrode_example():
    """
    """

    electrode_type = 'Utah Array'
    count = 10
    electrode_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    impedance = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 40-50
    length = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 2mm-2cm
    suaids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # between 1 and 4

    doc = odml.Document()

    doc.append(odml.Section(name='Multielectrode Array'))

    parent = doc['Multielectrode Array']

    parent.append(odml.Property(name='Type', values=electrode_type))

    parent.append(odml.Section(name='Electrodes'))
    parent = doc['Multielectrode Array']['Electrodes']
    parent.append(odml.Property(name='count', values=count))

    for i in list(range(count)):
        parent = doc['Multielectrode Array']
        sec_name = 'Electrode' + str(i + 1)
        parent.append(odml.Section(name=sec_name))
        parent = doc['Multielectrode Array'][sec_name]
        parent.append(odml.Property(name='ID',
                                    definition='Electrode ID',
                                    values=electrode_id[i]))
        parent.append(odml.Property(name='Impedance',
                                    definition='Pre-implantation impedance',
                                    values=impedance[i]))
        parent.append(odml.Property(name='Length',
                                    definition='Length',
                                    values=length[i]))
        parent.append(odml.Property(name='SUAIDs',
                                    definition='ID of single units',
                                    values=suaids[i]))

    return doc


def create_mice_example():
    """
    """
    weight = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    body = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    tail = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    fur = 3
    eye = 13

    doc = odml.Document()

    for i in list(range(10)):
        sec_name = 'day' + str(i * 2)

        doc.append(odml.Section(name=sec_name))
        parent = doc[sec_name]
        parent.append(odml.Property(name='weight', values=weight[i]))
        parent.append(odml.Property(name='body length', values=body[i]))
        parent.append(odml.Property(name='tail length', values=tail[i]))
        parent.append(odml.Property(name='fur', values=(2 * i >= fur)))
        parent.append(odml.Property(name='eye opening', values=(2 * i >= eye)))

    return doc


if __name__ == "__main__":
    folder = '../data/examples/'

    ################## csv examples #######################

    # save the first odml as 'testfile.odml'
    #    doc = create_odmltable_example()
    #    odml.tools.xmlparser.XMLWriter(doc).write_file(folder +
    # 'testfile.odml')
    #
    #    # first example - create the first table
    #    myFirstTable = OdmlCsvTable()
    #    myFirstTable.load_from_file(folder + 'testfile.odml')
    #    myFirstTable.write2file(folder + 'testtable.csv')
    #
    #    # second example - change header titles
    #    myFirstTable.change_header_titles(Path='my path',
    #                                      PropertyName='my property',
    #                                      Value='my value',
    #                                      odmlDatatype='my datatype')
    #
    #    myFirstTable.write2file(folder + 'testtable2.csv')
    #
    #    # third example - change the header
    #    myFirstTable.change_header(Path=1,
    #                               SectionName=2,
    #                               SectionDefinition=3,
    #                               PropertyName=4,
    #                               Value=5)
    #
    #    myFirstTable.write2file(folder + 'testtable3.csv')
    #
    #    # fourth example - allow empty columns
    #    myFirstTable.allow_empty_columns = True
    #    myFirstTable.change_header(Path=1,
    #                               PropertyName=3,
    #                               Value=4,
    #                               SectionDefinition=7,
    #                               DataUncertainty=8)
    #    myFirstTable.write2file(folder + 'testtable4.csv')
    #
    #    # examples for 'showall'-attributes
    #
    #    myFirstTable.change_header(Path=1,
    #                               SectionDefinition=2,
    #                               PropertyName=3,
    #                               PropertyDefinition=4,
    #                               Value=5)
    #
    #    myFirstTable.show_all_properties = True
    #    myFirstTable.show_all_sections = True
    #    myFirstTable.write2file(folder + 'showall1.csv')
    #
    #    myFirstTable.show_all_properties = True
    #    myFirstTable.show_all_sections = False
    #    myFirstTable.write2file(folder + 'showall2.csv')
    #
    #    myFirstTable.show_all_properties = False
    #    myFirstTable.show_all_sections = False
    #    myFirstTable.write2file(folder + 'showall3.csv')
    #
    #    ##################### xls examples #######################
    #
    #    # create a xls table
    #    myXlsTable = OdmlXlsTable()
    #    myXlsTable.load_from_function(create_odmltable_example)
    #    myXlsTable.write2file(folder + 'testtable0.xls')
    #
    #    # first example - change a style
    #    myXlsTable.first_style.backcolor = 'gray25'
    #    myXlsTable.first_style.fontcolor = 'black'
    #    myXlsTable.first_style.fontstyle = ''
    #
    #    myXlsTable.second_style.backcolor = 'gray50'
    #    myXlsTable.second_style.fontcolor = 'black'
    #    myXlsTable.second_style.fontstyle = ''
    #
    #    myXlsTable.first_marked_style.backcolor = 'ice_blue'
    #    myXlsTable.first_marked_style.fontcolor = 'white'
    #    myXlsTable.first_marked_style.fontstyle = ''
    #
    #    myXlsTable.second_marked_style.backcolor = 'periwinkle'
    #    myXlsTable.second_marked_style.fontcolor = 'white'
    #    myXlsTable.second_marked_style.fontstyle = ''
    #
    #    myXlsTable.write2file(folder + 'testtable1.xls')
    #
    #    # second example - mark columns
    #    myXlsTable.mark_columns('Path', 'Value')
    #    myXlsTable.write2file(folder + 'testtable2.xls')
    #
    #    # adjust changing point
    #
    #    myXlsTable.changing_point = 'sections'
    #    myXlsTable.write2file(folder + 'change_sections.xls')
    #
    #    myXlsTable.changing_point = 'properties'
    #    myXlsTable.write2file(folder + 'change_properties.xls')
    #
    #    myXlsTable.changing_point = 'values'
    #    myXlsTable.write2file(folder + 'change_values.xls')
    #
    #    myXlsTable.changing_point = None
    #    myXlsTable.write2file(folder + 'change_none.xls')
    #
    #    # chessfield pattern
    #
    #    myXlsTable.changing_point = 'properties'
    #    myXlsTable.pattern = 'chessfield'
    #    myXlsTable.write2file(folder + 'chessfield.xls')

    #####################
    ##compare sections ##
    #####################

    ############ csv #######################

    # examples mice
    odml.tools.xmlparser.XMLWriter(create_mice_example()).write_file(
        folder + 'mice_example.odml')

    #    csv_mice = OdmlCsvTable()
    #    csv_mice.load_from_file(folder + 'mice_example.odml')
    #    csv_mice.write2file(folder + 'mice1.csv')
    #
    #    compare_mice_csv = CompareSectionCsvTable()
    #    compare_mice_csv.load_from_file(folder + 'mice_example.odml')
    #
    #    compare_mice_csv.choose_sections('day0', 'day2', 'day4')
    #    compare_mice_csv.write2file(folder + 'comparemice2.csv')
    #
    #    compare_mice_csv.choose_sections_startwith('day')
    #    compare_mice_csv.write2file(folder + 'comparemice.csv')
    #
    #    compare_mice_csv.switch = True
    #    compare_mice_csv.write2file(folder + 'comparemice3.csv')
    #
    #    compare_mice_csv.include_all = True
    #    compare_mice_csv.write2file(folder + 'mice_include_true.csv')
    #    compare_mice_csv.include_all = False
    #    compare_mice_csv.write2file(folder + 'mice_include_false.csv')

    # examples electrodes
    odml.tools.xmlparser.XMLWriter(create_electrode_example()).write_file(
        folder + 'electrodes_example.odml')

    #    csv_electrodes = OdmlCsvTable()
    #    csv_electrodes.load_from_file(folder + 'electrodes_example.odml')
    #    csv_electrodes.write2file(folder + 'electrodes1.csv')
    #
    #    compare_electrodes_csv = CompareSectionCsvTable()
    #    compare_electrodes_csv.load_from_file(folder +
    # 'electrodes_example.odml')
    #
    #    compare_electrodes_csv.choose_sections('Electrode1', 'Electrode2',
    # 'Electrode3')
    #    compare_electrodes_csv.write2file(folder + 'compareelectrodes2.csv')
    #
    #    compare_electrodes_csv.choose_sections_startwith('Electrode')
    #    compare_electrodes_csv.write2file(folder + 'compareelectrodes.csv')
    #
    #    compare_electrodes_csv.switch = True
    #    compare_electrodes_csv.write2file(folder + 'compareelectrodes3.csv')
    #
    #    compare_electrodes_csv.include_all = True
    #    compare_electrodes_csv.write2file(folder + 'electrodes_include_true.csv')
    #    compare_electrodes_csv.include_all = False
    #    compare_electrodes_csv.write2file(folder + 'electrodes_include_false.csv')

    # xls
    xls_electrodes = CompareSectionXlsTable()
    xls_electrodes.load_from_file(folder + 'electrodes_example.odml')
    xls_electrodes.choose_sections_startwith("Electrode")
    xls_electrodes.write2file(folder + 'electrodes1.xls')
