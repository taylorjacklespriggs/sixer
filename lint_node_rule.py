class BaseLintNodeRule(object):
    def check_node(self, node):
        raise NotImplementedError()

    def get_problems(self):
        raise NotImplementedError()

class LintNodeRule(BaseLintNodeRule):
    def __init__(self):
        self.problem_nodes = []

    def _get_problem_message(self, node):
        raise NotImplementedError()

    def _is_problem_node(self, node):
        raise NotImplementedError()

    def check_node(self, node):
        if self._is_problem_node(node):
            self.problem_nodes.append(node)

    def get_problems(self):
        for node in self.problem_nodes:
            yield self._get_problem_message(node), node

class CompoundLintNodeRule(BaseLintNodeRule):
    def __init__(self, rules):
        self.rules = rules

    def check_node(self, node):
        for rule in self.rules:
            rule.check_node(node)

    def get_problems(self):
        for rule in self.rules:
            for problem, node in rule.get_problems():
                yield problem, node
