import os
import datetime
import odml.base
import odmltables.odml_xls_table as odml_xls_table
from odmltables.xls_style import XlsStyle

pre_enriched_file = 'example2-1.odml'


# EXAMPLE
def run_example():
    # generating OdmlXlsTable object
    xlstable = odml_xls_table.OdmlXlsTable()

    # loading data from odml
    xlstable.load_from_file(pre_enriched_file)

    xlstable.write2file('automatically_enriched.xls')

    # mimicing manual entry of data in the xls
    manual_enrichment()

    xlstable.load_from_xls_table('manually_enriched.xls')

    xlstable.write2odml('example2-2.odml')



def automatic_enrichment():
    # mimic automatized enrichment prior to manual enrichment
    doc = odml.tools.xmlparser.load('../example1/example1-2.odml')
    animal_props = doc['Animal'].properties

    animal_props['AnimalID'].value.data = '2A'
    animal_props['Species'].value.data = 'Meriones unguiculatus'
    animal_props['Sex'].value.data = 'female'
    animal_props['Birthdate'].value.data = datetime.datetime.today().date() - datetime.timedelta(100)
    animal_props['Litter'].value.data = '1A-01'
    animal_props['Seizures'].value.data = 'not observed'

    odml.tools.xmlparser.XMLWriter(doc).write_file(pre_enriched_file)

    return doc

def manual_enrichment():
    # mimic manual enrichment of xls
    doc = automatic_enrichment()
    surgery_props = doc['Animal']['Surgery'].properties

    surgery_props['Surgeon'].value.data = 'Surgeon1'
    surgery_props['Date'].value.data = datetime.datetime.today().date()
    surgery_props['Weight'].value.data = 100.0
    surgery_props['Quality'].value.data = 'good'
    surgery_props['Anaesthetic'].value.data = 'urethane'
    surgery_props['Painkiller'].value.data = ''
    surgery_props['Link'].value.data = '../../surgery/protocols/protocol1.pdf'

    xlstable = odml_xls_table.OdmlXlsTable()
    xlstable.load_from_odmldoc(doc)

    xlstable.write2file('manually_enriched.xls')


if __name__=='__main__':
    if os.path.isfile(pre_enriched_file):
        print 'Mimicing manual odml enrichment.'
        run_example()
    else:
        print 'Performing automatic pre enrichment of odml template.'
        automatic_enrichment()
