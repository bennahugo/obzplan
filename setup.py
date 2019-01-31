import os
import sys
import logging

from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
log = logging.getLogger()


requirements = ['matplotlib', 
                'astropy', 
                'numpy', 
                'scipy']

setup(name='obzplan',
      version='1.0.0',
      description='Observation planning tool taking into account satelites and solar RFI',
      url='https://github.com/bennahugo/obzplan',
      classifiers=[
        "Development Status :: 1 - Stable",
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
      scripts=["obzplan/obzplan.py"],
)


