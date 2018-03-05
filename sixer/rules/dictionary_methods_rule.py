import ast

from sixer.rules.lint_node_rule import LintNodeRule

class DictionaryMethodsRule(LintNodeRule):
    def __init__(self):
        super(DictionaryMethodsRule, self).__init__()
        self.six_name = None

    def _is_problem_node(self, node):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == 'six':
                    self.six_name = name.asname or 'six'
        elif isinstance(node, ast.Attribute):
            return node.attr in ('iteritems', 'iterkeys', 'itervalues')
        return False

    def get_problems(self):
        for node in self.problem_nodes:
            if not (isinstance(node.value, ast.Name) and node.value.id == self.six_name):
                yield (
                    "`dict.{attr}` not compatible with python3, use `{six}.{attr}(dict)` instead"
                        .format(attr=node.attr, six=self.six_name)
                ), node
