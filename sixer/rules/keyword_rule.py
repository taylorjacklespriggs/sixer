import ast
import six

from sixer.rules.lint_node_rule import LintNodeRule


class KeywordOnlyRule(LintNodeRule):
    is_valid = six.PY3

    def _get_problem_message(self, node):
        return "keywords only arguments not allowed"

    def _is_problem_node(self, node):
        return (
            isinstance(node, (ast.FunctionDef, ast.Lambda))
            and node.args.kwonlyargs
        )
