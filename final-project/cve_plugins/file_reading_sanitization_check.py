import pdb
import re
import astroid
from typing import TYPE_CHECKING
from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter

if TYPE_CHECKING:
    from pylint.lint import PyLinter

"""
    Register the plugin with PyLint
"""
def register(linter: "PyLinter") -> None:
    linter.register_checker(FileReadingSanitizationChecker(linter))


class FileReadingSanitizationChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'file-reading-sanitization-check'
    priority = -1
    msgs = {
        'W0003': (
            "Detected file read with no input sanitization. Be sure to sanitize any data read from a file. (CWE-552)",
            'file-reading-sanitize-check',
            'Reading from a file can be insecure. Be sure to sanitize any data read in.',
        ),
    }
    options = ()
    OPEN_REGEX = '^open(\w*)' # regex to check for open statements

    def __init__(self, linter: PyLinter = None) -> None:
        super(FileReadingSanitizationChecker, self).__init__(linter)

    """
        This method takes in a node value and checks if it is an open statment. It uses the regex defined above.
    """
    def is_open_statement(self, value):
        if re.search(self.OPEN_REGEX, value.as_string()):
            return True
        return False

    """
        This method gets called every time there is a function definition when AST "visits" these nodes.
        There are 3 cases this supports - Assign, Expressions and a For loops. If the left hand side of an
        open statement isn't being used then we can assume there is no file input sanitization, so throw
        a warning. Same with the For loop. We will inspect the statement body and if there is an expression
        with no left hand side being set, we will assume there is no input sanitization.
    """
    def visit_functiondef(self, node) -> None:
        open_files = {}
        for statement in node.body:
            node_type = statement.__class__.__name__
            if node_type in ['Assign']:
                if self.is_open_statement(statement.value):
                    for target in statement.targets:
                        target_name = target.as_string()
                        open_files[target_name] = statement
            elif node_type in ['Expr']:
                for open_file, open_file_node in open_files.items():
                    if re.search(open_file, statement.as_string()):
                        self.add_message('file-reading-sanitize-check', node=statement)
            elif node_type in ['For'] and statement.iter.as_string() in open_files:
                current_line = statement.target.as_string()
                for for_body_statement in statement.body:
                    sub_nodetype = for_body_statement.__class__.__name__
                    if sub_nodetype in ['Expr'] and for_body_statement.value.__class__.__name__ in ['Call']:
                        method_call_node = for_body_statement.value
                        for arg in method_call_node.args:
                            if current_line == arg.as_string():
                                self.add_message('file-reading-sanitize-check', node=method_call_node)

