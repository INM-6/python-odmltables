
import odmltables.odml_xls_table as odml_xls_table
from odmltables.xls_style import XlsStyle

def run_example():

    # Generate OdmlXlsTable object
    xlstable = odml_xls_table.OdmlXlsTable()
    # Load data from xls
    xlstable.load_from_xls_table('example1-2.xls')

    # Save as odml file
    xlstable.write2odml('example1-2.odml')

    pass


def setup_example():
    # We are using the same csv table as used in the tutorial
    filename = '../../doc/source/csv/example1-2.csv'

    xlstable = odml_xls_table.OdmlXlsTable()
    xlstable.load_from_csv_table(filename)


    # turn off color of table cells
    basic_style = XlsStyle(backcolor='white', fontcolor='black', fontstyle='')
    xlstable.highlight_defaults = False
    xlstable.highlight_style = basic_style
    xlstable.header_style = basic_style
    xlstable.first_style = basic_style
    xlstable.second_style = basic_style
    xlstable.first_marked_style = basic_style
    xlstable.second_marked_style = basic_style
    xlstable.document_info_style = basic_style

    # saving as  file to be comparable to tutorial
    xlstable.write2file('example1-2.xls')

if __name__=='__main__':
    setup_example()
    run_example()