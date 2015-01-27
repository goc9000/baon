# baon/core/ast/matches/special/__tests__/test_BetweenMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase

from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.core.ast.matches.control.SequenceMatch import SequenceMatch
from baon.core.ast.matches.control.RepeatMatch import RepeatMatch
from baon.core.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.positional.EndAnchorMatch import EndAnchorMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch


class TestBetweenMatch(MatchTestCase):

    def test_basic(self):
        self._test_match(
            text='abc d',
            match=BetweenMatch(),
            expected_solutions=[
                {'matched_text': '', 'position': 0, 'anchored': False},
                {'matched_text': 'a', 'position': 1, 'anchored': False},
                {'matched_text': 'ab', 'position': 2, 'anchored': False},
                {'matched_text': 'abc', 'position': 3, 'anchored': False},
                {'matched_text': 'abc ', 'position': 4, 'anchored': False},
                {'matched_text': 'abc d', 'position': 5, 'anchored': False},
            ])

    def test_between_match_is_empty_if_unanchored(self):
        self._test_unique_match(
            text='abc d',
            match=BetweenMatch(),
            anchored=False,
            expected_solution={'matched_text': '', 'position': 0})

    def test_only_first_between_match_in_sequence_expands(self):
        self._test_unique_match(
            text='Some text',
            match=SequenceMatch(
                BetweenMatch().add_action(ApplyFunctionAction('paras')),
                BetweenMatch().add_action(ApplyFunctionAction('braces')),
                BetweenMatch().add_action(ApplyFunctionAction('curlies')),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(Some text)[]{}', 'position': 9})

    def test_anchored_state_preserved_across_iterations(self):
        self._test_unique_match(
            text='Some text',
            match=SequenceMatch(
                RepeatMatch(
                    BetweenMatch().add_action(ApplyFunctionAction('paras')),
                    0,
                    None,
                ),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(Some text)()', 'position': 9})

    def test_insert_matches_are_not_anchors(self):
        self._test_unique_match(
            text='Some text',
            match=SequenceMatch(
                BetweenMatch().add_action(ApplyFunctionAction('paras')),
                InsertLiteralMatch('1'),
                BetweenMatch().add_action(ApplyFunctionAction('braces')),
                InsertLiteralMatch('2'),
                BetweenMatch().add_action(ApplyFunctionAction('curlies')),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(Some text)1[]2{}', 'position': 9})

    def test_pattern_matches_are_anchors(self):
        self._test_unique_match(
            text='abcdefghi',
            match=SequenceMatch(
                BetweenMatch().add_action(ApplyFunctionAction('paras')),
                LiteralMatch('d'),
                BetweenMatch().add_action(ApplyFunctionAction('braces')),
                LiteralMatch('g'),
                BetweenMatch().add_action(ApplyFunctionAction('curlies')),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(abc)d[ef]g{hi}', 'position': 9})
