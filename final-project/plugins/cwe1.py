import astroid
from typing            import TYPE_CHECKING
from astroid           import nodes
from pylint.checkers   import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint       import PyLinter

if TYPE_CHECKING:
    from pylint.lint import PyLinter

def register(linter: "PyLinter") -> None:
    linter.register_checker(PassOnlyChecker(linter))

class PassOnlyChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'pass-only'
    priority = -1
    msgs = {
        'W0001': (
            'Keyword "pass" used in isolation. The error should be explicitly handled. Consider at least logging it.',
            'pass-only-used',
            'Exception blocks should be handled, sole use of pass not recommended.',
        ),
    }
    options = ()

    def __init__(self, linter: PyLinter =None) -> None:
        super(PassOnlyChecker, self).__init__(linter)

    def visit_tryexcept(self, node: nodes.TryExcept) -> None:
        for except_handler in node.handlers:
            if len(except_handler.body) != 1:
                continue

            statement = except_handler.body[0]
            if isinstance(statement, astroid.nodes.node_classes.Pass):
                self.add_message('pass-only-used', node=except_handler)

