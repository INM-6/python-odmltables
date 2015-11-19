# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:24:48 2015

@author: pick
"""

import odml
from compare_section_table import CompareSectionTable
import csv


class CompareSectionCsvTable(CompareSectionTable):
    """
    class to write a CompareSectionTable to a csv-file
    """

    def __init__(self):

        CompareSectionTable.__init__(self)

    def write2file(self, save_to):
        """
        saves the table as a csv-file
        """

        properties, sections, table = self._build_table()

        with open(save_to, "wb") as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel',
                                   quoting=csv.QUOTE_NONNUMERIC)


            if self.switch:
                csvwriter.writerow([''] + properties)

                for i, line in enumerate(table):
                    csvwriter.writerow([sections[i]] + line)

            else:
                csvwriter.writerow([''] + sections)

                for i in range(len(table[0])):
                    csvwriter.writerow([properties[i]] + [table[j][i]
                                       for j in range(len(table))])
