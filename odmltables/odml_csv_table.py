# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:17:02 2015

@author: pick
"""

from odml_table import OdmlTable
import csv


class OdmlCsvTable(OdmlTable):
    """
    Class to create a csv-file from an odml-file
    """

    def __init__(self):
        OdmlTable.__init__(self)

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

        with open(save_to, 'wb') as csvfile:

            fieldnames = [self._header_titles[h] if h is not None else ""
                          for h in self._header]

            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                       dialect='excel',
                                       quoting=csv.QUOTE_NONNUMERIC)
            oldpath = ""
            oldprop = ""

            csvwriter.writeheader()

            self.consistency_check()

            for dic in self._odmldict:
                # create a copy of the dictionary, so nothing in the odml_dict
                # will be changed
                tmp_row = dic.copy()

                # removing section entries (if neccessary)

                if dic["Path"] == oldpath:
                    if not self.show_all_sections:
                        for h in self._SECTION_INF:
                            tmp_row[h] = ""
                else:
                    oldpath = dic["Path"]
                    # if a new section begins all property- and value-
                    # information should be written, even if its the same as
                    # in the line before, so oldvalinf and oldprop are resetted
                    oldprop = ""

                # removing property entries (if neccessary)

                if dic["PropertyName"] == oldprop:
                    if not self.show_all_properties:
                        for h in self._PROPERTY_INF:
                            tmp_row[h] = ""
                else:
                    oldprop = dic["PropertyName"]

                # eliminate those fields that wont show up in the table

                row = {self._header_titles[h]: tmp_row[h]
                       for h in self._header if h is not None}

                # check if row is empty, otherwise write it to the csv-file
                if not (row.values() == ['' for r in row]):
                    csvwriter.writerow(row)
                else:
                    pass
