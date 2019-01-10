import datetime

import odml
from odml import DType
import odmltables.odml_xls_table as odml_xls_table


# EXAMPLE
def run_example():
    # generating OdmlXlsTable object
    xlstable = odml_xls_table.OdmlXlsTable()

    # loading data from xls file
    xlstable.load_from_xls_table('example3.xls')

    # filtering only for developmental age and body weight properties
    xlstable.filter(PropertyName=['DevelopmentalAge','Weight'], comparison_func= lambda x,y: (x in y))

    # removing templates
    xlstable.filter(invert=True,Path='template', comparison_func=lambda x,y: x.endswith(y))
    xlstable.write2file('example3_Output.xls')


def setup_example():

    # generate OdmlTable object
    xlstable = odml_xls_table.OdmlXlsTable()

    # customize odmldtypes to use
    xlstable.odtypes.add_synonym('string', 'pers')
    dtypes = xlstable.odtypes

    # generating odml document with template structure
    # this could also be done in excel using odmltables
    odml_doc = get_odml_doc(dtypes)

    # enter animal specifications in template structure
    # this would typically be done manually once per animal
    enrich_animal_specifications(odml_doc)

    # enter developmental data in template structure
    # this would typically be done manually on a daily basis using odmltables
    enrich_developmental_specifications(odml_doc)

    # load odml structure into odmltable object
    xlstable.load_from_odmldoc(odml_doc)

    # adapt header of excel file to be written
    xlstable.change_header(Path=1, PropertyName=2, Value=3, DataUnit=4, odmlDatatype=5,PropertyDefinition=6)

    xlstable.write2file('example3.xls')
    xlstable.write2odml('example3.odml')



def get_odml_doc(dtypes):
    # CREATE A DOCUMENT
    doc = odml.Document(version='0.0.1')
    doc.author = 'Author1'
    doc.date = datetime.date.today()
    doc.version = '0.0.1'
    doc.repository = ''

    # APPEND MAIN SECTIONS
    doc.append(odml.Section(name='Animal', definition = 'Information about the animal used'))

    parent = doc['Animal']
    parent.append(odml.Section('Development', definition = 'Information about the development of the animal'))

    parent = doc['Animal']['Development']
    parent.append(odml.Section('dev_measures_template', type='template', definition = 'Developmental data of a single day'))

    parent = doc['Animal']
    parent.append(odml.Property(name='AnimalID', definition='ID of the animal used for this experiment'))
    parent.append(odml.Property(name='Species', definition='Species of the animal'))
    parent.append(odml.Property(name='Strain', definition='Strain of the animal'))
    parent.append(odml.Property(name='Sex', definition='Sex of the animal'))
    parent.append(odml.Property(name='Birthdate', definition='Birthdate of the animal'))
    parent.append(odml.Property(name='BirthAge', unit='days', definition = 'Time of birth after conception'))
    parent.append(odml.Property(name='MotherID', definition='AnimalID of the mother'))

    parent = doc['Animal']['Development']
    parent.append(odml.Property(name='EyeOpening', definition='Date of first eye opening'))
    parent.append(odml.Property(name='GraspingReflex', definition='Date of first observation of grasping reflex'))

    parent = doc['Animal']['Development']['dev_measures_template']
    parent.append(odml.Property(name='Weight', unit='g', definition='Weight of the animal'))
    parent.append(odml.Property(name='BodyLength', unit='cm', definition='Distance from nose to tail tip [cm]'))
    parent.append(odml.Property(name='TailLength', unit='cm', definition='Length of the tail'))
    parent.append(odml.Property(name='Date', definition='Date of recording of this set of developmental measures'))
    parent.append(odml.Property(name='CliffAvoidance', unit='s', definition='Time after which cliff aversion reflex is observed'))
    parent.append(odml.Property(name='DevelopmentalAge', definition='Developmental age of the animal in days after birth (P_)'))

    return doc


def enrich_animal_specifications(odml_doc):
    animal_properties = odml_doc['Animal'].properties

    animal_properties['AnimalID'].values = '2A'
    animal_properties['Species'].values = 'Mouse'
    animal_properties['Strain'].values = 'C57/Blj6'
    animal_properties['Sex'].values = 'female'
    animal_properties['Birthdate'].values = datetime.date.today() - datetime.timedelta(10)
    animal_properties['BirthAge'].values = 20.0
    animal_properties['MotherID'].values = '1A'

def enrich_developmental_specifications(odml_doc,n_examinations=5):

    # adding properties which only need to be entered once
    developmental_properties = odml_doc['Animal']['Development'].properties

    developmental_properties['EyeOpening'].values = datetime.date.today() - datetime.timedelta(5)
    developmental_properties['GraspingReflex'].values = datetime.date.today() - datetime.timedelta(7)

    # adding properties which are measured regulary
    template_section = odml_doc['Animal']['Development']['dev_measures_template']

    for examination_id in range(n_examinations):

        #generate new copy of template sec and fill values
        dev_sec = template_section.clone()
        dev_sec.name = 'dev_measures_%i'%int(examination_id)
        dev_sec.type = 'enriched'
        dev_properties = dev_sec.properties
        #measuring every second day
        dev_properties['Date'].values = datetime.date.today() - datetime.timedelta(10) + datetime.timedelta(examination_id*2)
        dev_properties['DevelopmentalAge'].values = examination_id*2
        dev_properties['Weight'].values = 2+examination_id
        dev_properties['BodyLength'].values = 3 + examination_id
        dev_properties['TailLength'].values = 1 + examination_id
        dev_properties['CliffAvoidance'].values = 5 - 5*examination_id/n_examinations

        # appending new section to main odml
        template_section.parent.append(dev_sec)


if __name__=='__main__':
    setup_example()
    run_example()