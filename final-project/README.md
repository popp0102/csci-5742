# CSCI 5742 Final Project
Jason Joppler and Benjamin Straub  
The original scope of your project was to 

## Table of Contents
- [How To Install](#How-To-Install)
- [How To Run](#How-To-Run)
- [References](#References)


## How To Install
```bash
# Install the required libraries 
pip install -r requirements.txt
```

## How To Run
```bash
pylint --load-plugins=ban_arbitrary_execution_subprocess,ban_create_os_subprocess,cwe1 ${Library_Under_Test}
```

## References
[1] [Pylint - How to Write a Pylint Plugin](https://pylint.pycqa.org/en/latest/how_tos/plugins.html) last visited 04/22/2022  
[2] [Kiwi CMS linters](https://github.com/kiwitcms/Kiwi/tree/master/kiwi_lint) last visited 04/22/2022  
