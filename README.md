
python-odmltables
=================
An interface to convert odML structues to and from table-like representations, such as spreadsheets.

odMLtables provides a set of functions to simplify the setup, maintainance and usage of a metadata management structure using odML. 
In addition to the Python API, python-odmltables provides its main functionality also via a graphical user interface.


Download
--------

The latest version of python-odmltables is available on [GitHub] (https://github.com/INM-6/python-odmltables). You can either use git and download python-odmltables directly using

	$ cd /home/usr/toolbox/
	$ git clone https://github.com/INM-6/python-odmltables.git

or use the download python-odmltables as ZIP file.


Requirements
------------
To use python-odmltables you also need to install

- [python-odML] (https://github.com/G-Node/python-odml)
- [xlrd] (https://pypi.python.org/pypi/xlrd) and [xlwt] (https://pypi.python.org/pypi/xlwt) for reading and writing of the xls format using python


Installation
------------

To set up python-odmltables you navigate to your python-odmltables folder and install it via

	$ cd /home/usr/toolbox/python-odmltables/
	$ python setup.py install

Alternatively, if you don't want to install python-odmltables, you can add the path to your python-odmltables folder to your PYTHONPATH. On Linux this can be (temporarily) done via

    $ PYTHONPATH="${PYTHONPATH}:/home/usr/toolbox/python-odmltables"
    $ export PYTHONPATH

Then you can start the odmltables wizard by navigating to the wizard folder

    $ cd /home/usr/toolbox/python-odmltables/

Bugs
----
If you observe a bug in odMLtables please add a bug report at [the github bug tracker] (https://github.com/INM-6/python-odmltables/issues)
