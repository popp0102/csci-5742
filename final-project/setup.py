#!/usr/bin/env python

from distutils.core import setup

setup(name='CSCI_5742_Final_Project',
      version='1.0',
      description='Python Distribution Utilities',
      author='Jason Poppler, Benjamin Straub',
      author_email='jason.poppler@ucdenver.edu, benjamin.straub@ucdenver.edu',
      url='https://github.com/popp0102/csci-5742',
      packages=['cve_plugins'],
      package_dir={'cve_plugins': 'cve_plugins'},
     )