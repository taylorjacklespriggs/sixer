import ast

from sixer.rules.lint_node_rule import CompoundLintNodeRule, LintNodeRule

class ForbiddenBuiltinRule(LintNodeRule):
    def __init__(self, forbidden, alternative):
        super(ForbiddenBuiltinRule, self).__init__()
        self.forbidden = forbidden
        self.name_nodes = []
        self.problem_message = "builtin `{}` is not allowed, use `{}` instead".format(forbidden, alternative)

    def _is_problem_node(self, node):
        return isinstance(node, ast.Name) and node.id == self.forbidden

    def _get_problem_message(self, node):
        return self.problem_message

class ForbiddenBuiltinsRule(CompoundLintNodeRule):
    def __init__(self):
        super(ForbiddenBuiltinsRule, self).__init__([
            ForbiddenBuiltinRule(builtin, alt)
            for builtin, alt in [
                ('xrange', 'range|six.moves.xrange'),
                ('raw_input', 'six.input'),
                ('input', 'six.input'),
                ('long', 'int|six.moves.integer_types'),
                ('unicode', 'six.text_type'),
                ('basestring', 'six.string_types'),
                ('reduce', 'six.moves.reduce'),
            ]
        ])
