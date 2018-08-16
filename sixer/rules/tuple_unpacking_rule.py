import ast
import six

from sixer.rules.lint_node_rule import LintNodeRule

class TupleUnpackingRule(LintNodeRule):
    is_valid = six.PY2

    def _get_problem_message(self, node):
        return "tuple parameter unpacking not allowed, see PEP 3113"

    def _is_problem_node(self, node):
        return isinstance(node, ast.arguments) and any(
            isinstance(parameter, ast.Tuple)
            for parameter in node.args
        )

    def get_problems(self):
        for node in self.problem_nodes:
            for parameter in node.args:
                if isinstance(parameter, ast.Tuple):
                    yield self._get_problem_message(parameter), parameter
