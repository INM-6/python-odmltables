# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:43:40 2015

@author: pick
"""
import odml
import csv
import datetime
import xlrd


class OdmlTable(object):
    """
    Class to create tables in different formats from odml-files


    :param show_all_sections: if set to False, information about the section
        like the path or name of the section wont be in the table again, if
        they are same as in the line before
    :param show_all_properties: if set to False, information about the property
        like the name or definition of the property wont be in the table again,
        if they are same as in the line before
    :param allow_empty_columns: if set to False it is forbidden to create
        tables with an emptycolumn
    :type show_all_sections: bool
    :type show_all_properties: bool
    :type allow_empty_columns: bool

    """

    def __init__(self):

        self._odmldict = None
        self._header = ["Path", "PropertyName", "Value", "odmlDatatype"]
        self._header_titles = {"Path": "Path to Section",
                               "SectionName": "Section Name",
                               "SectionType": "Section Type",
                               "SectionDefinition": "Section Definition",
                               "PropertyName": "Property Name",
                               "PropertyDefinition": "Property Definition",
                               "Value": "Value",
                               "ValueDefinition": "Value Definition",
                               "DataUnit": "Data Unit",
                               "DataUncertainty": "Data Uncertainty",
                               "odmlDatatype": "odML Data Type"}
        self.show_all_sections = False
        self.show_all_properties = False
        self._SECTION_INF = ["Path", "SectionName", "SectionType",
                             "SectionDefinition"]
        self._PROPERTY_INF = ["PropertyName", "PropertyDefinition"]
        # TODO: remove option
        self._allow_empty_columns = False

    def __create_odmldict(self, doc):
        """
        function to create the odml-dict
        """
        odmldict = [{'Path': v.parent.parent.get_path(),
                     'SectionName': v.parent.parent.name,
                     'SectionType': v.parent.parent.type,
                     'SectionDefinition': v.parent.parent.definition,
                     'PropertyName': v.parent.name,
                     'PropertyDefinition': v.parent.definition,
                     'Value': v.data if type(v.data) is not bool else
                     str(v.data),
                     'ValueDefinition': v.definition,
                     'DataUnit': v.unit,
                     'DataUncertainty': v.uncertainty,
                     'odmlDatatype': v.dtype}
                    for v in doc.itervalues()]
        return odmldict

    @property
    def allow_empty_columns(self):
        return self._allow_empty_columns

    @allow_empty_columns.setter
    def allow_empty_columns(self, allow):

        if allow is True:
            self._allow_empty_columns = True
        elif allow is False:
            if None in self._header:
                errmsg = "Your header already contains empty columns!" +\
                         " Please change that before using this option!"
                raise Exception(errmsg)
            else:
                self._allow_empty_columns = False
        else:
            raise Exception('invalid argument!!')

        #TODO: better exception

    def load_from_file(self, load_from):
        """
        loads the odml-data from an odml-file

        :param load_from: the path to the odml-file
        :type load_from: string

        """
        doc = odml.tools.xmlparser.load(load_from)
        self._odmldict = self.__create_odmldict(doc)

    def load_from_odmldoc(self, doc):
        """
        loads the odml-data from an odml-document

        :param load_from: the odml-document
        :type load_from: odml-document
        """
        self._odmldict = self.__create_odmldict(doc)

    def load_from_function(self, odmlfct):
        """
        loads the odml-data by using a function that creates an odml-document

        :param load_from: function that returns an odml-document
        :type load_from: function
        """
        doc = odmlfct()
        self._odmldict = self.__create_odmldict(doc)

    def load_from_xls_table(self, load_from):
        """
        loads the odml-data from a xls-file. To load the odml, at least Value,
        Path, PropertyName and odmlDatatype must be given in the table. Also,
        the header_titles must be correct

        :param load_from: name(path) of the xls-file
        :type load_from: string
        """
        # create a inverted header_titles dictionary for an inverted lookup
        inv_header_titles = {v: k for k, v in self._header_titles.items()}

        self._odmldict = []
        workbook = xlrd.open_workbook(load_from)

        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)

            # read the header
            self._header = [inv_header_titles[worksheet.cell(0, col_n).value]
                            for col_n in range(worksheet.ncols)]
            old_dic = {"Path": "",
                       "SectionName": "",
                       "SectionType": "",
                       "SectionDefinition": "",
                       "PropertyName": "",
                       "PropertyDefinition": "",
                       "Value": "",
                       "ValueDefinition": "",
                       "DataUnit": "",
                       "DataUncertainty": "",
                       "odmlDatatype": ""}

            for row_n in range(1, worksheet.nrows):
                current_dic = {"Path": "",
                               "SectionName": "",
                               "SectionType": "",
                               "SectionDefinition": "",
                               "PropertyName": "",
                               "PropertyDefinition": "",
                               "Value": "",
                               "ValueDefinition": "",
                               "DataUnit": "",
                               "DataUncertainty": "",
                               "odmlDatatype": ""}

                for col_n in range(worksheet.ncols):
                    cell = worksheet.cell(row_n, col_n)
                    value = cell.value

                    current_dic[self._header[col_n]] = value

                if (current_dic['Path'] == '' or
                   current_dic['Path'] == old_dic['Path']):
                        # it is not the start of a new section

                        if (current_dic['PropertyName'] == '' or
                            current_dic['PropertyName'] ==
                                old_dic['PropertyName']):
                            # old section, old property
                            for key in self._SECTION_INF:
                                current_dic[key] = old_dic[key]
                            for key in self._PROPERTY_INF:
                                current_dic[key] = old_dic[key]
                        else:
                            # old section, new property
                            for key in self._SECTION_INF:
                                current_dic[key] = old_dic[key]
                else:
                        # new section, => new property
                        pass

                old_dic = current_dic.copy()

                # convert to python datatypes
                dtype = current_dic['odmlDatatype']
                value = current_dic['Value']

                if dtype == 'int':
                    current_dic['Value'] = int(value)
                elif dtype == 'float':
                    current_dic['Value'] = float(value)
                elif dtype == 'boolean':
                    if value in [1, 0]:
                        value = int(value)
                    current_dic['Value'] = str(value)
                elif dtype == 'datetime':
                    value = xlrd.xldate_as_tuple(value, 0)
                    current_dic['Value'] = datetime.datetime(value)
                elif dtype == 'time':
                    value = xlrd.xldate_as_tuple(value, 0)
                    current_dic['Value'] = datetime.time(value[3:])
                elif dtype == 'date':
                    value = xlrd.xldate_as_tuple(value, 0)
                    current_dic['Value'] = datetime.date(value[:3])
                elif dtype in ['string', 'text', 'person']:
                    current_dic['Value'] = str(current_dic['Value'])
                else:
                    raise Exception('unknown datatype!!')
                    # TODO: change exception?!

                self._odmldict.append(current_dic)

    #TODO: use normal reader instead of dictreader => much easier!!
    def load_from_csv_table(self, load_from):
        """
        loads the odmldict from a csv-file containing an odml-table. To load
        the odml, at least Value, Path, PropertyName and odmlDatatype must be
        given in the table. Also, the header_titles must be correct

        :param load_from: name(path) of the csv-file
        :type load_from: string
        """

        self._odmldict = []
        # create a inverted header_titles dictionary for an inverted lookup
        inv_header_titles = {v: k for k, v in self._header_titles.items()}

        with open(load_from, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)

            self._header = [inv_header_titles[h] for h in csvreader.next()]

            must_haves = ["Path", "PropertyName", "Value", "odmlDatatype"]

            # check, if all of the needed information are in the table
            if any([(m not in self._header) for m in must_haves]):
                err_msg = ("your table has to contain all of the following " +
                           " attributes: {0}").format(must_haves)
                raise Exception(err_msg)
                # TODO: exception??
            old_dic = {"Path": "",
                       "SectionName": "",
                       "SectionType": "",
                       "SectionDefinition": "",
                       "PropertyName": "",
                       "PropertyDefinition": "",
                       "Value": "",
                       "ValueDefinition": "",
                       "DataUnit": "",
                       "DataUncertainty": "",
                       "odmlDatatype": ""}

            for row in csvreader:

                current_dic = {"Path": "",
                               "SectionName": "",
                               "SectionType": "",
                               "SectionDefinition": "",
                               "PropertyName": "",
                               "PropertyDefinition": "",
                               "Value": "",
                               "ValueDefinition": "",
                               "DataUnit": "",
                               "DataUncertainty": "",
                               "odmlDatatype": ""}

                for col_n in range(len(row)):
                    current_dic[self._header[col_n]] = row[col_n]

                if (current_dic['Path'] == '' or
                        current_dic['Path'] == old_dic['Path']):
                    # it is not the start of a new section

                    if (current_dic['PropertyName'] == ''
                        or current_dic['PropertyName'] ==
                            old_dic['PropertyName']):
                        # old section, old property
                        for key in self._SECTION_INF:
                            current_dic[key] = old_dic[key]
                        for key in self._PROPERTY_INF:
                            current_dic[key] = old_dic[key]
                    else:
                        # old section, new property
                        for key in self._SECTION_INF:
                                current_dic[key] = old_dic[key]
                else:
                    # new section, => new property
                    pass

                old_dic = current_dic.copy()

                # convert to python datatypes
                dtype = current_dic['odmlDatatype']
                value = current_dic['Value']

                if dtype == 'int':
                    current_dic['Value'] = int(value)
                elif dtype == 'float':
                    current_dic['Value'] = float(value)
                elif dtype == 'boolean':
                    current_dic['Value'] = str(value)
                elif dtype == 'datetime':
                    current_dic['Value'] = \
                        datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                elif dtype == 'time':
                    current_dic['Value'] = \
                        datetime.datetime.strptime(value, '%H:%M:%S').time()
                elif dtype == 'date':
                    current_dic['Value'] = \
                        datetime.datetime.strptime(value, '%Y-%m-%d').date()
                elif dtype in ['string', 'text', 'person']:
                    current_dic['Value'] = str(current_dic['Value'])
                else:
                    raise Exception('unknown datatype!!')
                    # TODO: change exception?!

                self._odmldict.append(current_dic)

    def change_header_titles(self, **kwargs):
        """
        Function to change the Name of a column in your table. Be careful with
        this function if you want to convert the table back to an odml.


        :param Path: Name of the 'Path'-Column in the table
        :param SectionName: Name of the 'Section Name'-Column in the table
        :param SectionType: Name of the 'Section Type'-Column in the table
        :param SectionDefinition: Name of the 'Section Definition'-Column in
            the table
        :param ProgertyName: Name of the 'Property Name'-Column in the table
        :param PropertyDefinition: Name of the 'Property Definition'-Column in
            the table
        :param Value: Name of the 'Value'-Column in the table
        :param ValueDefinition: Name of the 'Value Definition'-Column in the
            table
        :param DataUnit: Name of the 'Data Unit'-Column in the table
        :param DataUncertainty: Name of the 'Data Uncertainty'-Column in the
            table
        :param odmlDatatype: Name of the 'odML Data Type'-Column in the table
        :type Path: string, optional
        :type SectionName: string, optional
        :type SectionType: string, optional
        :type SectionDefinition: string, optional
        :type ProgertyName: string, optional
        :type PropertyDefinition: string, optional
        :type Value: string, optional
        :type ValueDefinition: string, optional
        :type DataUnit: string, optional
        :type DataUncertainty: string, optional
        :type odmlDatatype: string, optional

        """

        for k in kwargs:
            if k in self._header_titles:
                self._header_titles[k] = kwargs[k]
            else:
                errmsg = "{0} is not in the header_title-dictionary".format(k)
                raise Exception(errmsg)
                # TODO: better exception

    def change_header(self, **kwargs):
        """
        Function to change the header of the table.

        The keywordarguments of the function are the possible columns you can
        include into your table; they are listed below, you can also check the
        possible options bei looking at the keys of the header_titles
        dictionary. They take the number of their position in the table,
        starting from left with 1.
        The default-header is ['Path', 'Property Name', 'Value', 'odML Data
        Type']. These are the columns you need to be able to convert your table
        back to an odml-file. Important: You can create tables wich dont
        contain any of those four, but they cant be converted back to odml.

        :param Path: Position of the 'Path'-Column in the table.
        :param SectionName: Position of the 'Section Name'-Column in the table
        :param SectionType: Position of the 'Section Type'-Column in the table
        :param SectionDefinition: Position of the 'Section Definition'-Column
            in the table
        :param PropertyName: Position of the 'Property Name'-Column in the
            table
        :param PropertyDefinition: Position of the 'Property Definition'-Column
            in the table
        :param Value: Position of the 'Value'-Column in the table
        :param ValueDefinition: Position of the 'Value Definition'-Column in
            the table
        :param DataUnit: Position of the 'Data Unit'-Column in the table
        :param DataUncertainty: Position of the 'Data Uncertainty'-Column in
            the table
        :param odmlDatatype: Position of the 'odML Data Type'-Column in the
            table
        :type Path: int, optional
        :type SectionName: int, optional
        :type SectionType: int, optional
        :type SectionDefinition: int, optional
        :type PropertyName: int, optional
        :type PropertyDefinition: int, optional
        :type Value: int, optional
        :type ValueDefinition: int, optional
        :type DataUnit: int, optional
        :type DataUncertainty: int, optional
        :type odmlDatatype: int, optional

        :Example:

            mytable.change_header(Path=1, Value=3, odmlDataType=2)
                => outcoming header: ['Path', 'odML Data Type', 'Value']

        """

        # sortieren nach values
        keys_sorted = sorted(kwargs, key=kwargs.get)

        #check if first element is in range
        if kwargs[keys_sorted[0]] <= 0:
            errmsg = ("Your smallest argument is {}, but the columns start" +
                      " at 1").format(kwargs[keys_sorted[0]])
            raise Exception(errmsg)
            # TODO: better Exception

        max_col = kwargs[keys_sorted[-1]]

        # check if there are empty columns
        if self._allow_empty_columns is False:
            for i in range(1, max_col+1):
                if kwargs[keys_sorted[i-1]] != i:
                    errmsg = ("column {0} is empty. if you want to have " +
                              "empty columns in your table, you have to set" +
                              " allow_empty_columns = True").format(i)
                    raise Exception(errmsg)
                    # TODO: better exception

        #initialize header with enough elements
        header = max_col * [None]

        if keys_sorted[0] in self._header_titles:
                header[kwargs[keys_sorted[0]]-1] = keys_sorted[0]
        else:
            raise Exception(keys_sorted[0], "not in header_titles")
            # TODO: better Exception

        #check if there are two keys with the same value
        for index, key in enumerate(keys_sorted[1:]):
            if kwargs[keys_sorted[index]] == kwargs[keys_sorted[index-1]]:
                errmsg = "The keys {0} and {1} both have the value {2}"\
                    .format(keys_sorted[index-1],
                            keys_sorted[index],
                            kwargs[keys_sorted[index]])
                raise Exception(errmsg)
                # TODO: better exception
            else:
                if key in self._header_titles:
                    header[kwargs[key]-1] = key
                else:
                    raise Exception(key, "not in header_titles")
                    # TODO: better Exception

        self._header = header

    def write2file(self, save_to):
        """
        write the table to the specific file
        """
        raise NotImplementedError()

    def write2odml(self, save_to):
        """
        writes the loaded odmldict (e.g. from an csv-file) to an odml-file
        """

        doc = odml.Document()
        oldpath = []
        oldpropname = ''
        oldpropdef = ''
        valuelist = []
        parent = ''

        for dic in self._odmldict:

            # get the actual Value
            value = odml.Value(data=dic['Value'], dtype=dic['odmlDatatype'])
            if 'ValueDefinition' in self._header:
                value.definition = dic['ValueDefinition']
            if 'DataUnit' in self._header:
                value.unit = dic['DataUnit']
            if 'DataUncertainty' in self._header:
                value.uncertainty = dic['DataUncertainty']

            if dic['Path'] == oldpath:
                # parent is still the same
                if dic['PropertyName'] == oldpropname:
                    # still the same property
                    valuelist.append(value)
                else:
                    prop = odml.Property(name=oldpropname, value=valuelist)
                    if 'PropertyDefinition' in self._header:
                        prop.definition = oldpropdef
                    parent.append(prop)
                    valuelist = [value]
            else:

                if parent != '':
                    prop = odml.Property(name=oldpropname, value=valuelist)
                    if 'PropertyDefinition' in self._header:
                        prop.definition = oldpropdef
                    parent.append(prop)
                    valuelist = [value]
                else:
                    valuelist.append(value)

                parent = doc
                for section in dic['Path'].split('/')[1:]:
                    try:
                        parent = parent[section]
                    except KeyError:
                        parent.append(odml.Section(name=section))
                        parent = parent[section]

                if 'SectionType' in self._header:
                    parent.type = dic['SectionType']
                if 'SectionDefinition' in self._header:
                    parent.definition = dic['SectionDefinition']

            oldpath = dic['Path']
            oldpropname = dic['PropertyName']
            if 'PropertyDefinition' in self._header:
                oldpropdef = dic['PropertyDefinition']

        prop = odml.Property(name=oldpropname, value=valuelist)
        if 'PropertyDefinition' in self._header:
            prop.definition = oldpropdef
        parent.append(prop)

        odml.tools.xmlparser.XMLWriter(doc).write_file(save_to)
