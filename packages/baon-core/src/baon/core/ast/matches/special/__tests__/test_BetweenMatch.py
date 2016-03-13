# baon/core/ast/matches/special/__tests__/test_BetweenMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase, mark_parens, mark_braces, mark_curlies
from baon.core.ast.matches.composite.RepeatMatch import RepeatMatch
from baon.core.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.core.ast.matches.immaterial.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.core.ast.matches.material.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.material.positional.EndAnchorMatch import EndAnchorMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch
from baon.core.ast.matches.special.SearchReplaceMatch import SearchReplaceMatch


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

    def test_anchored_by_end_anchor_match(self):
        self._test_unique_match(
            text='Some text',
            match=SequenceMatch(
                mark_parens(BetweenMatch()),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(Some text)', 'position': 9})

    def test_only_first_between_match_in_sequence_expands(self):
        self._test_unique_match(
            text='Some text',
            match=SequenceMatch(
                mark_parens(BetweenMatch()),
                mark_braces(BetweenMatch()),
                mark_curlies(BetweenMatch()),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(Some text)[]{}', 'position': 9})

    def test_repeated_between_match(self):
        self._test_match(
            text='Some text',
            match=SequenceMatch(
                RepeatMatch(mark_parens(BetweenMatch()), 0, None),
                EndAnchorMatch(),
            ),
            expected_solutions=[
                {'matched_text': '(Some text)()', 'position': 9},
                {'matched_text': '(Some text)', 'position': 9},
            ])

    def test_insert_matches_are_not_anchors(self):
        self._test_unique_match(
            text='Some text',
            match=SequenceMatch(
                mark_parens(BetweenMatch()),
                InsertLiteralMatch('1'),
                mark_braces(BetweenMatch()),
                InsertLiteralMatch('2'),
                mark_curlies(BetweenMatch()),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(Some text)1[]2{}', 'position': 9})

    def test_pattern_matches_are_anchors(self):
        self._test_unique_match(
            text='abcdefghi',
            match=SequenceMatch(
                mark_parens(BetweenMatch()),
                LiteralMatch('d'),
                mark_braces(BetweenMatch()),
                LiteralMatch('g'),
                mark_curlies(BetweenMatch()),
                EndAnchorMatch(),
            ),
            expected_solution={'matched_text': '(abc)d[ef]g{hi}', 'position': 9})

    def test_multiple_possible_anchors(self):
        self._test_match(
            text='abracadabra',
            match=SequenceMatch(
                LiteralMatch('a'),
                mark_parens(BetweenMatch()),
                LiteralMatch('a'),
            ),
            expected_solutions=[
                {'matched_text': 'a(br)a', 'position': 4},
                {'matched_text': 'a(brac)a', 'position': 6},
                {'matched_text': 'a(bracad)a', 'position': 8},
                {'matched_text': 'a(bracadabr)a', 'position': 11},
            ])

    def test_anchor_may_not_match(self):
        self._test_match(
            text='aabbaaba',
            match=SequenceMatch(
                mark_parens(BetweenMatch()),
                RepeatMatch(LiteralMatch('b'), 0, None),
            ),
            expected_solutions=[
                {'matched_text': '()', 'position': 0, 'anchored': False},
                {'matched_text': '(a)', 'position': 1, 'anchored': False},
                {'matched_text': '(aa)bb', 'position': 4, 'anchored': True},
                {'matched_text': '(aa)b', 'position': 3, 'anchored': True},
                {'matched_text': '(aa)', 'position': 2, 'anchored': False},
                {'matched_text': '(aab)b', 'position': 4, 'anchored': True},
                {'matched_text': '(aab)', 'position': 3, 'anchored': False},
                {'matched_text': '(aabb)', 'position': 4, 'anchored': False},
                {'matched_text': '(aabba)', 'position': 5, 'anchored': False},
                {'matched_text': '(aabbaa)b', 'position': 7, 'anchored': True},
                {'matched_text': '(aabbaa)', 'position': 6, 'anchored': False},
                {'matched_text': '(aabbaab)', 'position': 7, 'anchored': False},
                {'matched_text': '(aabbaaba)', 'position': 8, 'anchored': False},
            ])

    def test_between_match_before_search_replace(self):
        self._test_match(
            text='abracadabra',
            match=SequenceMatch(
                mark_parens(BetweenMatch()),
                SearchReplaceMatch(mark_braces(LiteralMatch('a'))),
                LiteralMatch('r'),
                BetweenMatch(),
                EndAnchorMatch(),
            ),
            expected_solutions=[
                {'matched_text': '(ab)r[a]c[a]d[a]br[a]', 'position': 19, 'text': 'abr[a]c[a]d[a]br[a]'},
                {'matched_text': '(abracadab)r[a]', 'position': 13, 'text': 'abracadabr[a]'},
            ])
