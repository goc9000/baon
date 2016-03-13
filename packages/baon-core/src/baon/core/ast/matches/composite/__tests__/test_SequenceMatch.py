# baon/core/ast/matches/composite/__tests__/test_SequenceMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch


class TestSequenceMatch(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text='abcdefghi',
            match=SequenceMatch(
                LiteralMatch('abc'),
                LiteralMatch('de'),
                LiteralMatch('fgh'),
            ),
            expected_solution={'matched_text': 'abcdefgh', 'position': 8})

    def test_empty_sequence(self):
        self._test_unique_match(
            text='abcdefghi',
            match=SequenceMatch(),
            expected_solution={'matched_text': '', 'position': 0})

    def test_single_item(self):
        self._test_unique_match(
            text='abcdefghi',
            match=SequenceMatch(LiteralMatch('abc')),
            expected_solution={'matched_text': 'abc', 'position': 3})
        self._test_no_match(
            text='abcdefghi',
            match=SequenceMatch(LiteralMatch('def')))

    def test_fail_middle(self):
        self._test_no_match(
            text='abcdefghi',
            match=SequenceMatch(
                LiteralMatch('abc'),
                LiteralMatch('xxx'),
            ))
