"""
Doc String
"""
from os import system as s
from os import fork as f


def from_os_system_test():
    """
    This test uses OS.System and should be flagged!
    :return: NULL
    """
    s('echo "Hello World"')


def from_os_system_test_with_input(arbitrary_input):
    """
    This test uses OS.System and should be flagged!
    :return: NULL
    """
    s(arbitrary_input)


def from_os_run_fork():
    """
    This test uses OS.Fork and should be flagged!
    """
    f()


from_os_system_test()
from_os_system_test_with_input('echo "Hello World"')