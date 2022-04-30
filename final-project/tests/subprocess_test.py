"""
A Test file for the ban_arbitrary_execution_subprocess plugin
"""
from subprocess import run as s
from subprocess import Popen as p
# Confounding imports
from array import typecodes, array
import string as x
import math


def run_test(value):
    """
    Call subprocess run alias
    """
    s(value)
    print("Done")


def function_ptr_run_test(inputs):
    """
    Call Subprocess run alias on inputs map
    """
    map(s, inputs)


def Popen_test(value):
    """
    Call subprocess Popen alias
    """
    p(value)


run_test('echo "hello"')
Popen_test('ls -lah')
