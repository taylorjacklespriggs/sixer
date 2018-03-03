import ast

from lint_node_rule import LintNodeRule

class RaiseRule(LintNodeRule):
    def _get_problem_message(self, node):
        return "raise with extra arguments not allowed, use six.reraise instead"

    def _is_problem_node(self, node):
        return (
            isinstance(node, ast.Raise) and
            hasattr(node, 'inst') and
            hasattr(node, 'tback') and
            (node.inst or node.tback)
        )
