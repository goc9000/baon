# baon/core/ast/matches/control/__tests__/test_RepeatMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.core.ast.matches.control.AlternativesMatch import AlternativesMatch
from baon.core.ast.matches.control.RepeatMatch import RepeatMatch
from baon.core.ast.matches.control.SequenceMatch import SequenceMatch
from baon.core.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.core.ast.matches.pattern.FormatMatch import FormatMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.positional.EndAnchorMatch import EndAnchorMatch


class TestRepeatMatch(MatchTestCase):

    def test_basic(self):
        self._test_match(
            text='abcabcabcabca',
            match=RepeatMatch(LiteralMatch('abc'), 0, None),
            expected_solutions=[
                {'matched_text': 'abcabcabcabc', 'position': 12},
                {'matched_text': 'abcabcabc', 'position': 9},
                {'matched_text': 'abcabc', 'position': 6},
                {'matched_text': 'abc', 'position': 3},
                {'matched_text': '', 'position': 0},
            ])

    def test_maximum(self):
        self._test_match(
            text='abcabcabcabca',
            match=RepeatMatch(LiteralMatch('abc'), 0, 2),
            expected_solutions=[
                {'matched_text': 'abcabc', 'position': 6},
                {'matched_text': 'abc', 'position': 3},
                {'matched_text': '', 'position': 0},
            ])

    def test_minimum(self):
        self._test_match(
            text='abcabcabcabca',
            match=RepeatMatch(LiteralMatch('abc'), 2, None),
            expected_solutions=[
                {'matched_text': 'abcabcabcabc', 'position': 12},
                {'matched_text': 'abcabcabc', 'position': 9},
                {'matched_text': 'abcabc', 'position': 6},
            ])

    def test_fail_match(self):
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
                ).add_action(ApplyFunctionAction('parens')),
                0, None),
            expected_solutions=[
                {'matched_text': '(abc)(abc)(abc)', 'position': 9},
                {'matched_text': '(abc)(abc)', 'position': 6},
                {'matched_text': '(abc)(abcabca)', 'position': 10},
                {'matched_text': '(abc)', 'position': 3},
                {'matched_text': '(abcabca)', 'position': 7},
                {'matched_text': '', 'position': 0},
            ])

    def test_stops_iteration_on_empty_match(self):
        self._test_unique_match(
            text='abcabcabca',
            match=RepeatMatch(InsertLiteralMatch('defgh'), 1, None),
            expected_solution={'matched_text': 'defgh', 'position': 0})

    def test_alternative_with_empty_match(self):
        self._test_match(
            text='abcabca',
            match=RepeatMatch(
                AlternativesMatch(
                    LiteralMatch('abc'),
                    InsertLiteralMatch(','),
                ).add_action(ApplyFunctionAction('parens')),
                0, None),
            expected_solutions=[
                {'matched_text': '(abc)(abc)(,)', 'position': 6},
                {'matched_text': '(abc)(abc)', 'position': 6},
                {'matched_text': '(abc)(,)(abc)(,)', 'position': 6},
                {'matched_text': '(abc)(,)(abc)', 'position': 6},
                {'matched_text': '(abc)(,)', 'position': 3},
                {'matched_text': '(abc)', 'position': 3},
                {'matched_text': '(,)(abc)(abc)(,)', 'position': 6},
                {'matched_text': '(,)(abc)(abc)', 'position': 6},
                {'matched_text': '(,)(abc)(,)(abc)(,)', 'position': 6},
                {'matched_text': '(,)(abc)(,)(abc)', 'position': 6},
                {'matched_text': '(,)(abc)(,)', 'position': 3},
                {'matched_text': '(,)(abc)', 'position': 3},
                {'matched_text': '(,)', 'position': 0},
                {'matched_text': '', 'position': 0},
            ])

    def test_optional_match(self):
        match = SequenceMatch(
            FormatMatch('s').add_action(ApplyFunctionAction('parens')),
            RepeatMatch(FormatMatch('d'), 0, 1).add_action(ApplyFunctionAction('braces')),
            FormatMatch('s').add_action(ApplyFunctionAction('curlies')),
            EndAnchorMatch(),
        )

        self._test_unique_match(
            text='Time 2 Die',
            match=match,
            expected_solution={'matched_text': '(Time) [2] {Die}', 'position': 10})
        self._test_unique_match(
            text='Time Die',
            match=match,
            expected_solution={'matched_text': '(Time)[] {Die}', 'position': 8})
        self._test_unique_match(
            text='Time 2',
            match=match,
            expected_solution={'matched_text': '(Time)[] {2}', 'position': 6})
