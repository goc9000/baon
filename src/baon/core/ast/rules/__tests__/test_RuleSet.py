# baon/core/ast/rules/__tests__/test_RuleSet.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.core.ast.actions.SaveToAliasAction import SaveToAliasAction
from baon.core.ast.matches.control.SequenceMatch import SequenceMatch
from baon.core.ast.matches.insertion.InsertAliasMatch import InsertAliasMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.pattern.FormatMatch import FormatMatch
from baon.core.ast.rules.Rule import Rule
from baon.core.ast.rules.RuleSet import RuleSet


class TestRuleSet(TestCase):

    def test_aliases_and_text_are_passed_from_rule_to_rule(self):
        self._test_rule_set(
            text=u'abc 123',
            rule_set=RuleSet(
                Rule(
                    SequenceMatch(
                        LiteralMatch(u'abc').add_action(ApplyFunctionAction(u'paras')),
                        FormatMatch(u'd').add_action(SaveToAliasAction(u'alias')),
                    ),
                ),
                Rule(
                    InsertAliasMatch(u'alias'),
                ),
            ),
            expected_text=u' 123(abc) 123',
            expected_aliases={u'alias': u' 123'}
        )

    def _test_rule_set(self, text, rule_set, expected_text, aliases=None, expected_aliases=None):
        aliases = aliases or dict()
        expected_aliases = expected_aliases or dict()

        result = rule_set.apply_on(text, aliases)

        self.assertEqual(result.text, expected_text)
        self.assertEqual(result.aliases, expected_aliases)
