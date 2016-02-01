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
        tables with an emptycolumn
    :type show_all_sections: bool
    :type show_all_properties: bool

    """

    def __init__(self):

        self._odmldict = None
        self._docdict = None
        self.odtypes = OdmlDtypes()
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

    def _create_documentdict(self,doc):
        attributes = ['author','date','repository','version']
        docdict = {att:getattr(doc,att) for att in attributes}
        return docdict


        #TODO: better exception

    def load_from_file(self, load_from):
        """
        loads the odml-data from an odml-file

        :param load_from: the path to the odml-file
        :type load_from: string

        """
        doc = odml.tools.xmlparser.load(load_from)
        self._odmldict = self.__create_odmldict(doc)
        self._docdict =  self._create_documentdict(doc)

    def load_from_odmldoc(self, doc):
        """
        loads the odml-data from an odml-document

        :param load_from: the odml-document
        :type load_from: odml-document
        """
        self._odmldict = self.__create_odmldict(doc)
        self._docdict =  self._create_documentdict(doc)

    def load_from_function(self, odmlfct):
        """
        loads the odml-data by using a function that creates an odml-document

        :param load_from: function that returns an odml-document
        :type load_from: function
        """
        doc = odmlfct()
        self._odmldict = self.__create_odmldict(doc)
        self._docdict =  self._create_documentdict(doc)

    def _get_docdict(self,row):
        '''
        supplementory function to reconstruct self._docdict from first row in table

        :param row: list of values in first row of table
        :return: None
        '''
        if self._docdict == None:
            self._docdict = {}
        for col_id in range(len(row)/2):
            if row[2*col_id+1] != '':
                key = row[2*col_id+1]
                # in case last entry was empty and document
                # info is longer than header, this cell will
                # not be present
                if 2*col_id+2 == len(row):
                    value = ''
                else:
                    value = row[2*col_id+2]
                self._docdict[key] = value

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

            row = 0

            # read document information if present
            if worksheet.cell(0,0).value ==  'Document Information':
                doc_row = [r.value for r in worksheet.row(row)]
                self._get_docdict(doc_row)
                row += 1

            # get number of non-empty odml colums
            header_row = worksheet.row(row)

            # read the header
            header = [h.value for h in header_row]
            # strip trailing empty cells from header
            for i in range(len(header_row)-1,-1,-1):
                if header_row[i].ctype == 0:
                    header.pop(i)
                else:
                    break

            n_cols =  len(header)
            self._header = [inv_header_titles[h] if h!='' else None for h in header]
            row += 1

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

            for row_n in range(row, worksheet.nrows):
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

                for col_n in range(n_cols):
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

                if ('date' in dtype or 'time' in dtype) and (value!=''):
                    value = xlrd.xldate_as_tuple(value, workbook.datemode)
                current_dic['Value'] = self.odtypes.to_odml_value(value,dtype)

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

            row = csvreader .next()

            # check if first line contains document information
            if row[0] == 'Document Information':
                self._get_docdict(row)
                try:
                    row = csvreader.next()
                except StopIteration():
                    raise IOError('Csv file does not contain header row.'
                                  ' Filename "%s"'%load_from)

            # get column ids of non-empty header cells
            header_title_ids = {inv_header_titles[h]:id for id,h in enumerate(row) if h!=''}
            header_title_order = {id:inv_header_titles[h] for id,h in enumerate(row) if h!=''}

            # reconstruct headers
            self._header = [inv_header_titles[h] if h!='' else None for h in row]

            must_haves = ["Path", "PropertyName", "Value", "odmlDatatype"]

            # check, if all of the needed information are in the table
            if any([(m not in self._header) for m in must_haves]):
                err_msg = ("your table has to contain all of the following " +
                           " attributes: {0}").format(must_haves)
                raise Exception(err_msg)

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
                    # using only columns with header
                    if col_n in header_title_order:
                        current_dic[header_title_order[col_n]] = row[col_n]

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

                current_dic['Value'] = self.odtypes.to_odml_value(value,dtype)

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
        :type ValueDefinition: int,
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

    def consistency_check(self):
        """
        check odmldict for consistency regarding dtypes to ensure that data can be loaded again.
        """
        for property_dict in self._odmldict:
            if property_dict['odmlDatatype'] not in self.odtypes.valid_dtypes:
                raise TypeError('Non valid dtype "{0}" in odmldict. Valid types are {1}'.format(property_dict['odmlDatatype'],self.odtypes.valid_dtypes))

    def _filter(self, filter_func):
        """
        remove odmldict entries which do not match filter_func.
        """
        new_odmldict = [d for d in self._odmldict if filter_func(d)]
        deleted_properties = [d for d in self._odmldict if not filter_func(d)]

        self._odmldict = new_odmldict
        return new_odmldict, deleted_properties

    def filter(self,mode='and',invert=False,recursive=False,comparison_func=lambda x,y: x==y,**kwargs):
        """
        filters odml properties according to provided kwargs.

        :param mode: Possible values: 'and', 'or'. For 'and' all keyword arguments
                must be satisfied for a property to be selected. For 'or' only one
                of the keyword arguments must be satisfied for the property to be
                selected. Default: 'and'
        :param invert: Inverts filter function. Previously accepted properties
                are rejected and the other way round. Default: False
        :param recursive: Delete also properties attached to subsections of the
                mother section and therefore complete branch
        :param comparison_func: Function used to compare dictionary entry to
               keyword. Eg. 'lambda x,y: x.startswith(y)' in case of strings or
               'lambda x,y: x in y' in case of multiple permitted values.
               Default: lambda x,y: x==y
        :param kwargs: keywords and values used for filtering
        :return: None
        """
        if not kwargs:
            raise ValueError('No filter keywords provided for property filtering.')
        if mode not in ['and','or']:
            raise ValueError('Invalid operation mode "%s". Accepted values are "and","or".'%(mode))

        def filter_func(dict_prop):
            keep_property = False
            for filter_key, filter_value in kwargs.iteritems():
                if filter_key not in dict_prop:
                    raise ValueError('Key "%s" is missing in property dictionary %s'%(filter_key,dict_prop))

                if comparison_func(dict_prop[filter_key],filter_value):
                    keep_property = True
                else:
                    keep_property = False

                if mode=='or' and keep_property:
                    break
                if mode=='and' and not keep_property:
                    break

            if invert:
                keep_property = not keep_property

            return keep_property


        _, del_props = self._filter(filter_func=filter_func)

        if recursive and len(del_props)>0:
            for del_prop in del_props:
                self.filter(invert=True,recursive=True,comparison_func= lambda x,y: x.startswith(y),Path=del_prop['Path'])

    def merge(self,odmltable):
        """
        Merge odmltable into current odmltable.
        :param odmltable: OdmlTable object or Odml document object
        :return:
        """
        if hasattr(odmltable,'_convert2odml'):
            doc2 = odmltable._convert2odml()
        else:
            # assuming odmltable is already an odml document
            doc2 = odmltable
        doc1 = self._convert2odml()

        for sec in doc2:
            if sec.name in doc1.sections:
                doc1.sections[sec.name].merge(sec)
            else:
                doc1.append(sec)


        #TODO: What should happen to the document properties?
        """
        'author'
        'date'
        'version'
        'repository'
        """

        #TODO: Check what happens to original odmldict...
        self.load_from_odmldoc(doc1)


    def write2file(self, save_to):
        """
        write the table to the specific file
        """
        raise NotImplementedError()

        self.consistency_check()


    def _convert2odml(self):
        """
        Generates odml representation of odmldict and return it as odml document.
        :return:
        """
        doc = odml.Document()
        oldpath = []
        oldpropname = ''
        oldpropdef = ''
        valuelist = []
        parent = ''

        self.consistency_check()

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

        return doc


    def write2odml(self, save_to):
        """
        writes the loaded odmldict (e.g. from an csv-file) to an odml-file
        """
        doc = self._convert2odml()
        odml.tools.xmlparser.XMLWriter(doc).write_file(save_to)


class OdmlDtypes(object):
    """
    Class to handle odml data types, synonyms and default values.

    :param basedtypes_dict: Dictionary containing additional basedtypes to use as keys and default values as values.
            Default: None
    :param synonyms_dict: Dictionary containing additional synonyms to use as keys and basedtypes to associate as values.
            Default: None
    :return: None
    """


    default_basedtypes = {'int':-1,
                  'float':-1.0,
                  'bool':False,
                  'datetime':datetime.datetime(1900,11,11,00,00,00),
                  'datetime.date':datetime.datetime(1900,11,11).date(),
                  'datetime.time':datetime.datetime(1900,11,11,00,00,00).time(),
                  'str':'-',
                  'url':'file://-'}
    default_synonyms = {'boolean':'bool','binary':'bool','date':'datetime.date','time':'datetime.time',
                'integer':'int','string':'str','text':'str','person':'str'}


    def __init__(self,basedtypes_dict=None,synonyms_dict=None):
        self._basedtypes = self.default_basedtypes.copy()
        self._synonyms = self.default_synonyms.copy()
        self._validDtypes = None

        # update default values with used defined defaults
        if basedtypes_dict is not None:
            self._basedtypes.update(basedtypes_dict)
        if synonyms_dict is not None:
            self._synonyms.update(synonyms_dict)


    @property
    def valid_dtypes(self):
        # if not done yet: generate validDtype list with unique entries
        if self._validDtypes == None:
            validDtypes = self._basedtypes.keys()
            for syn in self._synonyms.keys():
                if syn not in validDtypes:
                    validDtypes.append(syn)
            self._validDtypes = validDtypes

        return self._validDtypes


    @property
    def synonyms(self):
        return self._synonyms

    def add_synonym(self,basedtype, synonym):
        """
        Setting user specific default synonyms
        :param basedtype: Accepted basedtype of OdmlDtypes or None. None delete already existing synonym
        :param synonym: Synonym to be connected to basedtype
        :return: None
        """
        if basedtype not in self._basedtypes:
            if basedtype is None and synonym in self._synonyms:
                self._synonyms.pop(synonym)
            else:
                raise ValueError('Can not add synonym "%s=%s". %s is not a base dtype.'
                                 'Valid basedtypes are %s.'%(basedtype,synonym,basedtype,self.basedtypes))

        elif synonym is None or synonym == '':
            raise ValueError('"%s" is not a valid synonym.'%synonym)
        else:
            self._synonyms.update({synonym:basedtype})

    @property
    def basedtypes(self):
        return self._basedtypes.keys()

    def add_basedtypes(self,basedtype,default_value):
        if basedtype in self._basedtypes:
            raise ValueError('Basedtype "%s" already exists. Can not be added. '
                             'To customize the default value use "customize_default".')
        else:
            self._basedtypes.update({basedtype:default_value})

    @property
    def default_values(self):
        def_values = self._basedtypes.copy()
        for syn,base in self._synonyms.iteritems():
            def_values[syn] = self._basedtypes[base]
        return def_values

    def default_value(self,basedtype):
        if basedtype in self.default_values:
            return self.default_values[basedtype]
        else:
            raise ValueError('"%s" is not a basedtype. Valid basedtypes are %s'%(basedtype,self.basedtypes))


    def set_default_value(self,basedtype,default_value):
        if basedtype in self.basedtypes:
            self._basedtypes[basedtype] = default_value
        else:
            raise ValueError('Can not set default value for basedtype "%s". '
                             'This is not a basedtype. Valid basedtypes are %s'%(basedtype,self.basedtypes))

    def to_odml_value(self,value,dtype):
        # return default value of dtype if value is empty
        if value == '':
            return self.default_value(dtype)

        if dtype in self._synonyms:
            dtype = self._synonyms[dtype]

        if dtype == 'datetime':
            result = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif dtype ==  'datetime.date':
            try:
                result = datetime.datetime.strptime(value, '%Y-%m-%d').date()
            except TypeError:
                result = datetime.datetime(*value).date()
        elif dtype == 'datetime.time':
            try:
                result = datetime.datetime.strptime(value, '%H:%M:%S').time()
            except TypeError:
                result = datetime.datetime(*value).time()
        elif dtype == 'url':
            result = str(value)

        elif dtype in self._basedtypes:
            try:
                result = eval('%s("%s")'%(dtype,value))
            except ValueError:
                result = eval('%s(%s)'%(dtype,value))
        else:
            raise TypeError('Unkown dtype {0}'.format(dtype))

        return result
