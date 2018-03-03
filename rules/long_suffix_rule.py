import ast
import re

from sixer.rules.lint_node_rule import LintNodeRule

class LongSuffixRule(LintNodeRule):
    def __init__(self, lines):
        super(LongSuffixRule, self).__init__()
        self.lines = lines
        self.regexp = re.compile('^[0-9]+[Ll]')

    def _is_problem_node(self, node):
        if isinstance(node, ast.Num) and repr(node.n)[-1] == 'L':
            line = self.lines[node.lineno - 1][node.col_offset:]
            return bool(self.regexp.search(line))
        return False

    def _get_problem_message(self, node):
        return "`L` suffix not allowed for ints"
