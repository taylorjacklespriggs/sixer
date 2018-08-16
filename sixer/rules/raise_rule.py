import ast
import six

from sixer.rules.lint_node_rule import LintNodeRule

class ReraiseRule(LintNodeRule):
    is_valid = six.PY2

    def _get_problem_message(self, node):
        return "`raise` with extra arguments not allowed, use six.reraise instead"

    def _is_problem_node(self, node):
        return (
            isinstance(node, ast.Raise) and
            (node.inst or node.tback)
        )

class RaiseFromRule(LintNodeRule):
    is_valid = six.PY3

    def _get_problem_message(self, node):
        return "`raise from` is not allowed, use six.raise_from instead"

    def _is_problem_node(self, node):
        return isinstance(node, ast.Raise) and node.cause
