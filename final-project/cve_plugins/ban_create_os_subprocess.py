"""
    Python 3 has implemented the multiprocessing and subprocess interfaces for creation of subprocesses
    those should be used rather than the python2 os interfaces. This class attempts to find and alert on
    any usage of the old os functions that create subprocesses
"""
from pylint.interfaces import IAstroidChecker, ITokenChecker
from pylint.checkers import BaseTokenChecker


def register(linter):
    """
    Register the plugin with the linter
    """
    linter.register_checker(BanCreateSubprocessViaOS(linter))


class BanCreateSubprocessViaOS(BaseTokenChecker):
    """
    This plugin attempts to discourage the use of the old os api for sub process creation since it can execute
    arbitrary code. It is preferred to use the multiprocessing and subprocessing apis in python 3. Additionally, the use
    of external binaries should be avoided, with a preference to implementation in native python or Cpython.
    """
    __implements__ = (IAstroidChecker, ITokenChecker)


    debug = False
    SUBPROCESS_CREATION_IS_BANNED = 'subprocess-creation-is-banned'
    name = 'find-banned-subprocess-creation'
    priority = -1
    msgs = {
        'W0005': ('"%s" should not be used, try multiprocessing.'
                  'Remember to sanitize your paths when execing paths (CWE-78)',
                  SUBPROCESS_CREATION_IS_BANNED,
                  'Avoid using os level calls for subprocess creation. Opens up your program to CWE-78')
    }
    options = ()
    # List of function calls from os that spawn new subprocesses
    banned_function_calls = [
        'add_dll_directory',
        'execl',
        'execle',
        'execlp',
        'execlpe',
        'execv',
        'execve',
        'execvp',
        'execvpe',
        'fork',
        'forkpty',
        'pidfd_open',
        'popen',
        'posix_spawn',
        'posix_spawnp',
        'register_at_fork',
        'spawnl',
        'spawnle',
        'spawnlp',
        'spawnlpe',
        'spawnv',
        'spawnve',
        'spawnvp',
        'spawnvpe',
        'startfile',
        'system'
    ]

    def process_tokens(self, tokens):
        """
        Processes the raw token strings, looks for tokens that match the banned names above. There could be
        classifications if a user names a variable the same as one of the defined banned calls. In these cases the
        user should not have used the name.
        """
        for (tok_type, token, line_character_start_tuple, line_character_end_tuple, line_being_parsed) in tokens:
            line_number = line_character_start_tuple[0]
            start_col = line_character_start_tuple[1]
            end_lineno = line_character_end_tuple[0]
            end_col = line_character_end_tuple[1]
            if self.debug:
                print(f"Token Type: {tok_type}")
                print(f"Token: {token}")
                print(f"Line: {line_character_start_tuple[0]}")
                print(f"Token Position (start, end): {line_character_start_tuple[1]}, {line_character_end_tuple[1]}")
                print(f"String being parsed: {line_being_parsed}")
            if token in self.banned_function_calls:
                self.add_message('subprocess-creation-is-banned', line=line_number, end_lineno=end_lineno,
                                 col_offset=start_col, end_col_offset=end_col, args=token)
