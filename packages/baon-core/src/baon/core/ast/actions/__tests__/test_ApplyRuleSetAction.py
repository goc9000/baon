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
from baon.core.ast.matches.__tests__.MatchTestCase import delete_action
from baon.core.ast.matches.composite.MatchWithActions import MatchWithActions
from baon.core.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.core.ast.matches.immaterial.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.core.ast.matches.material.pattern.LiteralMatch import LiteralMatch
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
                            delete_action(LiteralMatch('c')),
                        ),
                    ),
                ),
            ),
            'abraadabra'
        )

    def test_aliases_are_saved(self):
        self._test_aliases_action(
            {'prev_alias': 'prev_value'},
            ApplyRuleSetAction(
                RuleSet(
                    Rule(
                        MatchWithActions(
                            InsertLiteralMatch('value'),
                            SaveToAliasAction('alias'),
                            DeleteAction(),
                        ),
                    ),
                ),
            ),
            {'alias': 'value', 'prev_alias': 'prev_value'},
        )
