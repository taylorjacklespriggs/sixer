import ast

from lint_node_rule import LintNodeRule, CompoundLintNodeRule

class DictionaryMethodsRule(LintNodeRule):
    def __init__(self):
        super(DictionaryMethodsRule, self).__init__(self)
        self.six_name = None

    def _is_problem_node(self, node):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == 'six':
                    self.six_name = name.asname or 'six'
        elif isinstance(node, ast.Attribute):
            return node.attr in ('iteritems', 'iterkeys', 'itervalues'):
        return False

    def get_problems(self):
        for node in self.problem_nodes:
            if not (isinstance(node.value, ast.Name) and node.value.id == self.six_name):
                yield (
                    "`dict.{attr}` not compatible with python3, use `{six}.{attr}(dict)` instead"
                        .format(attr=node.attr, six=self.six_name)
                ), node

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

class TupleUnpackingRule(LintNodeRule):
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
                yield self._get_problem_message(parameter), parameter

class LongSuffixRule(LintNodeRule):
    def __init__(self, source):
        super(LongSuffixRule, self).__init__()
        self.lines = source.split('\n')
        self.regexp = re.compile('^[0-9]+[Ll]')

    def _is_problem_node(self, node):
        if isinstance(node, ast.Num) and repr(node.n)[-1] == 'L':
            line = self.lines[node.lineno - 1][node.col_offset:]
            return bool(self.regexp.search(line))
        return False

    def _get_problem_message(self, node):
        return "`L` suffix not allowed for ints"
