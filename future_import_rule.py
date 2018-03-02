import ast

from lint_node_rule import CompountLintNodeRule, LintNodeRule

class FutureImportRule(LintNodeRule):
    def __init__(self, future_import):
        self.future_import = future_import
        self.did_import_future = False

    def _is_conflicting_future_node(self, node):
        raise NotImplementedError()

    def _is_problem_node(self, node):
        if not self.did_import_future:
            if isinstance(node, ast.ImportFrom):
                if node.module == '__future__' and any(n.name == self.future_import for n in node.names):
                    self.did_import_future = True
                    return False
            return self._is_conflicting_future_node(node)
        return False

    def get_problems(self):
        if self.did_import_future:
            return iter([])
        return super(FutureImportRule, self).get_problems()

class FuturePrintFunctionRule(FutureImportRule):
    def __init__(self):
        super(FuturePrintFunctionRule, self).__init__('print_function')

    def _get_problem_message(self, node):
        return "print with no `from __future__ import print_function`"

    def _is_conflicting_future_node(self, node):
        if hasattr(ast, 'Print'):
            return isinstance(node, ast.Print)
        else:
            return isinstance(node, ast.Call) and getattr(node.func, 'id', None) == 'print'

class FutureDivisionRule(FutureImportRule):
    def __init__(self):
        super(FuturePrintFunctionRule, self).__init__('print_function')

    def _get_problem_message(self, node):
        return "division with no `from __future__ import division`"

    def _is_conflicting_future_node(self, node):
        return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)

class FutureImportsRule(CompountLintNodeRule):
    def __init__(self):
        super(FutureImportsRule, self).__init__((
            FuturePrintFunctionRule(),
            FutureDivisionRule(),
        ))
