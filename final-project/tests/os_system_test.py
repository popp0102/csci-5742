"""Module Doc String"""
import os


def os_system_test():
    """
    This test uses OS.System and should be flagged!
    :return: NULL
    """
    os.system('echo "Hello World"')


def os_system_test_with_input(arbitrary_input):
    """
    This test uses OS.System and should be flagged!
    :return: NULL
    """
    exec("print(Hello)")
    os.system(arbitrary_input)


os_system_test()
os_system_test_with_input('echo "Hello World"')
