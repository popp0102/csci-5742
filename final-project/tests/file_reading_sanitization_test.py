import os
import html

def read_test_file_with_no_sanitization(fullpath):
    file = open(fullpath)
    for line in file:
        print(line, end='')

def read_test_file_with_no_sanitization2(fullpath):
    file = open(fullpath)
    print(file.readline(), end='')
    print(file.readline(), end='')
    print(file.readline(), end='')


def read_test_file_with_sanitization2(fullpath):
    file = open(fullpath)
    line = file.readline()
    line = line.escape(user_input)


######################################################################
filename = 'test_file.txt'
dir_path = os.path.dirname(os.path.realpath(__file__))
fullpath = f'{dir_path}/{filename}'

print("--------------")
read_test_file_with_no_sanitization(fullpath)
print("--------------")
read_test_file_with_no_sanitization2(fullpath)
print("--------------")
######################################################################

