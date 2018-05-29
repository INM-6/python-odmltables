# -*- coding: utf-8 -*-
"""

"""

__package__='odmltables'

import csv

from .odml_table import OdmlTable


class OdmlCsvTable(OdmlTable):
    """
    Class to create a csv-file from an odml-file
    """

    def __init__(self, load_from=None):
        super(OdmlCsvTable, self).__init__(load_from=load_from)

    def write2file(self, save_to):
        """
        writes the data from the odml-file to a csv-file.
        Each line of the table represents one Value of the odml-file. By
        changing the header of the table you can choose, which informations
        about those values will be shown in the table.
        You can also decide, not to include information about every specific
        value in your header, for example if you just want to get an overview
        of your odml-structur. Then rows, that would be empty will be skipped
        and not printed in the table.

        :param save_to: name of the csv-file
        :type save_to: string

        """

        self.consistency_check()

        with open(save_to, 'w') as csvfile:

            len_docdict = 0 if not self._docdict else len(self._docdict)
            fieldnames = list(range(max(len(self._header), len_docdict * 2 + 1)))

            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                       dialect='excel',
                                       quoting=csv.QUOTE_NONNUMERIC)
            oldpath = ""
            oldprop = ""

            # writing document info
            if self._docdict:
                doc_list = ['Document Information']
                for doc_key in sorted(self._docdict):
                    doc_list = doc_list + [doc_key, self._docdict[doc_key]]
                csvwriter.writerow(dict(zip(range(len(doc_list)), doc_list)))

            # writing document headers
            header_list = [self._header_titles[h] if h is not None else ""
                           for h in self._header]
            csvwriter.writerow(dict(zip(range(len(header_list)), header_list)))

            for dic in self._odmldict:
                # create a copy of the dictionary, so nothing in the odml_dict
                # will be changed
                tmp_row = dic.copy()

                # inflate dictionary to fit to column headers
                tmp_row['Path'], tmp_row['PropertyName'] = tmp_row['Path'].split(':')
                tmp_row['SectionName'] = tmp_row['Path'].split('/')[-1]

                # removing section entries (if necessary)
                if tmp_row["Path"].split(':')[0] == oldpath:
                    if not self.show_all_sections:
                        for h in self._SECTION_INF + ['SectionName', 'Path']:
                            tmp_row[h] = ""
                else:
                    oldpath = tmp_row["Path"].split(':')[0]
                    # if a new section begins all property- and value-
                    # information should be written, even if its the same as
                    # in the line before, so oldvalinf and oldprop are reset
                    oldprop = ""

                # removing property entries (if neccessary)

                if tmp_row['PropertyName'] == oldprop:
                    if not self.show_all_properties:
                        for h in self._PROPERTY_INF + ['PropertyName']:
                            tmp_row[h] = ""
                else:
                    oldprop = tmp_row['PropertyName']

                # eliminate those fields that wont show up in the table

                row = {header_list.index(self._header_titles[h]): tmp_row[h]
                       for h in self._header if h is not None}

                def write_row(row):
                    # check if row is empty, otherwise write it to the csv-file
                    if not (list(row.values()) == ['' for r in row]):
                        csvwriter.writerow(row)
                    else:
                        pass

                # writing also rows when value is not present
                if tmp_row['Value'] == []:
                    tmp_row['Value'] = ['']

                for v in tmp_row['Value']:
                    if 'Value' in header_list:
                        row[header_list.index('Value')] = v
                    write_row(row)
                    # empty entries for further values to be added
                    for h in self._header:
                        if ((not self.show_all_properties
                             and h in self._PROPERTY_INF + ['PropertyName']) or
                                (not self.show_all_sections
                                 and h in self._SECTION_INF + ['SectionName', 'Path'])):
                            row[header_list.index(self._header_titles[h])] = ''
