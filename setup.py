#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, glob
import warnings
from setuptools import setup, find_packages

with open("README.rst") as f:
    long_description = f.read()
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
with open('requirements_doc.txt') as f:
    doc_requires = f.read().splitlines()
with open('requirements_test.txt') as f:
    test_requires = f.read().splitlines()
with open('requirements_gui.txt') as f:
    gui_requires = f.read().splitlines()

extras_require = {'doc': doc_requires,
                  'test': test_requires,
                  'gui': gui_requires
                  }

# PyQt5 needs to be installed manually with python 2 when installing odmltables gui.
if sys.version_info.major < 3:
    warnings.warn('The odMLtables gui requires PyQt5. Please install this dependency first before '
                  'installing the odmltables gui, eg. using "conda install -c anaconda '
                  '\'pyqt>=5\'"')

VERSION = open('./odmltables/VERSION.txt', 'r').read().strip()

setup(
    name="odmltables",
    version=VERSION,
    packages=find_packages(),
    package_data={'odmltables': ['gui/graphics/*', 'VERSION.txt']},
    install_requires=install_requires,
    extras_require=extras_require,

    author="odMLtables authors and contributors",
    author_email="j.sprenger@fz-juelich.de",
    description="Interface to convert odML structures to and from table-like representations",
    long_description=long_description,
    license="BSD",
    url='https://github.com/INM-6/python-odmltables',
    download_url="https://github.com/INM-6/python-odmltables/archive/{0}.tar.gz".format(VERSION),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'],
    entry_points={
        'gui_scripts': ['odmltables = odmltables.gui.main:parse_args []']},
    zip_safe=False,
    keywords=['odml', 'excel', 'metadata management'],
    # Extension('foo', ['foo.c'], include_dirs=['.']),
    data_files=[('share/pixmaps', glob.glob(os.path.join("logo", "*"))),
                ('.', ['odmltables/VERSION.txt',
                       'requirements.txt',
                       'requirements_doc.txt',
                       'requirements_gui.txt',
                       'requirements_test.txt'])]
)