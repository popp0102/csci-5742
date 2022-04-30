"""
Subprocess still allows the execution of arbitrary commands from the file system. Warn on these calls, as they should
probably be avoided in favor of implementation in python/CPython. At minimum, they need proper sanitization.
"""
from pylint.interfaces import IAstroidChecker, ITokenChecker
from pylint.checkers import BaseTokenChecker
from pylint.checkers.utils import infer_all
from astroid.nodes import Call, FunctionDef
from astroid import Uninferable


def register(linter):
    """
    Register the plugin with the linter
    """
    linter.register_checker(BanArbitraryExecutionFromSubprocess(linter))


class BanArbitraryExecutionFromSubprocess(BaseTokenChecker):
    __implements__ = (IAstroidChecker, ITokenChecker)
    """
    This plugin attempts to find the use of banned subprocess functions through tokens, imports and calls. The banned
    functions are run and Popen. Since run is a common method name, the specific use of subprocess.run is looked for.
    """
    debug = False
    BAN_ARBITRARY_EXECUTION_SUBPROCESS = 'ban-arbitrary-execution-subprocess'
    name = BAN_ARBITRARY_EXECUTION_SUBPROCESS
    priority = -1
    msgs = {
        'W0008': ('"%s" should not be used ',
                  BAN_ARBITRARY_EXECUTION_SUBPROCESS,
                  'Avoid creating subprocesses that execute external scripts. Opens up your program to CWE-78.')
    }
    options = ()

    def process_tokens(self, tokens) -> None:
        """
        Any use of Popen should be banned, if Popen appears in tokens, flag as bad.
        :param tokens: string token from the code under test
        """
        for (tok_type, token_string, line_character_start_tuple, line_character_end_tuple, line_being_parsed) in tokens:
            line_number = line_character_start_tuple[0]
            start_col = line_character_start_tuple[1]
            end_lineno = line_character_end_tuple[0]
            end_col = line_character_end_tuple[1]
            if self.debug == True:
                print(f"Token Type: {type(tok_type)}")
                print(f"Token: {token_string}")
                print(f"Line: {line_character_start_tuple[0]}")
                print(f"Token Position (start, end): {line_character_start_tuple[1]}, {line_character_end_tuple[1]}")
                print(f"String being parsed: {line_being_parsed}")
            if token_string == 'Popen':
                self.add_message(self.BAN_ARBITRARY_EXECUTION_SUBPROCESS, line=line_number, end_lineno=end_lineno,
                                 col_offset=start_col, end_col_offset=end_col, args=token_string)

    def visit_call(self, node: Call) -> None:
        """
            subprocess.run has to be called, so look for call. Only works if process was imported and subsequently
            called.
            Based on code in pylint source.
        """
        for inferred in infer_all(node.func):
            if inferred is Uninferable:
                continue
            elif isinstance(inferred, FunctionDef) and inferred.qname() == "subprocess.run":
                self.add_message(self.BAN_ARBITRARY_EXECUTION_SUBPROCESS, line=1, args="subprocess.run")

    def visit_importfrom(self, node) -> None:
        """
        Visit import x from y nodes; attempt to find any instances of subprocess.run being imported.
        Necessary in order to catch functions being imported with aliases, which avoids run being called.
        :param node: importfrom node
        """
        base_name = node.modname
        if base_name == 'subprocess':
            name_mapping = node.names
            for name_pair in name_mapping:
                original_function_name = name_pair[0]
                if original_function_name == 'run':
                    self.add_message(self.BAN_ARBITRARY_EXECUTION_SUBPROCESS, line=1, args="subprocess.run")
