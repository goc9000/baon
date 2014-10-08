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
            text=u'abcdefghi',
            match=SequenceMatch(
                LiteralMatch(u'abc'),
                LiteralMatch(u'de'),
                LiteralMatch(u'fgh'),
            ),
            expected_solution={'matched_text': u'abcdefgh', 'position': 8})

    def test_empty_sequence(self):
        self._test_unique_match(
            text=u'abcdefghi',
            match=SequenceMatch(),
            expected_solution={'matched_text': u'', 'position': 0})

    def test_single_item(self):
        self._test_unique_match(
            text=u'abcdefghi',
            match=SequenceMatch(LiteralMatch(u'abc')),
            expected_solution={'matched_text': u'abc', 'position': 3})
        self._test_no_match(
            text=u'abcdefghi',
            match=SequenceMatch(LiteralMatch(u'def')))

    def test_fail_middle(self):
        self._test_no_match(
            text=u'abcdefghi',
            match=SequenceMatch(
                LiteralMatch(u'abc'),
                LiteralMatch(u'xxx'),
            ))
