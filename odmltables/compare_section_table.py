# -*- coding: utf-8 -*-
"""

"""

import warnings
import datetime
import odml


class CompareSectionTable():
    """
    class to create a table in which you compare different sections of a odml-
    file wich have the same properties

    :param include_all: if set to false, only those properties which exist in
        every chosen section will be shown
    :param switch: when set to True, the table will be switched so the
        sections are in the rows and the properties in the columns
    :type include_all: bool
    :type switch: bool

    """

    def __init__(self):
        self.show_odml_warnings = False
        self._odmldoc = None
        self._sel_fun = lambda x: True
        self.include_all = True
        self.switch = False

    def _build_table(self):
        """
        function to build the table with the names of the sections in the
        header

        :return fieldnames: header of the table
        :return table: nested dictionary of the rows in the table
        :type fieldnames: list
        :type table: dictionary

        """

        properties = []
        sections = []
        table = []

        prop_num = 0
        sec_num = 0
        sec_ind = 0

        for sect in self._odmldoc.itersections(filter_func=self._sel_fun):
            sections.append(sect.name)
            for prop in sect.properties:
                if prop.name not in properties:
                    properties.append(prop.name)
        sec_num = len(sections)
        prop_num = len(properties)
        table = [[None for p in list(range(prop_num))] for s in list(range(sec_num))]

        for sect in self._odmldoc.itersections(filter_func=self._sel_fun):
            for prop in sect.properties:
                val = prop.values
                if val:
                    # for formatting reasons uncertainties and units are ignored for datetimes
                    if isinstance(val[0], (datetime.date, datetime.time, datetime.datetime)):
                        table[sec_ind][properties.index(prop.name)] = val[0]
                    else:
                        value, uncertainty, unit = str(val[0]), '', ''
                        if len(prop.values) > 1:
                            value += ', ...'
                        if prop.uncertainty:
                            uncertainty = '+-{})'.format(prop.uncertainty)
                            value = '({}'.format(value)
                        if prop.unit:
                            unit = prop.unit
                        table[sec_ind][properties.index(prop.name)] = '{}{}{}'.format(value,
                                                                                      uncertainty,
                                                                                      unit)
                    if len(prop.values) > 1:
                        # table[sec_ind][properties.index(prop.name)] += ', ...'
                        warnings.warn('Property %s contains %i values. Only showing first one in '
                                      'comparison table' % (prop.name, len(prop.values)))
            sec_ind += 1

        if self.include_all:
            pass
        else:
            to_delete = [properties[i] for i in list(range(len(table[0])))
                         if None in [s[i] for s in table]]
            for prop in to_delete:
                for section in table:
                    del section[properties.index(prop)]  # CHANGE!!
                properties.remove(prop)

        return properties, sections, table

    def load_from_file(self, load_from):
        """
        load the data for the table from an odml-file

        :param load_from: Name of the odml-file to load from
        :type load_from: string

        """
        self._odmldoc = odml.load(load_from, show_warnings=self.show_odml_warnings)
        # resolve links and includes
        self._odmldoc.finalize()

    def choose_sections_startwith(self, startwith):
        """
        choose all sections with the same beginning

        :param startwith: beginning of the sectionname of the sections that
            will be compared
        :type startwith: string

        """

        self._sel_fun = lambda x: x.name.startswith(startwith)

    # TODO: change from args to list for easier use of functions
    def choose_sections(self, *args):
        """
        choose all sections out of the list of sectionnames you give this
        function

        :param args: names of the sections
        :type args: strings

        :Example:

             a.choose_sections('section1', 'section2', 'section4')
        """
        self._sel_fun = lambda x: x.name in args

    def write2file(self, save_to):
        """
        write the table to the specific file

        :param save_to: path and name where the file will be saved
        :type save_to: string

        :raise NotImplementedError: Implemented in the subclass
        """
        # TODO: Error Message if no document loaded!!
        raise NotImplementedError()
