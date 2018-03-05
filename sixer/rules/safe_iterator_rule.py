import ast

from sixer.rules.lint_node_rule import CompoundLintNodeRule, LintNodeRule

def _is_iterator(node, iterator_name):
    return (
        isinstance(node, ast.Call) and
        isinstance(node.func, ast.Name) and
        node.func.id == iterator_name
    )

class ReturnIteratorRule(LintNodeRule):
    def __init__(self, iterator_name):
        super(ReturnIteratorRule, self).__init__()
        self.iterator_name = iterator_name
        self.problem_message = "Not allowed to return iterator `{}` from function".format(self.iterator_name)

    def _get_problem_message(self, node):
        return self.problem_message

    def _is_problem_node(self, node):
        return isinstance(node, ast.Return) and _is_iterator(node.value, self.iterator_name)

class ReturnIteratorsRule(CompoundLintNodeRule):
    def __init__(self):
        super(ReturnIteratorsRule, self).__init__([
            ReturnIteratorRule(iterator_name)
            for iterator_name in ('filter', 'map', 'zip')
        ])

class AddOperandIteratorRule(LintNodeRule):
    def __init__(self, iterator_name, operand):
        super(AddOperandIteratorRule, self).__init__()
        self.iterator_name = iterator_name
        self.operand = operand

    def _get_operand(self, add):
        return getattr(add, self.operand)

    def _get_problem_message(self, node):
        return "Not allowed to perform addition with `{}` as {} operand".format(self._get_operand(node), self.operand)

    def _is_problem_node(self, node):
        return (
            isinstance(node, ast.BinOp) and
            isinstance(node.op, ast.Add) and
            _is_iterator(self._get_operand(node), self.iterator_name)
        )

class AddIteratorRule(CompoundLintNodeRule):
    def __init__(self, iterator_name):
        super(AddIteratorRule, self).__init__([
            AddOperandIteratorRule(iterator_name, 'left'),
            AddOperandIteratorRule(iterator_name, 'right'),
        ])

class AddIteratorsRule(CompoundLintNodeRule):
    def __init__(self):
        super(AddIteratorsRule, self).__init__([
            AddIteratorRule(iterator_name)
            for iterator_name in [
                'filter',
                'map',
                'range',
                'zip',
            ]
        ])
