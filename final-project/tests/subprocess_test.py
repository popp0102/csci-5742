from subprocess import run as s
from subprocess import Popen as p
from array import typecodes, array
import string as x
import math


def run_test(value):
    s(value)
    print("Done")


def function_ptr_run_test(inputs):
    map(s, inputs)


def Popen_test(value):
    p(input)


run_test('echo "hello"')
Popen_test('ls -lah')
