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
from baon.core.ast.matches.control.SequenceMatch import SequenceMatch
from baon.core.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch


class TestApplyRuleSetAction(ActionTestCase):

    def test_basic(self):
        self._test_simple_text_action(
            u'abracadabra',
            ApplyRuleSetAction(
                RuleSet(
                    Rule(
                        SequenceMatch(
                            BetweenMatch(),
                            LiteralMatch(u'c').add_action(DeleteAction()),
                        )
                    )
                )
            ),
            u'abraadabra'
        )

    def test_aliases_are_saved(self):
        self._test_aliases_action(
            {u'prev_alias': u'prev_value'},
            ApplyRuleSetAction(
                RuleSet(
                    Rule(
                        InsertLiteralMatch(u'value').add_action(SaveToAliasAction(u'alias')).add_action(DeleteAction()),
                    )
                )
            ),
            {u'alias': u'value', u'prev_alias': u'prev_value'},
        )
