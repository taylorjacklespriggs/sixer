import ast

from sixer.rules.lint_node_rule import LintNodeRule, CompoundLintNodeRule

class ForbiddenAttributeRule(LintNodeRule):
    def __init__(self, module, attribute, alternative):
        super(ForbiddenAttributeRule, self).__init__()
        self.module_name = module
        self.attribute = attribute
        self.problem_message = "`{}.{}` is not allowed, use `{}` instead".format(
            self.module_name,
            attribute,
            alternative,
        )

    def _is_problem_node(self, node):
        return (
            isinstance(node, ast.Attribute) and
            isinstance(node.value, ast.Name) and
            node.value.id == self.module_name and
            node.attr == self.attribute
        )

    def _get_problem_message(self, node):
        return self.problem_message

class ForbiddenItertoolsRule(CompoundLintNodeRule):
    def __init__(self):
        super(ForbiddenItertoolsRule, self).__init__([
            ForbiddenAttributeRule('itertools', attr, alt)
            for attr, alt in [
                ('imap', 'six.moves.imap'),
                ('izip', 'six.moves.izip'),
                ('izip_longest', 'six.moves.zip_longest'),
            ]
        ])
