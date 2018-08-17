from sixer.rules.dictionary_methods_rule import DictionaryMethodsRule
from sixer.rules.forbidden_attribute_rule import ForbiddenAttributeRule, ForbiddenItertoolsRule
from sixer.rules.forbidden_builtins_rule import ForbiddenBuiltinRule, ForbiddenBuiltinsRule
from sixer.rules.fsl_rule import FormattedStringLiteralRule
from sixer.rules.future_import_rule import FutureImportRule, FuturePrintFunctionRule, FutureDivisionRule, FutureImportsRule
from sixer.rules.keyword_rule import KeywordOnlyRule
from sixer.rules.lint_node_rule import BaseLintNodeRule, CompoundLintNodeRule, LintNodeRule
from sixer.rules.long_suffix_rule import LongSuffixRule
from sixer.rules.metaclass_rule import MetaclassRule
from sixer.rules.prohibited_import_rule import ProhibitedImportRule, ProhibitedImportsRule
from sixer.rules.raise_rule import ReraiseRule, RaiseFromRule
from sixer.rules.safe_iterator_rule import ReturnIteratorRule, ReturnIteratorsRule, AddOperandIteratorRule, AddIteratorRule, AddIteratorsRule
from sixer.rules.unpacking_rule import DictionaryUnpackingRule, IterableUnpackingRule, TupleUnpackingRule

def prepare_all_rules(source):

    def get_rules():
        for BasicRule in [
            AddIteratorsRule,
            DictionaryMethodsRule,
            DictionaryUnpackingRule,
            ForbiddenItertoolsRule,
            ForbiddenBuiltinsRule,
            FormattedStringLiteralRule,
            FutureImportsRule,
            IterableUnpackingRule,
            KeywordOnlyRule,
            MetaclassRule,
            ProhibitedImportsRule,
            RaiseFromRule,
            ReraiseRule,
            ReturnIteratorsRule,
            TupleUnpackingRule,
        ]:
            yield BasicRule()
        yield LongSuffixRule(source.splitlines())

    return [rule for rule in get_rules() if rule.is_valid]
