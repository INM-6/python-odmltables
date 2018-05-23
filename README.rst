
python-odmltables
=================
An interface to convert odML structures to and from table-like representations, such as spreadsheets.

odMLtables provides a set of functions to simplify the setup, maintenance and usage of a metadata
 management structure using [odML](_odml).
In addition to the Python API, python-odmltables provides its main functionality also via a graphical user interface.


Code Status
-----------
.. image:: https://travis-ci.org/INM-6/python-odmltables.png?branch=master
   :target: https://travis-ci.org/INM-6/python-odmltables
   :alt: Unit Test Status
.. image:: https://coveralls.io/repos/INM-6/python-odmltables/badge.png
   :target: https://coveralls.io/r/INM-6/python-odmltables
   :alt: Unit Test Coverage


Dependencies
------------

The packages required to use python-odmltables are listed in the [requirements]
(requirements.txt). Additional packages are required when installing the [odmltables gui]
(requirements_gui.txt) or building the [documentation generation](requirements_docs.txt) or
running [odmltables tests](requirements_tests.txt).

Release Versions
----------------
Official release versions are available at the [Python Package Index] (https://pypi.python.org/pypi/python-odmltables/) and can be installed using pip::

    $ pip install python-odmltables


Latest version
--------------
To install the latest version of odmltables you first need to download the odmltables source files and install it in a second step.

Download
--------

The latest version of python-odmltables is available on [GitHub] (https://github.com/INM-6/python-odmltables). You can either use git and download python-odmltables directly under Linux using::

    $ cd /home/usr/toolbox/
    $ git clone https://github.com/INM-6/python-odmltables.git

or alternatively download python-odmltables as ZIP file and unzip it to a folder.


Documentation
-------------

The documentation of odmltables is based on [sphinx] (http://www.sphinx-doc.org/en/stable/) and can be vizualized in multiple formats. E.g., to access the documentation in html format navigate to the documentation folder within odmltables and compile the html documentation::

    $ cd /home/usr/toolbox/python-odmltables/doc
    $ make html

All output format available can be listed using::

    $ make -n


Installation
------------

Linux
*****

On Linux, to set up python-odmltables you navigate to your python-odmltables folder and install it via::

    $ cd /home/usr/toolbox/python-odmltables/
    $ python setup.py install

You can start the odmltables graphical wizard by calling::

    $ odmltables

Alternatively, you may navigate to the python-odmltables folder and run::

    $ ./odmltables-gui


Windows/Mac OS X
****************

On non-Linux operating systems we recommend using the Anaconda_ Python distribution, and installing all dependencies in a `Conda environment`_, e.g.::

    $ conda create -n metadataenv python numpy scipy pip six
    $ source activate metadataenv

Then navigate to the folder where you downloaded python-odmltables and run::

    $ python setup.py install

or::

    $ pip install .

For installing also the odmltables gui, please run::

    $ pip install .[gui]

On Windows, to run the graphical wizard, execute odml-tables.exe in the
Anaconda/Envs/metadataenv/Scripts folder in your User directory.

Alternatively, on Windows or Mac OS X you may navigate to the python-odmltables folder and run::

    $ python odmltables-gui.py



Anaconda environments
*********************

Anaconda environments require the following additional package::

    $ conda install pyqt=4


Bugs
----
If you observe a bug in odMLtables please add a bug report at [the github bug tracker] (https://github.com/INM-6/python-odmltables/issues)

.. _`Python`: http://python.org/
.. _`odml`: http://www.g-node.org/projects/odml
.. _`Anaconda`: http://continuum.io/downloads
.. _`Conda environment`: http://conda.pydata.org/docs/faq.html#creating-new-environments


test


