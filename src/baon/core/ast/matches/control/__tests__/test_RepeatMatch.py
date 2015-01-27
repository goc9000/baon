# baon/core/ast/matches/control/__tests__/test_RepeatMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.control.RepeatMatch import RepeatMatch
from baon.core.ast.matches.control.AlternativesMatch import AlternativesMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch


class TestRepeatMatch(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text='abcabcabcabca',
            match=RepeatMatch(LiteralMatch('abc'), 0, None),
            expected_solution={'matched_text': 'abcabcabcabc', 'position': 12})

    def test_maximum(self):
        self._test_unique_match(
            text='abcabcabcabca',
            match=RepeatMatch(LiteralMatch('abc'), 0, 2),
            expected_solution={'matched_text': 'abcabc', 'position': 6})

    def test_minimum(self):
        self._test_unique_match(
            text='abcabcabcabca',
            match=RepeatMatch(LiteralMatch('abcd'), 0, None),
            expected_solution={'matched_text': '', 'position': 0})
        self._test_no_match(
            text='abcabcabcabca',
            match=RepeatMatch(LiteralMatch('abcd'), 1, None))
        self._test_no_match(
            text='abcabdabcabca',
            match=RepeatMatch(LiteralMatch('abc'), 2, None))

    def test_alternative(self):
        self._test_match(
            text='abcabcabca',
            match=RepeatMatch(
                AlternativesMatch(
                    LiteralMatch('abc'),
                    LiteralMatch('abcabca'),
                ),
                0, None),
            expected_solutions=[
                {'matched_text': 'abcabcabc', 'position': 9},  # abc+abc+abc
                {'matched_text': 'abcabcabca', 'position': 10},  # abc+abcabca
                {'matched_text': 'abcabca', 'position': 7},  # abcabca
            ])

    def test_alternative_order(self):
        self._test_match(
            text='abcabcabca',
            match=RepeatMatch(
                AlternativesMatch(
                    LiteralMatch('abcabca'),
                    LiteralMatch('abc'),
                ),
                0, None),
            expected_solutions=[
                {'matched_text': 'abcabca', 'position': 7},  # abcabca
                {'matched_text': 'abcabcabca', 'position': 10},  # abc+abcabca
                {'matched_text': 'abcabcabc', 'position': 9},  # abc+abc+abc
            ])

    def test_stops_iteration_on_empty_match(self):
        self._test_unique_match(
            text='abcabcabca',
            match=RepeatMatch(InsertLiteralMatch('abcabca'), 0, None),
            expected_solution={'matched_text': 'abcabca', 'position': 0})

    def test_alternative_with_empty_match(self):
        self._test_match(
            text='abcabca',
            match=RepeatMatch(
                AlternativesMatch(
                    LiteralMatch('abc'),
                    InsertLiteralMatch(','),
                ),
                0, None),
            expected_solutions=[
                {'matched_text': 'abcabc,', 'position': 6},
                {'matched_text': 'abc,abc,', 'position': 6},
                {'matched_text': ',abcabc,', 'position': 6},
                {'matched_text': ',abc,abc,', 'position': 6},
            ])
