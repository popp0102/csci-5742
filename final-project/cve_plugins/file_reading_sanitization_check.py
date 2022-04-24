import pdb
import re
import astroid
from typing            import TYPE_CHECKING
from astroid           import nodes
from pylint.checkers   import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint       import PyLinter

if TYPE_CHECKING:
    from pylint.lint import PyLinter

def register(linter: "PyLinter") -> None:
    linter.register_checker(FileReadingSanitizationChecker(linter))

class FileReadingSanitizationChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'file-reading-sanitization-check'
    priority = -1
    msgs = {
        'W0003': (
            "Detected file, but no input sanitization was found. Be sure to sanitize any data read from a file.",
            'file-reading-sanitize-check',
            'Reading from a file can be insecure. Be sure to sanitize any data read in.',
        ),
    }
    options = ()

    def __init__(self, linter: PyLinter =None) -> None:
        super(FileReadingSanitizationChecker, self).__init__(linter)

    def visit_functiondef(self, node) -> None:
        self.add_message('file-reading-sanitize-check', node=node)

