import ast

from sixer.rules.lint_node_rule import LintNodeRule

class FormattedStringLiteralRule(LintNodeRule):
    rule_is_valid = hasattr(ast, 'JoinedStr')

    def _get_problem_message(self, node):
        return "using formatted string literal, use str.format instead"

    def _is_problem_node(self, node):
        return isinstance(node, ast.JoinedStr)
