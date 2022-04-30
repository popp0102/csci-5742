# CSCI 5742 Final Project
Jason Poppler and Benjamin Straub  
The purpose of this project is to create a best effort CWE[3] finder à la FlawFinder; it uses pylint[1] and the underlying
library astroid[4] to parse the python code and interact with the abstract syntax tree. The plugins are not 100% accurate,
but are looking for instances that could be vulnerable or cause issue. Since the majority of CVEs for python are around
inputs, these mainly involve user input, file input and interaction with the operating system. Some code was based off
the checkers implemented by Kiwi[2], thanks to them for their wonderful video[5].

## Table of Contents
- [How to Build Distribution](#How-to-Build-Distribution)
- [How To Install](#How-To-Install)
- [How To Run](#How-To-Run)
- [Available Plugins](#Available-Plugins)
- [References](#References)

## How to Build Distribution
```bash
python3 setup.py sdist bdist_wheel
```
The above should create a dist directory which contains the `-py3-none-any.whl` and `.tar.gz` distributions of the
codebase.

## How To Install
```bash
# Install the required libraries 
pip install -r requirements.txt
pip install CSCI_5742_Final_Project-1.0-py3-none-any.whl
```

## How To Run
When installed using pip, all plugin modules fall under the cve_plugins package
```bash
pylint --load-plugins=cve_plugins.ban_arbitrary_execution_subprocess ${Library_Under_Test}
```

Adding the cve_plugins directory to the PYTHONPATH environment variable should allow for use of the plugins
directly.
```bash
pylint --load-plugins=ban_arbitrary_execution_subprocess ${Library_Under_Test}
```

## Available Plugins
* **ban_arbitrary_execution_subprocess** - Attempts to find usages of run and Popen methods on the subprocess module which 
allows arbitrary code execution and opens the door to CWE-78.
* **ban_create_os_subprocess** - Attempts to find usages of a variety of functions that the os module provides to create
subprocesses; since the subprocess module exists, these should be avoided. They also fall under CWE-78.
* **ban_empty_try_catch_blocks** - Attempts to find any use of try except that only contains the pass keyword. Falls under
CWE-755.
* **file_reading_sanitization_check** - Attempts to find uses of the builtin function open() that opens a file descriptor
and warns against its usage. Falls under the CWE-552.
* **input_sanitization_check** - Attempts to find uses of the builtin function input() that takes external input from the
input stream (keyboard, etc) and warns against its usage. Falls under CWE-20.

## References
[1] [Pylint - How to Write a Pylint Plugin](https://pylint.pycqa.org/en/latest/how_tos/plugins.html) last visited 04/22/2022  
[2] [Kiwi CMS linters](https://github.com/kiwitcms/Kiwi/tree/master/kiwi_lint) last visited 04/22/2022  
[3] [Mitre CWE](https://cwe.mitre.org) last visited 04/30/2022    
[4] [Astroid](https://pylint.pycqa.org/projects/astroid/en/latest/) last visited 04/30/2022    
[5] [How to Build a Pylint Plugin](https://www.youtube.com/watch?v=mT0SeMD9rpY) last visited 04/22/2022  
