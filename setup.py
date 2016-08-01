# -*- coding: utf-8 -*-

from setuptools import setup

long_description = open("README.rst").read()
install_requires = ['xlrd >= 0.9.4',
                    'xlwt >= 1.0.0',
                    'lxml >= 3.6.1',
                    'enum >= 0.4.6',
                    'numpy >= 1.8.2',
                    'quantities >= 0.10.1',
                    'odml >= 1.1.1']

extras_require = {'docs': ['numpydoc>=0.5',
                           'sphinx>=1.2.2'],
                  'tests': ['nose>=1.3.3'],
                  'gui': ['pyqt4>=4.0.0'],
                  # 'basics':['gcc >= 4.8.5',
                  #           'libxml2 >= 2.9.2'],
                  }

dependency_links = [
    'http://github.com/G-Node/python-odml/tarball/master#egg=odml-1.1.1']

setup(
    name="python-odmltables",
    version='0.1.1',
    packages=['odmltables', 'odmltables.wizard', 'odmltables.tests'],
    package_data={'odmltables': ['wizard/graphics/*']},
    install_requires=install_requires,
    extras_require=extras_require,
    dependency_links=dependency_links,

    author="odML-tables authors and contributors",
    author_email="j.sprenger@fz-juelich.de",
    description="Interface to convert odML structures to and from table-like representations",
    long_description=long_description,
    license="BSD",
    url='https://github.com/INM-6/python-odmltables',
    download_url='https://github.com/INM-6/python-odmltables/archive/0.1.0'
                 '.tar.gz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering'],

    entry_points={
        'gui_scripts': ['odmltables = odmltables.wizard.main:run []']},
    zip_safe=False,
    keywords = ['odml', 'excel', 'metadata management']
    #     data_files = [('/usr/share/applications', ['odmltables.desktop']),
    #                   ('/usr/share/pixmaps', ['logo/odMLtables.png'])]
)
