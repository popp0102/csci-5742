import astroid
from typing            import TYPE_CHECKING
from astroid           import nodes
from pylint.checkers   import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint       import PyLinter

if TYPE_CHECKING:
    from pylint.lint import PyLinter

def register(linter: "PyLinter") -> None:
    linter.register_checker(InputSanitizationChecker(linter))

class InputSanitizationChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'input-sanitization-check'
    priority = -1
    msgs = {
        'W0002': (
            "The input() method was used, but there doesn't seem to be any input sanitization. It is highly recommended some be added.",
            'input-sanitize-check',
            'When gathering input() from the user, it is always safest to sanitize that input.',
        ),
    }
    options = ()

    def __init__(self, linter: PyLinter =None) -> None:
        super(InputSanitizationChecker, self).__init__(linter)

    def visit_functiondef(self, node) -> None:
        print("111111111111111")

