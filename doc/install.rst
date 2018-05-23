.. _install:

****************************
Prerequisites / Installation
****************************

odMLtables is a pure Python_ package so that it should be easy to install on any system.


Dependencies
------------

The following packages are required to use odMLtables:

.. include:: ../requirements.txt

Download
--------

The latest version of odMLtables is available on GitHub_. You can either use git and download odMLtables
directly under Linux using::

    cd /home/usr/toolbox/
    git clone https://github.com/INM-6/python-odmltables.git

or alternatively download odMLtables as ZIP file and unzip it to a folder.


Installation
------------

Linux
*****

On Linux, to set up odMLtables you navigate to your odMLtables folder and install
odMLtables core via::

    cd /home/usr/toolbox/python-odmltables/
    python setup.py install

For installing also the grapical user interface run::

    cd /home/usr/toolbox/python-odmltables/
    pip install .[gui]

Please note that when using Python 2, the PyQt5 module needs to be manually installed beforehand,
eg using conda::

    conda install pyqt5

Now you can start the odMLtables graphical wizard by calling::

    odmltables

Alternatively, you may navigate to the odMLtables folder and run::

    ./odmltables-gui


Windows/Mac OS X
****************

On non-Linux operating systems we recommend using the Anaconda_ Python distribution, and installing all dependencies in a `Conda environment`_, e.g.::

    conda create -n metadataenv python numpy scipy pip six

    source activate metadataenv

Then navigate to the folder where you downloaded odMLtables and run::

    python setup.py install

or::

    pip install .

For installing also the odMLtables gui, please run::

    pip install .[gui]

Then navigate to the folder where you downloaded odMLtables and run::

    python setup.py install

On Windows, to run the graphical wizard, execute the `odmltables.exe` in the
`Anaconda/Envs/metadataenv/Scripts` in your `User` directory.

Alternatively, on Windows or Max OS X you may navigate to the odMLtables folder and run::

    python odmltables-gui.py


Bugs
----
If you observe a bug in odMLtables please add a bug report at `GitHub issue tracker`_


.. _`Python`: http://python.org/
.. _`GitHub`: https://github.com/INM-6/python-odmltables
.. _`Anaconda`: http://continuum.io/downloads
.. _`Conda environment`: http://conda.pydata.org/docs/faq.html#creating-new-environments
.. _`GitHub issue tracker`: https://github.com/INM-6/python-odmltables/issues
