import ast
import six

from sixer.rules.lint_node_rule import LintNodeRule


class DictionaryUnpackingRule(LintNodeRule):
    is_valid = six.PY3

    def _get_problem_message(self, node):
        return "dict unpacking not allowed, use dict.update instead"

    def _is_problem_node(self, node):
        return isinstance(node, ast.Dict) and None in node.keys


class IterableUnpackingRule(LintNodeRule):
    is_valid = six.PY3

    def _get_problem_message(self, node):
        return "iterable unpacking not allowed"

    def _is_problem_node(self, node):
        return isinstance(node, (ast.List, ast.Tuple)) and any(
            isinstance(elt, ast.Starred) for elt in node.elts
        )


class KwargUnpackingRule(LintNodeRule):
    is_valid = six.PY3

    def _get_problem_message(self, node):
        return "unpacking of multiple keyword arguments is not allowed"

    def _is_problem_node(self, node):
        return isinstance(node, ast.Call) and len([
            kw for kw in node.keywords if kw.arg is None
        ]) > 1


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
