import ast

from sixer.rules.lint_node_rule import CompoundLintNodeRule, LintNodeRule

class ProhibitedImportRule(LintNodeRule):
    def __init__(self, prohibited, alternative):
        super(ProhibitedImportRule, self).__init__()
        self.prohibited = prohibited
        self.problem_message = "importing from `{}`, import from `{}` instead".format(prohibited, alternative)

    def __check_bad_import(self, name):
        return name.split('.')[0] == self.prohibited

    def _is_problem_node(self, node):
        if isinstance(node, ast.Import):
            for name in node.names:
                if self.__check_bad_import(name.name):
                    return True
        elif isinstance(node, ast.ImportFrom):
            return self.__check_bad_import(node.module) if node.module is not None else False
        return False

    def _get_problem_message(self, node):
        return self.problem_message

class ProhibitedImportsRule(CompoundLintNodeRule):
    def __init__(self):
        super(ProhibitedImportsRule, self).__init__([
            ProhibitedImportRule(module, alternative)
            for module, alternative in [
                ('StringIO', 'six.StringIO'),
                ('urllib', 'six.moves.urllib'),
                ('urllib2', 'six.moves.urllib'),
                ('urlparse', 'six.moves.urllib.parse'),
                ('ConfigParser', 'six.moves.configparser'),
            ]
        ])
