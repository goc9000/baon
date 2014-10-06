# baon/logic/ast/__tests__/test_match_interactions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase

from baon.logic.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.logic.ast.matches.composite.RepeatMatch import RepeatMatch
from baon.logic.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.logic.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.logic.ast.matches.special.BetweenMatch import BetweenMatch
from baon.logic.ast.matches.special.EndAnchorMatch import EndAnchorMatch

from baon.logic.ast.actions.ApplyFunctionAction import ApplyFunctionAction


class TestBetweenMatchInteractions(MatchTestCase):
    """
    Integration test for checking the interactions between the BetweenMatch and other matches in various control
    structures.
    """

    def test_only_first_between_match_in_sequence_expands(self):
        self._test_unique_match(
            text=u'Some text',
            match=SequenceMatch(
                BetweenMatch().add_action(ApplyFunctionAction(u'paras')),
                BetweenMatch().add_action(ApplyFunctionAction(u'braces')),
                BetweenMatch().add_action(ApplyFunctionAction(u'curlies')),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': u'(Some text)[]{}', 'position': 9})

    def test_anchored_state_preserved_across_iterations(self):
        self._test_unique_match(
            text=u'Some text',
            match=SequenceMatch(
                RepeatMatch(
                    BetweenMatch().add_action(ApplyFunctionAction(u'paras')),
                    0,
                    None,
                ),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': u'(Some text)()', 'position': 9})

    def test_insert_matches_are_not_anchors(self):
        self._test_unique_match(
            text=u'Some text',
            match=SequenceMatch(
                BetweenMatch().add_action(ApplyFunctionAction(u'paras')),
                InsertLiteralMatch(u'1'),
                BetweenMatch().add_action(ApplyFunctionAction(u'braces')),
                InsertLiteralMatch(u'2'),
                BetweenMatch().add_action(ApplyFunctionAction(u'curlies')),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': u'(Some text)1[]2{}', 'position': 9})

    def test_pattern_matches_are_anchors(self):
        self._test_unique_match(
            text=u'abcdefghi',
            match=SequenceMatch(
                BetweenMatch().add_action(ApplyFunctionAction(u'paras')),
                LiteralMatch(u'd'),
                BetweenMatch().add_action(ApplyFunctionAction(u'braces')),
                LiteralMatch(u'g'),
                BetweenMatch().add_action(ApplyFunctionAction(u'curlies')),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': u'(abc)d[ef]g{hi}', 'position': 9})
