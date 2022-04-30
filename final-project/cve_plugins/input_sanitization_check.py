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

"""
    Register the plugin with PyLint
"""
def register(linter: "PyLinter") -> None:
    linter.register_checker(InputSanitizationChecker(linter))

class InputSanitizationChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'input-sanitization-check'
    priority = -1
    msgs = {
        'W0002': (
            "The input() method was used, but there doesn't seem to be any input sanitization."
            "It is highly recommended some be added. (CWE-20)",
            'input-sanitize-check',
            'When gathering input() from the user, it is always safest to sanitize that input.',
        ),
    }
    options = ()
    INPUT_REGEX = "^input(\w*)" # regex to check if an input statement

    def __init__(self, linter: PyLinter =None) -> None:
        super(InputSanitizationChecker, self).__init__(linter)

    """
        Method to check if the node value is an input statement. Uses the regex defined above.
    """
    def is_input_statement(self, value):
        if re.search(self.INPUT_REGEX, value.as_string()):
            return True
        return False

    """
        This method gets called every time there is a function definition when AST "visits" these nodes.
        We iterate over all statements in the function definition looking for input() method calls. If
        one is found then we will keep track if that statment is set to a variable or not. We will take
        into account whether the input is called via return statment and also warn on that.
    """
    def visit_functiondef(self, node) -> None:
        lhs_of_input_dict = {}
        for statement in node.body:
            node_type = statement.__class__.__name__
            if node_type in ['Expr', 'Return']:
                if self.is_input_statement(statement.value):
                    self.add_message('input-sanitize-check', node=statement)
                for lhs_name, original_statement in lhs_of_input_dict.items():
                    if node_type == 'Return' and statement.value.as_string() == lhs_name:
                        self.add_message('input-sanitize-check', node=statement)
            elif node_type in ['Assign']:
                for target in statement.targets:
                    target_name = target.as_string()
                    if self.is_input_statement(statement.value):
                        lhs_of_input_dict[target_name] = statement
                    elif target_name in lhs_of_input_dict:
                        del lhs_of_input_dict[target_name]

