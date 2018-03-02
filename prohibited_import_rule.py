from lint_node_rule import LintNodeRule

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
            return self.__check_bad_import(node.module)
        return False

    def _get_problem_message(self, node):
        return self.problem_message

prohibited_StringIO_import_rule = ProhibitedImportRule('StringIO', 'six.StringIO')
prohibited_urllib_import_rule = ProhibitedImportRule('urllib', 'six.moves.urllib')
prohibited_urllib2_import_rule = ProhibitedImportRule('urllib2', 'six.moves.urllib')
prohibited_urlparse_import_rule = ProhibitedImportRule('urlparse', 'six.moves.urllib.parse')
prohibited_ConfigParser_import_rule = ProhibitedImportRule('ConfigParser', 'six.moves.configparser')

all_prohibited_import_rules = [
    prohibited_StringIO_import_rule,
    prohibited_urllib_import_rule,
    prohibited_urllib2_import_rule,
    prohibited_urlparse_import_rule,
    prohibited_ConfigParser_import_rule,
]
