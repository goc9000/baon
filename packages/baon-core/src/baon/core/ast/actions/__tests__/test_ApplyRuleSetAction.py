# baon/core/ast/actions/__tests__/test_ApplyRuleSetAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.core.ast.actions.ApplyRuleSetAction import ApplyRuleSetAction
from baon.core.ast.actions.DeleteAction import DeleteAction
from baon.core.ast.actions.SaveToAliasAction import SaveToAliasAction
from baon.core.ast.rules.RuleSet import RuleSet
from baon.core.ast.rules.Rule import Rule
from baon.core.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.core.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch


class TestApplyRuleSetAction(ActionTestCase):

    def test_basic(self):
        self._test_simple_text_action(
            'abracadabra',
            ApplyRuleSetAction(
                RuleSet(
                    Rule(
                        SequenceMatch(
                            BetweenMatch(),
                            LiteralMatch('c').add_action(DeleteAction()),
                        )
                    )
                )
            ),
            'abraadabra'
        )

    def test_aliases_are_saved(self):
        self._test_aliases_action(
            {'prev_alias': 'prev_value'},
            ApplyRuleSetAction(
                RuleSet(
                    Rule(
                        InsertLiteralMatch('value').add_action(SaveToAliasAction('alias')).add_action(DeleteAction()),
                    )
                )
            ),
            {'alias': 'value', 'prev_alias': 'prev_value'},
        )
