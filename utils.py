from __future__ import print_function

import ast
import sys

from sixer.rules import prepare_all_rules

def check_file(source_name, out_file=sys.stderr):
    with open(source_name, 'r') as source_file:
        raw_source = source_file.read()
    all_lint_node_rules = list(prepare_all_rules(raw_source))
    tree = ast.parse(raw_source, source_name)
    for node in ast.walk(tree):
        for rule in all_lint_node_rules:
            rule.check_node(node)
    all_node_problems = [problem for rule in all_lint_node_rules for problem in rule.get_problems()]
    all_node_problems.sort(key=lambda p: (p[1].lineno, p[1].col_offset))
    for message, node in all_node_problems:
        print("{}:{}:{}: {}".format(source_name, node.lineno, node.col_offset, message))
    return bool(all_node_problems)