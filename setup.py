# -*- coding: utf-8 -*-

import sys

from odmltables import VERSION
from setuptools import setup

long_description = open("README.rst").read()
install_requires = ['xlrd >= 0.9.4',
                    'xlwt >= 1.0.0',
                    'numpy >= 1.8.2',
                    'quantities >= 0.10.1',
                    'odml <= 1.3.3',
                    'future >= 0.16.0']

# Add python 2 only install requirements
if sys.version_info.major < 3:
    install_requires.append('enum >= 0.4.6')

extras_require = {'docs': ['numpydoc>=0.5',
                           'sphinx>=1.2.2'],
                  'tests': ['nose>=1.3.3'],
                  'gui': ['pyqt4>=4.0.0'],
                  # 'basics':['gcc >= 4.8.5',
                  #           'libxml2 >= 2.9.2'],
                  }

dependency_links = [
    'https://github.com/G-Node/python-odml/tarball/master#egg=odml-1.1.1']

setup(
    name="python-odmltables",
    version=VERSION,
    packages=['odmltables', 'odmltables.gui', 'odmltables.tests'],
    package_data={'odmltables': ['gui/graphics/*']},
    install_requires=install_requires,
    extras_require=extras_require,
    # dependency_links=dependency_links,

    author="odMLtables authors and contributors",
    author_email="j.sprenger@fz-juelich.de",
    description="Interface to convert odML structures to and from table-like representations",
    long_description=long_description,
    license="BSD",
    url='https://github.com/INM-6/python-odmltables',
    download_url='https://github.com/INM-6/python-odmltables/archive/0.1.1.tar.gz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering'],

    entry_points={
        'gui_scripts': ['odmltables = odmltables.gui.main:parse_args []']},
    zip_safe=False,
    keywords = ['odml', 'excel', 'metadata management']
    #     data_files = [('/usr/share/applications', ['odmltables.desktop']),
    #                   ('/usr/share/pixmaps', ['logo/odMLtables.png'])]
)
