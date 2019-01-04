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
    doc = odml.fileio.load('../example1/example1-2.odml')
    animal_props = doc['Animal'].properties

    animal_props['AnimalID'].values = '2A'
    animal_props['Species'].values = 'Meriones unguiculatus'
    animal_props['Sex'].values = 'female'
    animal_props['Birthdate'].values = datetime.datetime.today().date() - datetime.timedelta(100)
    animal_props['Litter'].values = '1A-01'
    animal_props['Seizures'].values = 'not observed'

    odml.fileio.save(doc, pre_enriched_file)

    return doc

def manual_enrichment():
    # mimic manual enrichment of xls
    doc = automatic_enrichment()
    surgery_props = doc['Animal']['Surgery'].properties

    surgery_props['Surgeon'].values = 'Surgeon1'
    surgery_props['Date'].values = datetime.datetime.today().date()
    surgery_props['Weight'].values = 100.0
    surgery_props['Quality'].values = 'good'
    surgery_props['Anaesthetic'].values = 'urethane'
    surgery_props['Painkiller'].values = ''
    surgery_props['Link'].values = '../../surgery/protocols/protocol1.pdf'

    xlstable = odml_xls_table.OdmlXlsTable()
    xlstable.load_from_odmldoc(doc)

    xlstable.write2file('manually_enriched.xls')


if __name__=='__main__':
    if os.path.isfile(pre_enriched_file):
        print('Mimicing manual odml enrichment.')
        run_example()
    else:
        print('Performing automatic pre enrichment of odml template.')
        automatic_enrichment()
