from sixer.rules.dictionary_methods_rule import DictionaryMethodsRule
from sixer.rules.forbidden_attribute_rule import ForbiddenAttributeRule, ForbiddenItertoolsRule
from sixer.rules.forbidden_builtins_rule import ForbiddenBuiltinRule, ForbiddenBuiltinsRule
from sixer.rules.future_import_rule import FutureImportRule, FuturePrintFunctionRule, FutureDivisionRule, FutureImportsRule
from sixer.rules.lint_node_rule import BaseLintNodeRule, CompoundLintNodeRule, LintNodeRule
from sixer.rules.long_suffix_rule import LongSuffixRule
from sixer.rules.prohibited_import_rule import ProhibitedImportRule, ProhibitedImportsRule
from sixer.rules.raise_rule import RaiseRule
from sixer.rules.safe_iterator_rule import ReturnIteratorRule, ReturnIteratorsRule, AddOperandIteratorRule, AddIteratorRule, AddIteratorsRule
from sixer.rules.tuple_unpacking_rule import TupleUnpackingRule

def prepare_all_rules(source):
    for BasicRule in [
        AddIteratorsRule,
        DictionaryMethodsRule,
        ForbiddenItertoolsRule,
        ForbiddenBuiltinsRule,
        FutureImportsRule,
        ProhibitedImportsRule,
        RaiseRule,
        ReturnIteratorsRule,
        TupleUnpackingRule,
    ]:
        yield BasicRule()
    yield LongSuffixRule(source.split('\n'))
