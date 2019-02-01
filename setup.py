import os
import sys
import logging
import six
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
log = logging.getLogger()

__version__ = "1.0.0.0"

requirements = ['matplotlib <= 2.2.3', 
                'astropy <= 2.0.7', 
                'numpy <= 1.15.1',
                'scipy <= 1.1.0',
                'pyephem <= 3.7.6.0'] if six.PY2 else \
               ['matplotlib >= 2.2.3', 
                'astropy >= 2.0.7', 
                'numpy >= 1.15.1', 
                'scipy >= 1.1.0',
                'pyephem >= 3.7.6.0']

def readme():
    """ Return README.md contents """
    with open('README.md') as f:
        return f.read()

setup(name='obzplan',
      version = __version__,
      description='Observation planning tool taking into account satelites and solar RFI',
      long_description = readme(),
      url='https://github.com/bennahugo/obzplan',
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Astronomy"],
      author='Benjamin Hugo',
      author_email='bhugo@ska.ac.za',
      license='GNU GPL v3',
      install_requires=requirements,
      include_package_data=True,
      packages=["obzplan"],
      scripts=["obzplan/obzplan"],
)


