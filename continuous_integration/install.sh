#!/bin/bash
# Based on a script from scikit-learn

# This script is meant to be called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.

set -e

# Fix the compilers to workaround avoid having the Python 3.4 build
# lookup for g++44 unexpectedly.
export CC=gcc
export CXX=g++

if [[ "$DISTRIB" == "conda" ]]; then
    # Deactivate the travis-provided virtual environment and setup a
    # conda-based environment instead
    deactivate

    # Use the miniconda installer for faster download / install of conda
    # itself
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh \
        -O miniconda.sh
    chmod +x miniconda.sh && ./miniconda.sh -b -p $HOME/miniconda
    export PATH=/home/travis/miniconda/bin:$PATH
    conda config --set always_yes yes
    conda update --yes conda

    # Configure the conda environment and put it in the path using the
    # provided versions
    conda create -n testenv --yes python=$PYTHON_VERSION pip nose coverage lxml pyyaml\
        numpy=$NUMPY_VERSION xlwt=$XLWT_VERSION xlrd=$XLRD_VERSION
    source activate testenv
    conda install libgfortran=1

    # remove this once odml1.4 is on pypi
    conda install -c conda-forge rdflib

elif [[ "$DISTRIB" == "conda_min" ]]; then
    # Deactivate the travis-provided virtual environment and setup a
    # conda-based environment instead
    deactivate

    # Use the miniconda installer for faster download / install of conda
    # itself
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh \
        -O miniconda.sh
    chmod +x miniconda.sh && ./miniconda.sh -b -p $HOME/miniconda
    export PATH=/home/travis/miniconda/bin:$PATH
    conda config --set always_yes yes
    conda update --yes conda

    # Configure the conda environment and put it in the path using the
    # provided versions
    conda create -n testenv --yes python=$PYTHON_VERSION pip nose coverage lxml pyyaml \
        numpy=$NUMPY_VERSION xlwt=$XLWT_VERSION xlrd=$XLRD_VERSION
    source activate testenv

    # remove this once odml1.4 is on pypi
    conda install -c conda-forge rdflib

    if [[ "$COVERAGE" == "true" ]]; then
        pip install coveralls
    fi
elif [[ "$DISTRIB" == "ubuntu" ]]; then
    # deactivate
    # Create a new virtualenv using system site packages for numpy
    # virtualenv testenv
    # source testenv/bin/activate
    pip install nose
    pip install coverage
    pip install quantities
    pip install numpy==$NUMPY_VERSION
    pip install xlwt==$XLWT_VERSION
    pip install xlrd==$XLRD_VERSION
    pip install lxml
    pip install pyyaml
    pip install rdflib

    #TODO: remove pip installations which are already covered by setup.py

fi


if [[ "$COVERAGE" == "true" ]]; then
    pip install coveralls
fi

python setup.py install
