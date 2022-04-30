import astroid
from typing            import TYPE_CHECKING
from astroid           import nodes
from pylint.checkers   import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint       import PyLinter

if TYPE_CHECKING:
    from pylint.lint import PyLinter

"""
    Register the plugin with PyLint
"""
def register(linter: "PyLinter") -> None:
    linter.register_checker(PassOnlyChecker(linter))


"""
    This class will check if an except block only contains a pass statement.
    Comments don't count as well. This is considered bad practice because it 
    can swallow any errors.
"""
class PassOnlyChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'pass-only'
    priority = -1
    msgs = {
        'W0001': (
            'Keyword "pass" used in isolation. The error should be explicitly handled. Consider at least logging it.'
            ' (CWE-755)',
            'pass-only-used',
            'Exception blocks should be handled, sole use of pass not recommended.',
        ),
    }
    options = ()

    def __init__(self, linter: PyLinter =None) -> None:
        super(PassOnlyChecker, self).__init__(linter)

    """
        Iterate through each except handler and check the body. If the body has only one line
        then see if it is a pass statement. If so, then throw a PyLint warning.
    """
    def visit_tryexcept(self, node: nodes.TryExcept) -> None:
        for except_handler in node.handlers:
            if len(except_handler.body) != 1: # check if only one line and skip if it isn't
                continue

            statement = except_handler.body[0]
            if isinstance(statement, astroid.nodes.node_classes.Pass): # is that statement a pass line
                self.add_message('pass-only-used', node=except_handler)

