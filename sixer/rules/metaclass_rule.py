import ast

from sixer.rules.lint_node_rule import LintNodeRule, CompoundLintNodeRule

class Python2MetaclassRule(LintNodeRule):
    def _get_problem_message(self, node):
        return "using `__metaclass__`, use the `six.add_metaclass` decorator instead"

    def _is_problem_node(self, node):
        return isinstance(node, ast.ClassDef) and any(
            isinstance(child, ast.FunctionDef) and child.name == '__metaclass__' or
            isinstance(child, ast.Assign) and any(
              target.id == '__metaclass__'
              for target in child.targets
            ) for child in node.body
        )

class Python3MetaclassRule(LintNodeRule):
    def _get_problem_message(self, node):
        return "using `metaclass` class keyword, use the `six.add_metaclass` decorator instead"

    def _is_problem_node(self, node):
        return isinstance(node, ast.ClassDef) and any(
            kw.arg == 'metaclass' for kw in getattr(node, 'keywords', [])
        )

class MetaclassRule(CompoundNodeLintRule):
    def __init__(self):
        super(MetaclassRule, self).__init__([Python2MetaclassRule, Python3MetaclassRule])
