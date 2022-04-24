#!/usr/bin/env python

from distutils.core import setup

setup(name='CSCI_5742_Final_Project',
      version='1.0',
      description='Python Static Analysis for Common Weaknesses',
      author='Jason Poppler, Benjamin Straub',
      author_email='jason.poppler@ucdenver.edu; benjamin.straub@ucdenver.edu',
      url='https://github.com/popp0102/csci-5742',
      packages=['cve_plugins'],
      package_dir={'cve_plugins': 'cve_plugins'},
      py_modules=[
            'ban_arbitrary_execution_subprocess',
            'ban_create_os_subprocess',
            'cwe1',
            'input_sanitization_check],
      install_requires=[
            'astroid==2.9.3',
            'pylint==2.12.2'
      ]
     )
