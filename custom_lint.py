from __future__ import print_function
import ast
import re
import sys

def prepare_all_lint_node_rules(source, filename):
  all_rules = [DictionaryMethodsRule(), MetaclassRule()]
  all_rules.extend([
    ForbiddenAttributesRule(
      'itertools',
      {
        'imap': 'six.moves.imap',
        'izip': 'six.moves.izip',
        'izip_longest': 'six.moves.zip_longest',
      },
    ),
    FuturePrintFunctionRule(),
    FutureDivisionRule(),
    SafeIteratorRule({'zip', 'map', 'filter'}),
    TupleUnpackingRule(),
  ])
  if 'onprem/' not in filename:
    all_rules.extend([
      ForbiddenBuiltinsRule({
        'xrange': 'range|six.moves.xrange',
        'raw_input': 'six.input',
        'input': 'six.input',
        'long': 'int|six.moves.integer_types',
        'unicode': 'six.text_type',
        'basestring': 'six.string_types',
        'reduce': 'six.moves.reduce',
      }),
      ProhibitedImportRule({
        'StringIO': 'six.StringIO',
        'urllib': 'six.moves.urllib',
        'urllib2': 'six.moves.urllib',
        'urlparse': 'six.moves.urllib.parse',
        'ConfigParser': 'six.moves.configparser',
      }),
      RaiseRule(),
      LongSuffixRule(source),
    ])
  return all_rules

def check_file(source_name, out_file=sys.stdout):
  with open(source_name, 'r') as source_file:
    raw_source = source_file.read()
  all_lint_node_rules = prepare_all_lint_node_rules(raw_source, source_name)
  tree = ast.parse(raw_source, source_name)
  for node in ast.walk(tree):
    for rule in all_lint_node_rules:
      rule.check_node(node)
  all_node_problems = [problem for rule in all_lint_node_rules for problem in rule.problems()]
  all_node_problems.sort(key=lambda p: (p[1].lineno, p[1].col_offset))
  for message, node in all_node_problems:
    print("{}:{}:{}: {}".format(source_name, node.lineno, node.col_offset, message))
  return bool(all_node_problems)
