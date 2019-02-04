
odMLtables
=================
An interface to convert odML structures to and from table-like representations, such as spreadsheets.

odMLtables provides a set of functions to simplify the setup, maintenance and usage of a metadata
management structure using odML_.
In addition to the Python_ API, odMLtables provides its main functionality also
via a graphical user interface.


Code Status
-----------
.. image:: https://travis-ci.org/INM-6/python-odmltables.png?branch=master
   :target: https://travis-ci.org/INM-6/python-odmltables
   :alt: Unit Test Status
.. image:: https://coveralls.io/repos/github/INM-6/python-odmltables/badge.svg?branch=master
   :target: https://coveralls.io/github/INM-6/python-odmltables?branch=master
   :alt: Unit Test Coverage
.. image:: https://readthedocs.org/projects/odmltables/badge/?version=latest
   :target: https://odmltables.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Dependencies
------------

odMLtables is based on odML_. A complete list of dependencies is available in the odMLtables
documentation at `Read the Docs`_.

Release Versions
----------------
Official release versions are available at the `Python Package Index`_ and can be installed using
pip_::

    $ pip install odmltables

The graphical user interface can be installed using::

    $ pip install odmltables[gui]


Latest version
--------------

To install the latest version of odMLtables you first need to download the odMLtables source files and install it in a second step.

Download
--------

The latest version of odMLtables is available on GitHub_. You can either use git and download
odMLtables directly under Linux using::

    $ cd /home/usr/toolbox/
    $ git clone https://github.com/INM-6/python-odmltables.git

or alternatively download odMLtables as ZIP file and unzip it to a folder.


Documentation
-------------

The odMLtables documentation is available on `Read the Docs`_. It is based on Sphinx_ and also
locally be built in multiple formats. E.g., to access  the   documentation in html format
navigate to the documentation folder within odMLtables and  compile  the html documentation::

    $ cd /home/usr/toolbox/python-odmltables/doc
    $ make html

All output format available can be listed using::

    $ make -n

Installation
------------

Installation guidelines are available in the official odMLtables documentation
`Read the Docs`_.


Bugs
----
If you observe a bug in odMLtables please add a bug report at the `GitHub issue tracker`_

.. _`Python`: http://python.org/
.. _`pip`: http://pypi.python.org/pypi/pip
.. _`odML`: http://www.g-node.org/projects/odml
.. _`Sphinx`: http://www.sphinx-doc.org/en/stable/
.. _`Python Package Index`: https://pypi.python.org/pypi/python-odmltables/
.. _`GitHub`: https://github.com/INM-6/python-odmltables
.. _`Read the Docs`: https://odmltables.readthedocs.io/en/latest/
.. _`GitHub issue tracker`: https://github.com/INM-6/python-odmltables/issues



