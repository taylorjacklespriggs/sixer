from lint_node_rule import LintNodeRule

def _is_iterator(self, node, iterator_names):
    return (
        isinstance(node, ast.Call) and
        isinstance(node.func, ast.Name) and
        node.func.id in iterator_names
    )

class ReturnIteratorRule(LintNodeRule):
    def __init__(self, iterator_name):
        super(ReturnIteratorRule, self).__init__()
        self.iterator_name = iterator_name
        self.problem_message = problem_message

    def _get_problem_message(self):
        return self.problem_message

    def _is_problem_node(self, node):
        return isinstance(node, ast.Return) and _is_iterator(node.value, [self.iterator_name])

class AddIteratorRule(Rule):
    def __init__(self, disallowed_iterators):
        super(AddIteratorRule, self).__init__()
        self.disallowed_iterators = disallowed_iterators

    def __get_iterator_name(self, node):
        return "`{}`".format(node.func.id) if _is_iterator(node, self.disallowed_iterators) else "unknown"

    def _get_problem_message(self, node):
        left_name = self.__get_iterator_name(node.left)
        right_name = self.__get_iterator_name(node.right)
        return "adding {} to {} is not allowed".format(left_name, right_name)

    def is_problem_node(self, node):
        return (
            isinstance(node, ast.BinOp) and
            isinstance(node.op, ast.Add) and
            (_is_iterator(node.left, self.disallowed_iterators) or self.is_iterator(node.right, self.disallowed_iterators))
        )

return_iterator_rules = {
    iterator_name: ReturnIteratorRule(iterator_name)
    for iterator_name in ('filter', 'map', 'zip')
}

add_iterator_rule = AddIteratorRule(['filter', 'map', 'range', 'zip'])

all_iterator_rules = [rir for rir in return_iterator_rules.values()] + [add_iterator_rule]
