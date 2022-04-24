import os

def read_test_file(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fullpath = f'{dir_path}/{filename}'
    file     = open(fullpath)
    for line in file:
        print(line, end='')

read_test_file('test_file.txt')

