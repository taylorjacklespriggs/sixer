from __future__ import print_function

class BaseLintNodeRule(object):
    is_valid = True

    def check_node(self, node):
        raise NotImplemented

    def get_problems(self):
        raise NotImplemented

class LintNodeRule(BaseLintNodeRule):
    def __init__(self):
        self.problem_nodes = []

    def _get_problem_message(self, node):
        raise NotImplemented

    def _is_problem_node(self, node):
        raise NotImplemented

    def check_node(self, node):
        if self._is_problem_node(node):
            self.problem_nodes.append(node)

    def get_problems(self):
        for node in self.problem_nodes:
            yield self._get_problem_message(node), node

class CompoundLintNodeRule(BaseLintNodeRule):
    def __init__(self, rules):
        self.rules = [rule for rule in rules if rule.is_valid]
        self.is_valid = bool(self.rules)

    def check_node(self, node):
        for rule in self.rules:
            try:
                rule.check_node(node)
            except:
                print(rule)
                raise

    def get_problems(self):
        for rule in self.rules:
            for problem, node in rule.get_problems():
                yield problem, node
