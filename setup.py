# -*- coding: utf-8 -*-

from setuptools import setup

long_description = open("README.md").read()
install_requires = ['',
                    '']
extras_require = {'docs': ['sphinx>=1.2.2'],
                  'odml': ['python-odml>=0.1.0']}

setup(
    name="python-odmlviz",
    version='0.1.0',
    packages=['', ''],
    install_requires=install_requires,
    extras_require=extras_require,

    author="",
    author_email="",
    description="",
    long_description=long_description,
    license="BSD",
    url='github.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering']
)
